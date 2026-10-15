#!/usr/bin/env python3
"""Make the live-log hooks fail open, in Claude Code and in Cursor.

Every hook command that runs group/live/live-log.py is rewritten so that:
  - when the script file exists, the command runs exactly as before;
  - when it is missing, the hook exits 0 and lets the work through (printing the "allow" answer Cursor expects).
Until now a missing file made python3 exit 2 ("can't open file"), which both apps took as "block".

Usage:  python3 -I fix-hooks.py            shows what would change (dry run)
        python3 -I fix-hooks.py --apply    writes the changes, keeping <file>.bak-16Oct26 beside each file
        python3 -I fix-hooks.py [--apply] <settings file> ...   only those files

Default files (project root from LIVE_LOG_ROOT, else ~/Desktop/consensorAI/design-systems-09Oct26):
  <project>/.claude/settings.json  <project>/.claude/settings.local.json  <project>/.cursor/hooks.json
  ~/.claude/settings.json          ~/.cursor/hooks.json
Already-wrapped commands are left alone, so running this twice is safe.
"""
import difflib
import json
import os
import shlex
import sys

MARK = "live-log fail-open"


def wrap(command):
    """The fail-open form of one hook command, or None when it is not a live-log command / already wrapped."""
    if "live-log.py" not in command or MARK in command:
        return None
    try:
        words = shlex.split(command)
    except ValueError:
        return None
    i = next((k for k, w in enumerate(words) if w.endswith("live-log.py")), None)
    if i is None:
        return None
    path = words[i]
    mode = words[i + 1] if i + 1 < len(words) else ""
    app = words[i + 2] if i + 2 < len(words) else ""
    if app == "cursor":  # what live-log.py itself answers for Cursor when it cannot run
        answer = {"inject": '{"continue":true}', "record": "{}"}.get(mode, '{"permission":"allow"}')
        allow = 'printf "%s\\n" "' + answer.replace('"', '\\"') + '"; '
    else:  # Claude Code: exit 0 with no output means "go ahead"
        allow = ""
    inner = (f'# {MARK}: run the script when it exists, otherwise let the work through\n'
             f'f="{path}"; if [ -f "$f" ]; then exec {command}; fi; {allow}exit 0')
    return "sh -c " + shlex.quote(inner)


def rewrite(obj, changes):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "command" and isinstance(v, str):
                new = wrap(v)
                if new:
                    obj[k] = new
                    changes.append((v, new))
            else:
                rewrite(v, changes)
    elif isinstance(obj, list):
        for v in obj:
            rewrite(v, changes)


def main(argv):
    apply = "--apply" in argv
    files = [a for a in argv if a != "--apply"]
    if not files:
        root = os.environ.get("LIVE_LOG_ROOT") or os.path.expanduser("~/Desktop/consensorAI/design-systems-09Oct26")
        files = [os.path.join(root, ".claude", "settings.json"), os.path.join(root, ".claude", "settings.local.json"),
                 os.path.join(root, ".cursor", "hooks.json"), os.path.expanduser("~/.claude/settings.json"),
                 os.path.expanduser("~/.cursor/hooks.json")]
    touched = 0
    for path in files:
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                before = f.read()
            data = json.loads(before)
        except (OSError, ValueError) as e:
            print(f"skip {path}: {e}")
            continue
        changes = []
        rewrite(data, changes)
        if not changes:
            print(f"{path}: no live-log hook commands to change")
            continue
        after = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        print(f"\n{path}: {len(changes)} command(s)")
        for old, new in changes:
            print("  -", old)
            print("  +", new.replace("\n", "\\n"))
        if apply:
            with open(path + ".bak-16Oct26", "w", encoding="utf-8") as f:
                f.write(before)
            with open(path, "w", encoding="utf-8") as f:
                f.write(after)
            print(f"  written, backup at {path}.bak-16Oct26")
            touched += 1
        else:
            sys.stdout.writelines(difflib.unified_diff(before.splitlines(True), after.splitlines(True), path, path + " (after)"))
    if not apply:
        print("\nDry run. Add --apply to write.")
    else:
        print(f"\n{touched} file(s) written.")


if __name__ == "__main__":
    main(sys.argv[1:])
