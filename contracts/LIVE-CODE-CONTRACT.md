# Live code in the Functions column — contract (15 Oct 2026)

The app runs in the phone at production level but is connected to no users, police or lawyers. The application canvas shows the functionality and the code at the same time: the Functions column on the right-hand side shows working code.

Local preview: http://127.0.0.1:8794/ (server: `python3 -I -m http.server 8794 --bind 127.0.0.1`, cwd `group/work/caselock-shell`). Everything `HANDOFF-CASELOCK-SHELL.md` lists as locked stays locked.

## What it does

The real CaseLock runs in the phone (iframe `app/` → `caselock-v2/`). The right-hand Functions column keeps its current light look (nested boxes, Working/Building/Paused dropdown, ⋮ menu). Inside each function's open box, under the why and the wire lines, it shows the **real source code** of the functions that do that job, extracted from the files the phone is running. When she uses the app, the function that runs opens, its code box is marked running, the line in the caller that calls the next traced function lights, and when it finishes the box shows "ran · N ms". Nothing calls, texts or reaches anyone: in the shell, every `tel:`, `sms:` and `mailto:` is caught and shown as not connected.

## 1. `functions.json`: new optional field `code`

```json
{ "id": "fn.unlock", "name": "...", "state": "built", "why": "...", "nodes": [...], "wires": [...],
  "code": [ { "file": "js/app.js", "name": "tryUnlock" }, { "file": "js/vault.js", "name": "unlock" } ] }
```

- `file` is relative to the app folder (`caselock-v2/`). `name` is a top-level function or `const name = ...` in that file.
- Order is call order: caller first.
- A block's **trace id** is `<basename of file>:<name>`, e.g. `app.js:tryUnlock`, `vault.js:unlock`.
- Optional `via: ["vault.js:unlock", …]`: code that can't report on its own because it runs inside vault.js or passkey.js. Its box shows "running inside unlock()" and its lines light while one of those runs. Used for unwrap, derive, unseal, seal, core and passkey open/enroll.
- Lines that ran stay marked until the phone opens that function again; a box the phone opened closes when the phone opens another (one the person opened stays).

## 2. `code.json` (generated, never hand-edited)

Written by `publish/giving/shells/extract_code.py` beside `functions.json`:

```json
{ "app": "caselock-v2", "generated_by": "extract_code.py",
  "blocks": { "app.js:tryUnlock": { "file": "js/app.js", "name": "tryUnlock", "start": 154, "end": 160, "sha256": "<hex of text>", "text": "async function tryUnlock(code) {\n ...\n}" } } }
```

- `start`/`end` are 1-based line numbers in the source file. `text` is exactly those lines.
- The extractor refuses (non-zero exit, names the ref) a ref it cannot find, and checks every block with `node --check`.

## 3. Trace messages (app → shell), `window.postMessage`

```js
{ caselockTrace: { v: 1, id: "vault.js:unlock", phase: "start" | "end" | "error", seq: 12, ms: 641 } }
```

- `ms` only on `end`/`error` (whole milliseconds). `seq` increases per message.
- **Never** arguments, return values, error messages, slot names, passcodes, phrases, keys, entry text, numbers dialled, or anything she typed.
- Sent only when the app is framed (`window.top !== window.self`), only to an allowed parent origin: `http://127.0.0.1:8794`, `http://localhost:8794`, `http://127.0.0.1:8787`, `http://localhost:8787`, `https://giving.consensor.io`. The parent origin comes from `location.ancestorOrigins[0]`, else `document.referrer`. Unknown origin: send nothing.
- Not-connected events use `id: "shell.js:notConnected"` with `phase: "start"` then `"end"`, plus `kind: "tel" | "sms" | "mailto"` (the scheme only).

## 4. App side (`caselock-v2/js/shell.js`, new, imported by `app.js`)

