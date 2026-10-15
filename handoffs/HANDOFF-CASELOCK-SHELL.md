# CaseLock v2 shell — state at 15 Oct 2026, ~22:47 AEST

Nothing in this work has been committed, pushed, or released. Do not run `release-blue.command`. Do not `wrangler deploy`. Do not edit `group/green-site`. Do not start a second worker on 8787.

Live site: https://giving.consensor.io
CaseLock shell on the live site: https://giving.consensor.io/r/theus/caselock-v2
That live page does **not** have this work. It still serves `publish/giving/public/appshell.css` and `public/appshell.js`, which are the old copies. The new shell is only in `publish/giving/static/`. `build.py` copies static into public. A release is the only way the world sees it.

## Local preview

The work shows in the local preview, not on the website:

http://127.0.0.1:8794/

Server: `python3 -I -m http.server 8794 --bind 127.0.0.1` with cwd `group/work/caselock-shell`. If the page refuses the connection, start that again. Do not use another port. Prove every change here before it goes live; do not release to show a change.

Page file: `group/work/caselock-shell/index.html`
It links `appshell.css` and `appshell.js` by symlink to `publish/giving/static/`. Cache-bust query on those links is `?v=light1`. HTML is served with no cache header from Python, but an open tab keeps the old script. Open `http://127.0.0.1:8794/?v=light1` in a new tab rather than trusting a reload of an old one.

Local giving worker is already on 127.0.0.1:8787. It serves `public/`, so it still shows the old shell. Do not treat 8787 as proof of this work.

## What the phone is

There are two different phones. Do not mix them up: say which URL shows which phone.

1. **The phone on 8794** is an iframe of the real CaseLock app: `caselock-v2/` via symlink `group/work/caselock-shell/app`. That app runs. Passcode, vault, Notes cover, Leave. Script query in the iframe is `app/?v=icons1`.

2. **The phone on giving.consensor.io** is `publish/giving/shells/application/caselock-v2/phone.html`. The worker strips script, style, iframe, and event handlers (`phoneSafe` in `publish/giving/src/index.js`). `build.py` refuses those too. So the website phone cannot run the CaseLock program. It can only show the static screens in `phone.html` / `phone.css`. That rule stands. Do not put an iframe or script into `phone.html`.

## Locked, in order

Do not undo these. Do not redesign them while "improving" something else. When a change misses, fix the named thing in place; do not add a parallel version beside it.

### CaseLock vault (the app, not HOURGLASS)

HOURGLASS VDR is the wrong room: no request form, no email, no organisation. CaseLock's vault:

- Owner opens it with a platform passkey only (Face ID, Touch ID, Windows Hello). `userVerification: required`. PRF salt `caselock-vdr-vault-v1`. No server.
- Lawyer or police open a sealed copy with the share phrase. They do not use her passkey. The vault on her phone stays shut.
- Files: `caselock-v2/js/passkey.js`, additions in `caselock-v2/js/vault.js`, door UI in `caselock-v2/js/app.js`. App script query `js/app.js?v=icons1`. CSS `app.css?v=gray1`. Theme color `#e7e7e7` (giving shell gray, `room.css` body `#e7e7e7`).

### Leave returns to the cover

`leave()` in `caselock-v2/js/app.js` calls `lock()`. It must not `location.replace` to the Bureau of Meteorology. That navigation inside the phone frame went blank (the weather site will not be framed). Cover `notes` shows the shopping note. Cover `calc` shows the calculator. No cover shows the passcode.

Hold the word Shopping for about a second to reach the passcode. That listener is on the `h1` inside the notes iframe, armed from `shoppingList()` in `app.js`.

### The Notes page

`caselock-v2/notes/shopping.html` plus the icon PNGs cut from the reference Notes screenshot:

`back.png`, `share.png`, `more.png`, `check.png`, `clip.png`, `person.png`, `compose.png`

