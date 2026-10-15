# live-log "ready" marks — handoff (16 Oct 2026)

From claude·1670. File: `group/live/live-log.py` (the only file changed, 15 Oct 11:04). Nothing released or deployed for this.

## In one line

An agent can mark only its **own** giving work ready. Cursor can't mark Claude's, Claude can't mark Cursor's. ōkina can mark either.

## Why

15 Oct 10:43:28 the log got `claude·cli | ready | Owner asked to ship the current tree`. Claude didn't write it.
Cursor (session 333b7856) did, straight after ōkina wrote "push nit" to it (Cursor transcript line 455):
`… live-log.py ready claude "Owner asked to ship the current tree" && ./release-blue.command cursor`.
Its 10:44:32 release (14d14df9) shipped claude·f217's half-built picture editor; the card's + picture buttons were broken on live until 10:53.
The same Cursor session had marked Claude ready twice before that day (05:46, 10:24). Its own shell lines never reached LIVE.md
(failed commands and a bare `./release-blue.command cursor` aren't logged), so the transcript was the only record.

## How it works now

- **Who's asking** comes from the shell's environment, set by each app on every command its agent runs:
  Claude Code `CLAUDECODE=1` + `CLAUDE_CODE_SESSION_ID`; Cursor's agent `CURSOR_AGENT=1` + `CURSOR_CONVERSATION_ID`
  (same id the hooks tag as `cursor·xxxx`). Neither = a person (ōkina in Terminal) = may mark either. Both = can't tell = refused.
- **Two places refuse** `ready <other agent>`:
  1. `shellguard`, the pre-shell hook in both apps, before the command runs (uses the hook's own way of telling the apps apart).
     It also refuses a `ready` command that sets or clears those marks (`CLAUDECODE=…`, `unset`, `env -i/-u`). A quoted mention,
     like `grep "live-log.py ready cursor"`, is allowed.
  2. `live-log.py ready` itself: exit 1, plain message, nothing written.
- **The ready line names who marked it**: `claude·f975` (that session), or `claude·okina` (a person marked Claude's work).
  `released` lines are unchanged (`okina·cli`, `cursor·cli`, …). `check` and `pending()` read the agent before the `·`, as before.
- ōkina's "release anyway" button path is unchanged: `release-blue.command okina` answers its own prompt and never calls `ready`.

## State on 16 Oct 02:45

- `python3 -I group/live/live-log.py selftest` → **44 of 44** (28 older + 16 for this: own mark, other agent's mark refused, ōkina,
  both marks, the 10:43 replay, and 8 hook cases).
- One ready mark since: `claude·f975` at 00:14 (new tag working). No cross-marks tried, so no refusal seen in real use yet.
- Releases since: ōkina's at 00:22 and 00:23.
- Run recorded with `record_run.py`; not mirrored to Notion.

## Open

1. **Two Claude sessions are both "claude".** Any Claude session's `ready claude` clears every Claude session's edits, and a release by
   one Claude session skips all Claude edits as its own. Same accident, Claude-to-Claude. Proposed as its own session
   ("Per-session ready marks for concurrent Claude seats"); not started.
2. Failed commands and a bare `./release-blue.command <agent>` don't reach LIVE.md. Harmless to the check today; it only cost us the trail.
3. Notes for the other sessions: `~/Library/Application Support/Claude/side-session-notes/local_cf25325d-…/ready-mark-owner-check.md`.

## If you touch it

Re-read `live-log.py` first (claude·955e also changed it on 15 Oct: the false-alarm fix). Run the selftest before and after.
Don't run a release to test it, don't edit `publish/giving` for it, never edit `group/green-site`.
