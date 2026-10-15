# Go-live runbook — paste this into a Claude Code session on the Mac

Project: `/Users/okinaasagao/Desktop/consensorAI/design-systems-09Oct26`. Start with `cd` there. Every command runs from there unless a step says otherwise.

This is the owner's word for every release below. Do the whole runbook without asking, except at the stop points in part 7. Report once at the end (part 8). Short plain sentences; say what is real and what is a picture.

## 0. Preflight (5 minutes)

1. `python3 -I group/live/live-log.py selftest` must end `44 of 44 passed`. If the file is missing: `curl -fsSL https://raw.githubusercontent.com/rektpirate/hourglass-evidence/claude/new-session-5ye0kk/group/live/live-log.py -o group/live/live-log.py` and run the selftest again.
2. `python3 -I group/live/live-log.py check claude`. Note what it lists. Never run `ready cursor`.
3. Start the servers the tests need, each in its own background process, from `.claude/launch.json`: the consensor stub on 8788, and the apps dev server on 8796 (`publish/apps`, `wrangler dev --local --ip 127.0.0.1 --port 8796 --var APPS_LOCAL:yes`, with `CLOUDFLARE_API_TOKEN` unset). Confirm `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8796/caselock-v2/` prints 200. The giving site's local tests return 404 on `/apps/caselock-v2/` without it.
4. `git status` at the project root if it is a git repository; note the state, do not commit anything yet.

## 1. Live today

- CaseLock v2 app and the giving shell went live on 16 Oct 2026 (release-apps, then release-blue). Rollback point `c4077d1e-4346-4ddd-9eb5-f8088746a32b`, `group/stages/blue-20261015T175922Z.txt`. Cursor's Research edits went with it.
- Check now, in a headless browser or with curl, that `https://giving.consensor.io/r/theus/caselock-v2` serves the shell with `appshell.js` and that `/apps/caselock-v2/` answers 200 framed. Check `/r/research` loads. If either is broken, stop (part 7, stop point A).

## 2. giving offline work → live (the big one)

Sources: `giving-offline/HANDOFF-16Oct26.md`, `giving-offline/FROZEN.md` (every change since the freeze from live `4f1b9802`), `giving-offline/giving/` (the offline copy), `group/work/policy/GIVING-POLICY.md` (now possibly under `group/work/theus/`).

1. Read FROZEN.md and the handoff in full. List every file the offline copy changed.
2. Live `publish/giving` has moved since the freeze: the picture editor, the app shell, Cursor's Research work, tonight's release. For each changed file, port the offline change INTO `publish/giving` by hunk. Never copy a whole offline file over a live one that has also changed. `diff -r giving-offline/giving publish/giving --exclude public --exclude .wrangler --exclude node_modules` is the starting map.
3. `static/laps.js`: only the save code changed offline. The voice functions (`voiceLive`, `voiceText`, the speech language, the AI binding) must stay byte-identical to live. Prove it with a diff before and after.
4. Migrations: carry the offline migrations (Your space, posts, publish, the ledger blocks, admin openings) into `publish/giving/migrations` in order. Apply them only locally through `wrangler dev`. `release-blue.command` applies them remotely at release. Never run a remote D1 command yourself.
5. `build.py` must run the map snapshot: `dev/canonical-map/gen.py` → `public/maps/giving-canonical-map.html`, the way `giving-offline/stamp.py` does it. Port `dev/canonical-map/` and `dev/e2e.py` additions with it.
6. Privacy page: state what is kept on the server (each account's 25 MB space; the Laps page saves there, only its owner reads it) and in the ledger (a SHA-256 chain of publish, take back and admin openings; fingerprints, never words). Keep the house style: plain, short, no explainer banner across the top.
7. Fix the two known problems while you are in the code: the publish scrub that took a 13-digit number in a title for a phone number; the ledger error during Publish that returns an HTML 500 instead of JSON (offline `src/index.js` around lines 1609–1614).
8. Tests: port the offline `dev/e2e.py` cases (138 passed offline) into the live `dev/e2e.py` without dropping any live case. Then `node --check publish/giving/src/index.js`, `python3 -I publish/giving/build.py`, and the full local run (`test-local.sh`, wherever it now lives: `group/live/` or `publish/giving/`). Everything must pass. A failure that survives two fix attempts is stop point B.
9. Release: `python3 -I group/live/live-log.py ready claude "giving offline work: your space, publish, ledger blocks, canonical map, privacy page"` then `./release-blue.command claude`. If it stops on another agent's unfinished work, that is stop point C. After it says released: confirm `/r/mapping` serves the map snapshot, `/privacy` has the new text, and a signed-in Laps save lands in Your space on the live site.

## 2b. LAPS Foundation room (the owner's go, 16 Oct 2026)

Spec and first content: `LAPS-FOUNDATION-ROOM.md` in this repo (fetch it beside this runbook). Build it as a giving room at `/r/laps`, signed-in only, with the map from `~/Desktop/16Oct26-the-day-in-full/laps-bluelabs-map.html` as the canvas and the seven items filled into the integration room, each with its sources from `~/Desktop/16Oct26-the-day-in-full/research-notes/`. Keep every rule in the spec: facts with sources, "our reading" where it is inference, the allegations off the page, no author notes, no sign-off. Add it to the site's crawl and e2e checks (room loads signed in, redirects signed out, the map's script runs, every card opens). Release it with part 2's release-blue, or on its own if part 2 is not ready.

