# hourglass-evidence

Documents and scripts rescued from the consensorAI design-systems project on 16 Oct 2026, when the hook script `group/live/live-log.py` went missing on the Mac and both apps' hooks blocked every write and shell command.

## What is here

| Path | What it is | Named author or session | Date |
|---|---|---|---|
| `TODO-16Oct26.html` | The TODO list from every handoff: your calls, what agents can do now, waiting on outside people, releases, parked. Open it in a browser; ticks are saved per browser | | 16 Oct 2026 |
| `handoffs/HANDOFF-CASELOCK-SHELL.md` | CaseLock v2 shell, local preview, locked decisions | | 15 Oct 2026, 22:47 |
| `handoffs/HANDOFF-16Oct26-shell-library-csk.md` | Application shell, author-note sweep, documents library, library.consensor.io, Consensorship Kit, pull-down board | session f975a626 | 16 Oct 2026, 02:40 |
| `handoffs/HANDOFF-release-check-16Oct26.md` | The release check in `live-log.py` | claude·955e | 16 Oct 2026 |
| `handoffs/HANDOFF-ready-marks-16Oct26.md` | The ready marks in `live-log.py` | claude·1670 | 16 Oct 2026 |
| `handoffs/HANDOFF-CP2-16Oct26.md` | CP-2 KYC and age policy | | 16 Oct 2026 |
| `handoffs/HANDOFF-giving-offline-16Oct26.md` | giving offline build, policy, team-chat pilot. Could not be written on the Mac (`giving-offline/HANDOFF-16Oct26.md`); recovered from the blocked session | claude·f217 | 16 Oct 2026 |
| `handoffs/handoff-research-lab-laps-16Oct26.md` | Research lab, idea web, LAPS × BlueLabs map | session 012fZhS2iJf7mBXzHdwB8m7v | 16 Oct 2026, 02:42 |
| `contracts/LIVE-CODE-CONTRACT.md` | Live code in the Functions column, contract | | 15–16 Oct 2026 |
| `group/live/live-log.py` | Verbatim copy of the missing hook script. Restore it to the same relative path in the project | | 15 Oct 2026 |
| `publish/giving/test-local.sh` | Verbatim copy of giving's local test runner | | |

## The hook script

`group/live/live-log.py` here is byte-identical to the copy uploaded on 16 Oct 2026.

- sha256: `7572d88b327abd5f8b4884db76a2da5368948561fcf0eb58e3af9fb09befa36d`
- `python3 -I group/live/live-log.py selftest` from this copy: 44 of 44 passed (16 Oct 2026), the same count both `live-log.py` handoffs record.

Restore on the Mac, in Terminal (outside both apps):

```sh
cp group/live/live-log.py "/Users/okinaasagao/Desktop/consensorAI/design-systems-09Oct26/group/live/live-log.py"
cd "/Users/okinaasagao/Desktop/consensorAI/design-systems-09Oct26" && python3 -I group/live/live-log.py selftest
```

Why a missing file blocks work: the script exits 0 on every internal failure, but when the file itself is absent Python exits 2 before the script runs, and exit code 2 is the code Claude Code's hooks treat as a block.

Both `HANDOFF-CP2-16Oct26.md` uploads were identical; one copy is kept.
