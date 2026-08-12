#!/usr/bin/env python3
"""Stop hook: refuse to let a reply claim verification that never happened.

AI Coding Blueprint for Non-Developers, v1.0.0 (MIT).
Safe to overwrite with a newer version: this file holds nothing project-specific.

CLAUDE.md rule 1 says never write "verified"/"deployed"/"tests pass" without pasting
the output that proves it. Documentation alone does not reliably stop this, so this
hook enforces it in code.

The check: if the final reply of a turn asserts a verification-class claim, then a
matching command must have actually run in that same turn. Category-specific -- a
"deployed" claim is not satisfied by having run pytest.

Blocks by printing {"decision": "block", "reason": ...}. Claude then either runs the
real check or rewrites the claim honestly. stop_hook_active short-circuits the second
pass, so this can never loop.
"""
import json
import re
import sys


def strip_noise(text):
    """Remove spans where a claim word is being discussed rather than asserted.

    Fenced blocks, inline code, blockquotes, and double-quoted phrases. Replaying
    real sessions showed the common false alarm is a reply *talking about* the
    words -- e.g. a rule quoted as "verified/working/deployed" -- which is not a
    claim about anything.
    """
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"^\s*>.*$", " ", text, flags=re.M)
    text = re.sub(r"[\"“][^\"”\n]{0,120}[\"”]", " ", text)
    return text


# A claim that is being DENIED is the honest disclosure the rule asks for.
# "Nothing has been committed or deployed" must never be blocked.
NEGATED = re.compile(
    r"\b(not|never|nothing|none|no|isn't|is not|aren't|wasn't|weren't|hasn't|"
    r"has not|haven't|have not|didn't|did not|don't|do not|can't|cannot|"
    r"could not|couldn't|without|unverified|untested|undeployed|yet to be|"
    r"still needs?|before)\b[^.!?\n]{0,90}$", re.I)


def is_negated(text, index):
    """True if the claim at `index` sits inside a negative statement."""
    return bool(NEGATED.search(text[max(0, index - 140):index]))


# claim -> (what must have run, human name)
#
# Adjust the evidence regexes to match YOUR project's real deploy/test tooling.
# The defaults below cover common cases (docker, npm/yarn/pnpm, pytest, tsc, etc.)
# but if your deploy is e.g. `flyctl deploy` or `vercel --prod`, add those tokens.
CLAIMS = [
    (
        "deploy",
        re.compile(
            r"\b(deployed|shipped to (prod|production)|"
            r"live (on|at|in) (prod|production)|"
            r"(server|app|site|service)s? (is|are) (now )?live)\b", re.I),
        re.compile(
            r"\b(docker|deploy(\.sh)?|ssh|scp|compose|kubectl|systemctl|launchctl|"
            r"vercel|netlify|flyctl|fly deploy|heroku|git push (heroku|origin main))\b",
            re.I),
        "a deploy command (docker/deploy.sh/ssh/compose/vercel/etc.)",
    ),
    (
        "tests",
        re.compile(
            r"\b(tests? (pass|passed|passing)|suite (is )?green|all green|"
            r"0 fail(ed|ures)?|no failures|type ?check(s)? (pass|clean)|tsc clean)\b", re.I),
        re.compile(
            r"(\b(pytest|npm (run )?test|yarn test|pnpm test|vitest|jest|tsc|mypy|"
            r"ruff|go test|cargo test|unittest)\b"
            r"|\btest[_-]?\w*\.(py|mjs|js|ts|go|rs)\b)", re.I),
        "the test/typecheck command itself (pytest/npm test/tsc/a test script)",
    ),
    (
        "verified",
        re.compile(
            r"\b(verified|confirmed|proven|i (checked|tested|verified|confirmed)|"
            r"works (now|correctly|end to end)|is working|working correctly)\b", re.I),
        None,  # any real command or browser/simulator call counts
        "a command that actually checks it",
    ),
]

# tool calls that count as "went and looked", beyond Bash
LOOKED = re.compile(r"(Claude_Browser|claude-in-chrome|iOS_Simulator|computer-use)", re.I)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never break the session on a malformed payload

    # second pass after we already blocked once -- let it through
    if payload.get("stop_hook_active"):
        sys.exit(0)

    path = payload.get("transcript_path")
    if not path:
        sys.exit(0)
    try:
        with open(path, encoding="utf-8") as fh:
            entries = [json.loads(l) for l in fh if l.strip()]
    except Exception:
        sys.exit(0)

    # find the start of this turn: the last genuine user message, meaning one
    # that is not merely a tool_result being fed back in
    start = 0
    for i, e in enumerate(entries):
        if e.get("type") != "user" or e.get("isMeta"):
            continue
        content = e.get("message", {}).get("content")
        if isinstance(content, str):
            start = i
        elif isinstance(content, list) and any(
                b.get("type") != "tool_result" for b in content if isinstance(b, dict)):
            start = i

    # Claims are read from THIS turn only -- that is what is being asserted now.
    # Evidence is read from the WHOLE session: verifying in one turn and reporting
    # in the next is normal and honest, and blocking it produces mostly false
    # alarms. What this still catches is claiming something was checked when
    # nothing of that kind was ever run at all.
    said, ran = [], []
    for i, e in enumerate(entries):
        if e.get("type") != "assistant":
            continue
        for block in e.get("message", {}).get("content", []) or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                if i >= start:
                    said.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                name = block.get("name", "")
                if name == "Bash":
                    ran.append(str(block.get("input", {}).get("command", "")))
                else:
                    ran.append(name)

    reply = strip_noise("\n".join(said))
    if not reply.strip():
        sys.exit(0)

    commands = "\n".join(ran)
    looked = bool(LOOKED.search(commands))

    for _, claim_re, eviden_re, needed in CLAIMS:
        m = next((m for m in claim_re.finditer(reply)
                  if not is_negated(reply, m.start())), None)
        if not m:
            continue
        if eviden_re is None:
            # "verified" class: any command run, or a browser/simulator look
            if commands.strip() or looked:
                continue
        elif eviden_re.search(commands):
            continue
        print(json.dumps({
            "decision": "block",
            "reason": (
                f'This reply says "{m.group(0)}" but nothing in this session ever ran '
                f"{needed}.\n\n"
                "CLAUDE.md rule 1: never write verified / working / fixed / deployed / "
                "confirmed without pasting the output that proves it, in the same reply.\n\n"
                "Do one of these, then finish:\n"
                "  1. Actually run the check and paste its output, or\n"
                "  2. Rewrite the claim to say plainly what you did and did not verify.\n\n"
                "An honest gap is always cheaper than a wrong confirmation."
            ),
        }))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