## 3. Small fixes from the to-do (do all, in this order)

1. `publish/giving/static/appshell.css` line 59: remove the comment "owner's reference, 14 Oct 2026". Rebuild, release with the next release-blue (fold it into part 2's release if that is still ahead).
2. `group/work/pathways/PATHWAYS.md` CP-3 row: D1–D11 are decided, D12–D19 open.
3. `group/work/pilot/ENCODING-SEQUENCE.md` line 669 (D6): "Elkin" → "Elkann".
4. Links: `GIVING-POLICY.md`, `KYC-AGE-POLICY.md` and `HANDOFF-CP2-16Oct26.md` live under `group/work/theus/` now. Point `PATHWAYS.md` and the handoffs at the real paths.
5. `group/work/theus/CLAIM.md`: the app shell is no longer held by claude·f975 (that session ended). Record who holds it now (this session).
6. `group/work/speed/HANDOFF.md` step 3: drop the "known false alarm" text; it was fixed on 15 Oct.
7. Toolkit: open `http://localhost:8787/r/theus/caselock-v2` at 1440, 1000 and 390 wide in a headless browser and screenshot. The bar is centred on the nav pill, never over the phone or the Functions column, and the row scrolls. If it is off, fix it in `static/appshell.js`/`appshell.css` and fold it into the next release.

## 4. Re-run the interrupted workflows

Scripts: `~/.claude/projects/-Users-okinaasagao-Desktop-consensorAI-design-systems-09Oct26/f975a626-02e7-4242-8915-6c47560fe659/workflows/scripts/`

1. `strip-author-notes-wf_26619e0a-f05.js`: finishes the register (`document-stack/APP-DOCUMENT-REGISTER-16Oct26.md`, `register-data.json`, `App-Document-Register.html`, `DL-0008`), rebuilds `library-data.js` with `build-docs.py`, prints the grep proof. Then republish the App Document Register artifact from the cleaned HTML.
2. `csk-research-wf_b4a0b2be-d2c.js`: writes `csk/research/*.md` and `csk/CSK-SPEC.md`. Write the plan into `csk/PLAN.md`. Do not build the kit.
3. Standing rule for every document: zero author notes, no owner quotes, no agent names or stamps, no process chatter, no swearing on any site. No sign-off anywhere: the wording has not been given.

## 5. Documents library and library.consensor.io

1. Rebuild `documents-library/` around the App Document Register: sections A–P as the menu; each item (e.g. DOC-B04) its own read-only page with its sources as citations; per-app writable copies with a status (needed, conditional, not applicable, done), CaseLock first. `laps.js` stays byte-identical to giving's.
2. `publish/library/build.py` copies it into `public/`; run the library's local checks (53 passed on 16 Oct) and fix to green.
3. Release with `release-library.command` ONLY if the owner has said "library yes". Otherwise stop at a built, tested, unreleased site and say so in the report.

## 6. Receipts and mirrors

1. `scripts/record_run.py` from a shell outside the sandbox, one receipt per piece: the apps site release, tonight's giving release, part 2's release, the register, the toolkit, the library work, the CP-2 run of 15 Oct, session claude·f217's offline build.
2. Mirror the runs to Notion if the connector is available; otherwise list them in the report as not mirrored.

## 7. Stop points (the only reasons to ask the owner)

- A: a live page from part 1 is broken. Say which, and offer `./rollback-blue.command`.
- B: a test fails after two honest fix attempts. Paste the failure and your two attempts.
- C: release-blue lists another agent's unfinished work. Never mark it ready. Say whose, which files, and ask: wait, or release anyway.
- D: a merge in part 2 where both sides changed the same logic and either choice loses behaviour. Show both and recommend one.
- E: anything that would touch `wrangler.jsonc` placement, the voice functions in `laps.js`, `group/green-site`, or a remote database.

Put each as one decision at a time, with a recommendation and one alternative, as chat buttons. Never "type yes".

## 8. Report (one message at the end)

What is live, with version ids and rollback points. What is built but not released and why. Which stop points you hit and how they were resolved. Test counts. Then the receipts written. Nothing else.

## Rules that bind all of it

- giving goes live only through `release-blue.command`. Never `wrangler deploy` or any direct deploy. Never edit `group/green-site`. Never run remote D1 commands on `consensor-giving`. No placement in `wrangler.jsonc`.
- The microphone is locked: `voiceLive`, `voiceText`, the speech language and the AI binding in `static/laps.js` stay exactly as they are.
- Each agent marks only its own work ready. Never mark Cursor's.
- Offline first; every change proven locally before it ships.
- Decisions for the owner as chat buttons, one at a time, with a recommendation and one alternative.
- No explainer banners across the top of tool pages. Plain language, short.