- `traced(ns, file)` returns a plain object: every function export of `ns` wrapped to post start/end/error and return exactly what the original returns (sync stays sync, async stays async, errors rethrown unchanged); non-functions copied.
- `wrap(file, name, fn)` for app-level functions; `app.js` reassigns its own function bindings at the end of the module (`tryUnlock = wrap("app.js", "tryUnlock", tryUnlock);`).
- Not connected: only when framed, one capture-phase click listener on `document` catches `a[href^="tel:"], a[href^="sms:"], a[href^="mailto:"]`, prevents it, posts the not-connected trace, and shows a small sheet: "Not connected. This is a demo, so nothing was called or sent. If you are in danger now, call 000 from your phone." Standalone (not framed) the links behave as they do today.
- Do not change: the passkey vault, `leave()` → `lock()`, the Notes cover and its icons, `#e7e7e7`, the duress logic, `chrome()`.

## 5. Shell side (`publish/giving/static/appshell.js` + `appshell.css`)

- Loads `code.json` with the other slots (`getJSON("code.json")`); missing file: no code boxes, nothing else changes.
- In each function's open box, after the existing why and wire lines: one code box per `code` ref, in order. Header: file, name, `lines a–b`. Body: line-numbered source, light theme (white box like the existing nested boxes, monospace ~11px, horizontal scroll inside the box, no wrapping). All text via `textContent`; a tiny tokenizer may wrap keywords/strings/comments in spans, still via `textContent`.
- Listener: accepts a message only when `e.source` is the phone iframe's `contentWindow` and `e.origin` equals that iframe's origin, and the payload matches §3 exactly (types checked). Anything else is ignored.
- On `start` of a trace id: open the first function that lists it (same as clicking its name, once per run, not per message), mark that code box running; if the caller's box is running, light the caller's line(s) containing `<name>(`. On `end`: box shows "ran · N ms" and the time; on `error`: "stopped". Not-connected events open `fn.help`.
- Keep every existing behaviour of the column and stage. No new colours beyond the existing green/yellow/red tones. Not a dark panel.

## 6. Live terminal (16 Oct 2026)

Every button press shows live in the functions list, the way a program prints to a terminal as it loads.

**Taps (app → shell).** One new message kind, same channel and origin rules as §3:
`{ caselockTrace: { v: 1, id: "tap", phase: "tap", seq: n, label: "<name>" } }`
- `label` comes only from attribute names the app wrote itself: the `data-act` value (e.g. `leave`, `saveEntry`, `detail`), `data-chip` as `chip:<name>`, `data-go` as `go:<screen>`, a keypad press as `key` (digits never), `Enter` / `Delete` for the keypad's two word keys, or `button` for anything else. Never text content, aria-label, a value, an id from data (`data-id`), a name or a number. Pattern: `^[A-Za-z][A-Za-z0-9:._-]{0,39}$`.
- Sent for every click on a button, link, `[data-act]`, `[data-k]`, `[data-chip]`, `[role=button]`, `[role=switch]` inside the app, in the capture phase, before the action runs.

**More functions traced.** Every `A` (click-action table) entry runs wrapped (trace id `app.js:<key>`), unless it is already a wrapped function (no duplicate lines). Also wrapped, so the start-up prints as it loads: `boot`, `lockScreen`, `onboarding`, `main`, `home`, `timeline`, `caseView`, `help`, `calculator`, `shoppingList`, `captureSheet`, `entrySheet`, `detail`, `settings`. Never wrap anything a timer calls every second.

**Shell.** At the top of the Functions column, a terminal: one line per message as it arrives, newest at the bottom, auto-scrolling, monospace. Time (HH:MM:SS.mmm), then indentation by call depth, then: `›` tap and its label; `▸` a function starting, shown as its signature (first line of its code.json block, trimmed) or `name()`; `✓ name · N ms` when it ends; `✕ name · stopped` on error; `⊘ not connected · tel` for a caught call. Light theme like the rest of the column (no dark panel): white, the existing greys, green for ✓, red for ✕. A line for a function that has a box opens that box when clicked. Clear button. At most 400 lines. Messages that arrive before the shell has loaded its files are kept and printed in order once it has.

