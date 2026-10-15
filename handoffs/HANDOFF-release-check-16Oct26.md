# Handoff: the release check (group/live/live-log.py), 16 Oct 2026

Written by claude·955e. State checked 16 Oct 02:4x: `python3 -I group/live/live-log.py selftest` → 44 of 44 passed.

## What it does now
`./release-blue.command <who>` runs `live-log.py check <who>`. That check stops the release if another agent changed the giving source
(`publish/giving`) since the last release and hasn't marked the work ready.

- **Harmless shell commands don't count** (15 Oct, claude·955e). These are commands that only mark ready, check or record a release,
  run release-blue / mirror-green / rollback-blue, run `node --check <file>`, `cd`, or read files (ls, cat, grep, head, tail, wc,
  diff, `sed -n N,Mp`, …). The hook sees the whole command and logs these as `run` instead of `shell`. Long lines end in `…`, and new
  lines inside a command show as ` ; `.
- **Everything else still counts.** That covers writing to a file (`>`, cp, mv, rm, rsync, tee, `sed -i`), heredocs (`<<`), `$(…)`,
  `VAR=…` in front, subshells, and open quotes. When unsure, it counts.
- **`ready` is only for your own work** (15 Oct ~11:05, claude·1670). The script works out who is calling it from the shell's
  environment, and the pre-shell hooks refuse `ready <the other agent>` before it runs. ōkina, in Terminal, can mark either agent.
  Ready lines name who marked them (`claude·f217`, `claude·okina`).

## Open
1. **Running `build.py` or `test-local.sh` still counts as a change.** Both only rebuild `public/` and run tests, but they weren't on
   the list I was given. Right now 19 of Cursor's lines are waiting, several of them `node --check … && python3 -I publish/giving/build.py`.
   This is ōkina's call; if yes, add both to `harmless_command()` and add a self-test case.
2. **All Claude sessions are "claude".** One Claude session's `ready claude` clears every Claude session's edits, and a Claude release
   skips all Claude edits. The same bug applies between Claude seats (e.g. 955e and f217).
3. **Some commands never reach LIVE.md.** A failed command never does, and neither does a bare `./release-blue.command cursor`
   (no `group/` or `publish/giving` in its text). The `released` line still appears.
4. **A copy out of giving still counts** (e.g. `cp publish/giving/static/x group/work/…`). The check can't tell which way a copy goes.
5. `group/work/speed/HANDOFF.md` step 3 still describes the "known false alarm". That section belongs to claude·f217.

## Changing the script safely
- Both apps' hooks run this file on every message, edit and shell command. Edit a scratch copy, run its `selftest`, compare
  `check claude` / `check cursor` with the live copy, then swap it in with one `cp` to a temp name followed by `mv`.
- Don't put a deploy command's text in your own shell command, even as test data, because `shellguard` will refuse it. Put test
  payloads in a file.
- Never run a release or deploy to test this, never edit `group/green-site`, and never mark another agent's work ready.

Notes from the sessions that did this work: `~/Library/Application Support/Claude/side-session-notes/local_cf25325d-8f91-4a2a-a468-fc65a3d90fdf/`
(`release-check-false-alarm.md`, `ready-mark-owner-check.md`).
