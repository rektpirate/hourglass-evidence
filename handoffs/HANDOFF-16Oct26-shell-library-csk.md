# Handoff — 16 Oct 2026, 02:40 AEST

The session that held the Application shell, the documents library, library.consensor.io and the Consensorship Kit ended mid-run (context full). Nothing has been released. Three workflows stopped part-way; their scripts are on disk and can be run again fresh (a new session can't resume them from cache).

Scripts: `~/.claude/projects/-Users-okinaasagao-Desktop-consensorAI-design-systems-09Oct26/f975a626-02e7-4242-8915-6c47560fe659/workflows/scripts/`

## Standing rule for every document

Zero author notes in any document: no quotes of the owner, no "the owner said", no agent names or stamps, no process chatter, no swearing anywhere on a site. The only personal mark is the owner's sign-off at the bottom of each document. **The sign-off wording hasn't been given yet: ask for it before adding any.**

## 1. Application shell (giving, local only)

Files: `publish/giving/static/appshell.js`, `appshell.css`, `src/index.js` (appShellPage, THEUS apps), `group/work/theus/TOOLKIT.md`, `LIVE-CODE-CONTRACT.md`.

- **Done and verified on localhost:8787/r/theus/caselock-v2:**
  - **The Functions column as live code:** PROFILE, LIVE_VIEW, RUNTIME, ANALYTICS and FUNCTIONS, reacting to every tap.
  - **Stage geometry:** the phone sits 16px from the stage's top, bottom and left; the stage corner equals the phone corner + 16 (concentric). Measured at 1440, 1280 and 1180.
  - **The toolkit:** With / Without THEUS, Group functions, Zoom out / % / Zoom in, Fit, Follow the phone, Clear run marks.
- **Interrupted — toolkit centring and scroll** (`toolkit-centre-scroll-wf_67139b6f-db3.js`). The toolkit is now centred on the nav's axis, shortens as the page narrows, and scrolls across inside the bar. The build and the reviews ran; the fix pass was editing `appshell.js` at 02:36 when the session ended.
  - **Next:** run `node --check publish/giving/static/appshell.js`, then `python3 -I publish/giving/build.py`. Check at 1440, 1000 and 390 wide: the bar's centre equals the nav pill's centre, it never crosses the phone or the Functions column, and the row scrolls. Re-run the script if anything is off.
- **Open for the owner:** Fit to view now fits everything (about 24% in CaseLock). The alternative is to stop at reading size and pan.
- **Release, on the owner's word only:**
  1. `release-apps.command`, because the CaseLock app in the phone changed (`caselock-v2/js/shell.js`, `app.js`).
  2. Mark claude ready in LIVE.md.
  3. `release-blue.command`, run in the owner's Terminal. Cursor (cursor·f0d9) is also editing `src/index.js` and Research.

## 2. Author-note sweep

`strip-author-notes-wf_26619e0a-f05.js` stopped part-way.

- **Cleaned:**
  - the nine library documents (`documents-library/docs/`);
  - `TOOLKIT.md`, `LIVE-CODE-CONTRACT.md`, `HANDOFF-CASELOCK-SHELL.md`, `publish/giving/shells/APPLICATION-SHELL.md`, `publish/apps/AGENTS.md`;
  - by hand: comments in the THEUS apps and shell parts of `src/index.js`, `group/work/theus/CLAIM.md`, `publish/library/AGENTS.md`.
- **In progress when it stopped:**
  - the register: `document-stack/APP-DOCUMENT-REGISTER-16Oct26.md`, `register-data.json`, `App-Document-Register.html`, and its library copy `DL-0008`;
  - the proof scan.
- **Next:** re-run the script. Its last step rebuilds `library-data.js` with `build-docs.py` and prints the grep proof the owner asked for. Then republish the App Document Register artifact from the cleaned HTML.
- **Still to clean:** the comment at the top of the Stage section in `appshell.css` ("owner's reference, 14 Oct 2026").
- **Other sections:** the list for Cursor is in `group/work/common/FIXES-FOR-CURSOR.md` under "New site rule". That covers the Mapping transcript pages and the Research comments and files. The language atlas's entry for the esoteric programming language named "BF" in short is the owner's call.

## 3. Documents library (prototype)

`documents-library/`, at http://localhost:4378/documents-library/ (the design-shell preview serves the project root).

- **Built:**
  - a menu on the left with search, and an instant markdown canvas;
  - read-only canvases, where questions wait for the AI, and writable canvases with in-place edit and a `[[` cite picker;
  - cite chips, Cites / Cited by, and deep links;
  - `library.json` as the citation index.

  `laps.js` (the locked microphone) is byte-identical to giving's.
- **Owner's verdict:** the content is wrong. It was seeded with build notes. It must be rebuilt around the app document register:
  - the register's sections A–P as the menu;
  - each item (e.g. DOC-B04) as its own read-only page, with its sources as citations;
  - each app gets writable copies with a status (needed, conditional, not applicable, done), CaseLock first.
- **Open owner calls:** darken the bar's placeholder (it fails contrast); wide tables shown as records; the menu docked from 960px.

## 4. library.consensor.io

`publish/library/` (Worker `consensor-library`), `release-library.command`.

- **Built:**
  - the Worker that serves the documents library canvas (section 3) behind sign-in: `publish/library/build.py` copies `documents-library/` into `public/` on every build, and the Worker sets the page's session token on it;
  - consensor.io sign-in, copied from giving;
  - `LIBRARY_EMAILS` set to `"*"`, meaning any consensor.io account with a verified email (the owner's choice);
  - the files gated by `cross-origin-resource-policy: same-origin` and `Sec-Fetch-Site`;
  - the voice endpoints copied from giving;
  - a privacy page and sign-out.
- **Tested:** local checks passed (53/53).
- **Hold the release** until the library holds the right content (section 3). The release script creates the D1 database, applies the migrations, deploys and checks the live site.
- **Local dev:** the command is in `publish/library/AGENTS.md`. A dev server may still be running on 8793.

## 5. Consensorship Kit (CSK)

Three layers, defined in `csk/research/00-scope-app-library-and-csk.md`:

1. **The base library:** standards, laws, guidelines, templates, the register.
2. **An app library per app:** provenance, build logs, change logs, release history, research, decisions, tests and reviews, incidents.
3. **The CSK per app:** the inspector-facing package. It answers every inspector's checks (store review, security, privacy, accessibility, domestic-violence safety, marketing and claims, due diligence, legal, architecture) with every dossier, every node and edge, the Q&A bank and a status per item, all pointing into the app library and the code.

The app library and the CSK attach to each app on the THEUS apps page, signed-in only.

- **Status:** `csk-research-wf_b4a0b2be-d2c.js` (nine inspector lenses, then the design, then a completeness critic) stopped before any lens finished.
- **Next:** run it again. It writes `csk/research/*.md` and `csk/CSK-SPEC.md`. **Present the plan to the owner before building anything.**

## 5b. The pull-down board (not built)

The pill pulls down like a blind and reveals a large board behind the canvas. It is not built anywhere on the web. What exists:

- `group/work/board/PLAN-pull-down-board.md`: the plan, written 15 Oct, never started. Its target was the Laps page on giving, the board being giving's own map (rooms, place cards, THEUS apps, Mapping pages).
- The original in the THEUS chat Mac app: `~/BlueLabs3/projects/theus-chat/integration/new-ai-chat/Sources/` (`SmartBoard.swift`, `ChatPanelView.swift`), with its spec at `~/BlueLabs3/harness/projects/ai-chat-panel/docs/SPEC-smart-board.md`.
- The documents library canvas was copied without it, on purpose.

Needs the owner's call on where it goes first (the documents library canvas, or giving's Laps page) before building.

## 6. Servers this work uses

- design-shell (static, project root): 4378
- giving dev: 8787
- consensor stand-in: 8788
- apps dev (CaseLock): 8796
- library dev: 8793

## 7. Housekeeping

- No `record_run.py` receipts were written for this session's work (apps site, releases, register, code view, toolkit, library, library site).
- Notion mirroring is outstanding.
- M5 memory health is falling (Computer History capture stopped, binding refused, runs not mirrored).