**Look.** Nice, simple, clean components, not black, with nice writing.
Not a terminal look. Clean light components in the column's own style: each tap is a row with a plain-words title ("Leave", "Save entry", "Keypad"), its time small and grey on the right; the functions it ran sit under it as quiet indented rows (plain name first, the code name small in mono, "2 ms" as a soft pill). The column's sans font for writing; mono only for code names. No glyph soup, no dark background.

## 7. The Functions column as live code (16 Oct 2026) — replaces the terminal in §6 (taps from §6 stay)

The reference is a picture of a CV written as C# classes. The whole functionality list (profile, live view, current runtime, analytics) shows as live code: one button press causes a visible reaction somewhere in the code. The components stay nice, simple and clean, not black, with nice writing.

**What it is.** The whole right-hand column reads as one code file about the app, in the structure of the reference picture (summary comment, classes with typed fields, methods), on a LIGHT ground (white, the column's own greys), monospace (ui-monospace, "SF Mono", Menlo), with a restrained light syntax palette: keywords (public, class, static, void, var, string, int, bool, true, false, new) one colour, type/class names another, strings another, numbers another, comments grey. Nice writing: generous line-height, clear indentation guides (thin vertical rules like the reference picture), no glyph soup, no black.

**Sections, top to bottom (each a collapsible block):**
1. `/// <summary>` the app's line and the not-connected promise `/// </summary>`.
2. `public class PROFILE { ... }` — static facts as typed fields, from the app's new slot file `profile.json` (`profile`: list of {type, name, value, note}).
3. `public class LIVE_VIEW { ... }` — fields that change as she uses the phone: `screen` (from `profile.json` `views`: trace id → screen name, set when that function starts), `unlocked` (true after `profile.json` `unlocked.on` ends, false when `unlocked.off` starts), `lastTap` (the §6 tap label), `vault` ("open" after the vault-open function ends, "shut" on lock — names from profile.json).
4. `public class RUNTIME { ... }` — `running` (the function running now, or "idle"), `stack` (string[] of what is running, outermost first), `last` ("unlock() · 189 ms"), `uptime` (seconds since the phone loaded, ticking).
5. `public static class ANALYTICS { ... }` — counters: `taps`, `functionsRun`, `unlocks`, `avgUnlockMs`, `saves`, `notConnected`, `errors`.
6. `public static class FUNCTIONS { ... }` — each register function as a method: `/// <summary>why</summary>`, an attribute line with the existing state control (`[Working]` / `[Building]` / `[Paused]` as the same dropdown, styled as an attribute) and the ⋮ menu, then `public void OpenTheVault()` { the real code blocks from code.json, each headed by a comment `// js/vault.js · lines 72–79` }. Clicking the method name still lays its path out on the stage.

**Reactions — every tap visibly changes something in the code:**
- A field whose value changes flashes (soft green background that fades over ~900 ms) and shows its new value; counters tick up and flash.
- A function starting: its method header gets a running dot, its code lines light as today (hot/did), and `RUNTIME.running` / `stack` update; ending: `last` updates with the ms.
- A caught call: `ANALYTICS.notConnected` ticks and flashes, `LIVE_VIEW.lastTap` shows it, the help method lights.
- The column scrolls to the reacting method only when the user hasn't scrolled away in the last few seconds.

**Rules.** Everything via textContent. Values shown are only: names from the app's own markup and profile.json, counts, milliseconds, true/false. Never typed text, names, numbers she entered, passcode digits or length, entry ids. Messages arriving before the files load are queued and replayed. prefers-reduced-motion: no flash animation (the value still changes). Narrow layout keeps working. Other apps' shells without profile.json just show the FUNCTIONS class (and the summary).
