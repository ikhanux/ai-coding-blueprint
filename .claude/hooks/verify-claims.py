#!/usr/bin/env python3
"""Stop hook: refuse to let a reply claim verification that never happened.

AI Coding Blueprint for Non-Developers, v2.0.0 (MIT).
Safe to overwrite with a newer version: this file holds nothing project-specific.

CLAUDE.md verification rule 1 says never write "verified"/"deployed"/"tests pass"
without pasting the output that proves it. Documentation alone does not reliably stop
this, so this hook enforces it in code.

The check: if the final reply of a turn asserts a verification-class claim, then a
matching command must have actually run in that session. Category-specific -- a
"deployed" claim is not satisfied by having run pytest.

Blocks by printing {"decision": "block", "reason": ...}. Claude then either runs the
real check or rewrites the claim honestly. stop_hook_active short-circuits the second
pass, so this can never loop.

Known limits, on purpose:
  * It confirms a matching command RAN. It does not read the output to confirm the
    command proved the right thing.
  * "fixed" and "done" are covered by the rule but not by this hook: they are used
    honestly far too often to describe an edit ("fixed the typo") for a regex to tell
    the difference. The rule still applies; the hook just does not police those two.
"""
import json
import re
import sys


def strip_noise(text):
    """Remove spans where a claim word is being discussed rather than asserted.

    Fenced blocks, inline code, blockquotes, and quoted phrases. Replaying real
    sessions showed the common false alarm is a reply *talking about* the words --
    e.g. a rule quoted as "verified/working/deployed" -- which is not a claim.
    """
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"^\s*>.*$", " ", text, flags=re.M)
    text = re.sub(r"[\"“][^\"”\n]{0,120}[\"”]", " ", text)
    return text


# A claim that is being DENIED is the honest disclosure the rule asks for.
# "Nothing has been committed or deployed" must never be blocked.
#
# The negation reaches forward to the end of the clause: a period, question mark,
# exclamation mark, semicolon, colon or line break ends it. Commas do not, so
# "nothing was deployed, verified, or tested" stays one honest denial.
NEGATED = re.compile(
    r"\b(not|never|nothing|none|no|isn't|is not|aren't|wasn't|weren't|hasn't|"
    r"has not|haven't|have not|didn't|did not|don't|do not|can't|cannot|"
    r"could not|couldn't|without|unverified|untested|undeployed|yet to be|"
    r"still needs?|before)\b[^.!?;:\n]{0,90}$", re.I)


def is_negated(text, index):
    """True if the claim at `index` sits inside a negative statement."""
    return bool(NEGATED.search(text[max(0, index - 140):index]))


# claim -> (what must have run, human name)
#
# The evidence patterns cover the common tools. If your project checks or deploys
# with something not listed (say `flyctl deploy` or `make ci`), add the token to the
# matching regex, or the hook will block claims it cannot recognise as verified.
CLAIMS = [
    (
        "deploy",
        re.compile(
            r"\b(deployed|shipped to (prod|production)|"
            r"live (on|at|in) (prod|production)|"
            r"(server|app|site|service)s? (is|are) (now )?live)\b", re.I),
        re.compile(
            r"\b(docker|deploy(\.sh)?|ssh|scp|rsync|compose|kubectl|helm|systemctl|"
            r"launchctl|vercel|netlify|flyctl|fly deploy|heroku|wrangler|"
            r"gcloud|aws|az|terraform|pulumi|cap(istrano)? deploy|"
            r"git push (heroku|origin main))\b",
            re.I),
        "a deploy command (docker/deploy.sh/ssh/compose/vercel/etc.)",
    ),
    (
        "tests",
        re.compile(
            r"\b(tests? (pass|passes|passed|passing)|tests? (is|are) green|"
            r"suite (is )?green|all green|0 fail(ed|ures)?|no failures|"
            r"type ?check(s)? (pass|passes|passing|clean)|tsc clean|"
            r"lint (is )?(clean|passes|passing)|build (passes|succeeds|is green))\b",
            re.I),
        re.compile(
            # package-manager scripts: npm test, pnpm typecheck, yarn lint, bun run build
            r"(\b(npm|pnpm|yarn|bun)( run)? (test|typecheck|type-check|lint|build|check)\b"
            # direct tools
            r"|\b(npx (tsc|eslint|vitest|jest|playwright)|pytest|python3? -m pytest|"
            r"vitest|jest|tsc|eslint|mypy|ruff|pyright|go test|go vet|cargo (test|check|clippy)|"
            r"unittest|phpunit|rspec|mix test|dotnet test|gradle test|mvn test|"
            r"make (test|check|lint|ci))\b"
            # a test file actually executed, not merely opened
            r"|\b(python3?|node|bun|deno|bash|sh|npx tsx|npx ts-node)\s+\S*test[_-]?\w*\.(py|mjs|js|ts|sh)\b"
            r"|(^|\s)\./\S*test\S*\.(py|sh|mjs|js)\b)",
            re.I | re.M),
        "the test/typecheck command itself (npm test/pytest/tsc/a test script)",
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
                "CLAUDE.md verification rule 1: never write verified / working / fixed / "
                "deployed / confirmed without pasting the output that proves it, in the "
                "same reply.\n\n"
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