Words on the note are the shopping list (Milk, Bread, Bananas, Dishwasher tablets, Pasta, Tomatoes, Coffee, Tissues). Do not put back the "Questions" paragraph from the reference screenshot: the screenshot's words are removed and its Notes chrome is kept. The page is not yet signed off as a match; the open difference is the icons. The icons are those PNGs. Do not redraw them.

Background of the note is white. CaseLock app pages use `#e7e7e7` so the gray reaches the edges. Do not paint the Notes page gray.

### Shell layout (all app shells, not only CaseLock)

Source: `publish/giving/static/appshell.css` and `appshell.js`. This is the file the site will ship. It is not in `public/` yet.

Wide layout (`min-width: 1101px`):

- Stage card runs under the phone, from the left edge through to the functions column.
- Phone is on top of that canvas (`z-index: 6`), vertically centered, 20px from the left wall. Grid is `20px minmax(240px,280px) minmax(0,1fr) minmax(272px,330px)`.
- Functions stay the right-hand column, joined to the stage (no gap, square inner corners).
- The black THEUS toolkit is a horizontal tab on the top edge of the stage, not the left edge. Path is drawn in `drawIsland()` in `appshell.js`.
- Captions "User / The live app, simulated", "Stage / The back end…", and "Functions" are visually hidden. They are clipped, not `display: none`. `display: none` dropped them out of the grid and the board collapsed to a short strip that cut the phone off. The cards are pinned with `.as-dom > :not(.as-cap){grid-row:2}` so they stay in the tall row. Do not "clean this up" by setting `.as-cap{display:none}`.

### Functions column, current state

Not a dark script panel. It is light (`#fcfcfc` card, white boxes).

Each function is a nested box:

- Dropdown: Working (green), Building (yellow), Paused (red). `built` and `live` start on Working. Changing the dropdown only changes the color on the page. It does not write `functions.json`.
- Menu button `⋮`: Show on stage, Collapse.
- Open box shows the why, then nested lines `From → To`, the wire label, and the wire story. Green text when the card is Working.
- Clicking the name still lays that function's path out on the stage (`follow` / `select`), same as before.

Data for this preview: `group/work/caselock-shell/functions.json` and `stage.json` (copies of `publish/giving/shells/application/caselock-v2/`). Two functions: `fn.owner` Open the vault, `fn.share` Lawyer or police, sealed copy. Both `state: "built"`.

This functions UI is not yet approved. The light theme with the red, the yellow, the dropdown, and the menus replaced the dark version, and that is what is on the page now. Do not invent a third visual.

## Deferred

Do not start these until they are requested.

- A new function algorithm that measures what is happening, tied to research papers.
- Replacing the stage canvas with React Flow or Rete.js. Those were named as the next canvas components (dot ground, zoom control, minimap, toolbar that stays readable when zoomed; Rete if the graph has to run). Not installed. Not started.
- Shipping to giving.consensor.io.

## Files touched

Shell, the part that will ship:

- `publish/giving/static/appshell.css`
- `publish/giving/static/appshell.js`

Not updated, still the old shell until `build.py`:

- `publish/giving/public/appshell.css`
- `publish/giving/public/appshell.js`

Static phone slot (not the running app):

- `publish/giving/shells/application/caselock-v2/phone.html`
- `publish/giving/shells/application/caselock-v2/phone.css`
- `publish/giving/shells/application/caselock-v2/stage.json`
- `publish/giving/shells/application/caselock-v2/functions.json`

Local preview:

- `group/work/caselock-shell/index.html`
- `group/work/caselock-shell/stage.json`
- `group/work/caselock-shell/functions.json`
- symlinks: `appshell.css`, `appshell.js`, `room.css`, `app` → `caselock-v2`

CaseLock app:

- `caselock-v2/index.html`
- `caselock-v2/app.css`
- `caselock-v2/js/app.js`
- `caselock-v2/js/vault.js`
- `caselock-v2/js/passkey.js`
- `caselock-v2/notes/shopping.html` and the seven PNGs beside it
