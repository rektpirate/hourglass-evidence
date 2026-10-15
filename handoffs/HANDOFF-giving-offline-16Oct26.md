# Handoff: giving offline build, policy and the team-chat pilot

Session claude·f217, 15–16 Oct 2026, for ōkina (Joel West). Written so the next agent can pick up without the chat.

**Nothing from this session is live.** Live giving.consensor.io is still release 4f1b9802 (picture editing, 15 Oct).
Everything below is offline, in documents, or waiting on ōkina's word.

## 1. Where everything is

| What | Where |
|---|---|
| Offline copy of giving (frozen from live 4f1b9802, plus this session's work) | `giving-offline/giving/` (this folder). What changed since the freeze: `giving-offline/FROZEN.md` |
| giving canonical map (source) | `giving-offline/giving/dev/canonical-map/` (gen.py, map.html, serve.py) |
| giving canonical map (snapshot the site serves at /r/mapping) | `giving-offline/giving/public/maps/giving-canonical-map.html` |
| Offline helpers | `giving-offline/stamp.py` (copies static files to public, stamps `?v=`, runs the map snapshot), `giving-offline/seed.py` |
| Old first version of the map (superseded, keep or delete on ōkina's word) | `giving-offline/tree/` |
| giving policy, every rule with its status | `group/work/policy/GIVING-POLICY.md` |
| KYC and age policy (drafted by a separate session) | `group/work/policy/KYC-AGE-POLICY.md` |
| Crisis and critical pathways register (CP-1, CP-2, CP-3) | `group/work/pathways/PATHWAYS.md` |
| End-to-end encoding sequence for the team-chat pilot | `group/work/pilot/ENCODING-SEQUENCE.md` |
| The 62 review issues behind that document (10 blockers, all addressed in it) | `group/work/pilot/encoding-review-issues.json` |
| Workflow that wrote the sequence (6 reads, 6 checks, design, 3 critiques, revision) | `~/.claude/projects/-Users-okinaasagao-Desktop-consensorAI-design-systems-09Oct26/f217cce2-d1cd-40cd-8bb7-4aecfb6de5c4/workflows/scripts/campaign-encoding-sequence-wf_d3d3f10c-c15.js` |
| Full chat transcript | `~/.claude/projects/-Users-okinaasagao-Desktop-consensorAI-design-systems-09Oct26/f217cce2-d1cd-40cd-8bb7-4aecfb6de5c4.jsonl` |

The offline copy was moved here from the session scratchpad on 16 Oct 2026, because a reboot clears the scratchpad.
`.claude/launch.json` now points "giving-offline" and "giving-canonical-map" here.

## 2. Running it

1. Start "giving-consensor-stub" (8788, the stand-in for consensor.io sign-in), "giving-offline" (8797) and
   "giving-canonical-map" (8798) from `.claude/launch.json`. If 8788 is already taken, another session's stub is
   running and works as is.
2. Test: `python3 -I dev/e2e.py` from `giving-offline/giving`. **138/138 passed on 16 Oct 2026 from this folder.** The
   sandbox blocks localhost, so the test has to run outside it.
3. The map on 8798 redraws live as the source changes. The site's copy is a snapshot: re-run `stamp.py` after changes.

The offline `wrangler.jsonc` names the Worker `consensor-giving-offline` with a placeholder database id. It cannot
reach live.

## 3. Built offline this session (tested, not live)

Full list in `FROZEN.md`. In short:

- **giving canonical map.** Every route, page, script, function, table and outside service in giving, with
  the wires between them. Clicking a script fans its functions out to the left. Crisis-pathway code is pink. Mapping
  opens on it first. ōkina named it "giving canonical map" and rejected "clean tree".
- **Your space.** Every account gets 25 MB on giving's server, made at sign-up. The Laps page saves there, not only in
  the browser. Only its owner reads it. A save that would go over 25 MB is refused (proven in SQL).
- **Publish.** A post goes out under the card's name or its @handle, never a typed alias. You can only publish what
  is already on your own page. Emails and phone numbers are scrubbed out. The limit is 20 posts an hour. The Publish
  box reminds people that @handle posts are held to a stricter standard. A post can be taken back, and the record
  stays.
- **The ledger's first blocks.** A SHA-256 chain records publish, take back and an admin opening a record. A tamper
  test changed one word and the check reported "BROKEN at block 1 of 5". It is not anchored yet.
- **Admin Records tab.** It shows the chain status and the posts. A record opens only with a written reason, and each
  opening is itself a ledger block.

## 4. What ōkina decided (15 Oct 2026)

**Publish and storage:**
- The board is the only public space. Everything else is personal until Publish.
- Personal writing lives on the server, 25 MB per account.
- A post goes out under your name or your @handle.
- Take back is allowed, but the record always stays, for disputes.
- @handle posts are critiqued more strictly.

**KYC (CP-2):**
- Sign-in is by Google or Apple only, and that is the KYC.
- The policy follows Australian law (Bluelabs Pty Ltd).
- The minimum age is 16 everywhere. Sensitive things need 18.
- Age needs extra steps beyond sign-in.

**Team-chat pilot (CP-3), decisions D1–D11 of `ENCODING-SEQUENCE.md` Part C:**

| # | Decided |
|---|---|
| D1 | Both paths. The submission's Report mode is built first: a member reports one message, only that message is checked, on the server. ōkina's sweeping design is built on top as a separately labelled room, never cited for Davos or Italy, because it breaks promises in the pitch, the letter and the Italy readiness rules. |
| D2 | Real drug and alcohol words and phrases are on the list from the start. |
| D3 | Matched, not banned. Adults may talk about drugs and alcohol. A match means the admin checks it, help is shown first, and the message is always delivered. |
| D4 | giving's own ledger holds the records, as fingerprints, never words. Anchoring gets built on giving. The HOURGLASS gate is not used. |
| D5 | Team chat is a third kind of space, with its own rules and its own storage allowance. |
| D6 | The members are ōkina, Lapo Elkin, Joanna Robbie Madison and Tom Krzyzewski, on a server-checked list, one device each. ōkina confirmed in writing that all four are 18 or over. That confirmation becomes the first pilot ledger block once those events are built; it is not in the ledger yet. |
| D7 | 3 matches from one person within 30 days before anything opens, in the sweeping room. A cryptographer designs fake matches so the count below 3 is hidden. |
| D8 | IP address and location are off for the pilot. An empty sealed slot is kept for after the lawyer answers L7 and L11. |
| D9 | The admin sees the matched phrase, its category, the count, the time, the date and the account, never the rest of the message. |
| D10 | When a case is decided, the person is told in their own space. The reporter's name is never shown. |
| D11 | Messages are kept while the chat exists. Vouchers and sealed packages go after 30 days. Dismissed case details are destroyed within 30 days, with the ledger fingerprint kept. Confirmed cases are kept until any dispute closes. |

ōkina's own sequence and his correction (nothing is ever read; the fingerprint is made on the device before
encryption; matching is blinded) are in memory `giving-chat-pilot.md` and in `ENCODING-SEQUENCE.md` B.1.

## 5. Still open

- **Pilot:**
  - Decisions D12–D19 (`ENCODING-SEQUENCE.md` Part C) are still open. The walkthrough paused after D11, when my reply bringing D12 was cut off before it finished.
  - Lawyer questions L7–L13.
  - A cryptographer and an outside privacy reviewer.
  - Nothing is built. The document's build order says decisions, legal answers and a privacy impact assessment come first.
- **KYC:** `KYC-AGE-POLICY.md` waits on ōkina's answers (section 10) and a lawyer (L1–L6).
- **CP-1 disputes:** who may raise one, what they see, time limits, the hand-off to crisis help (`PATHWAYS.md`).
- **Ledger:**
  - The full ledger (every action in the portal, anchoring to OpenTimestamps and Rekor) was planned, then stopped by ōkina. Only the first blocks exist.
  - Anyone with write access to the database could rebuild the chain today, until anchoring exists.
- **Labs and the city:** the Labs plugin installer, the Research Lab cabinet with its draft and pre-publish step, and the "little city" of buildings in a 3D orbit were talked through. None is built.
- **Carrying to live**, only on ōkina's word:
  - Copy the offline changes into `publish/giving`.
  - `build.py` must run the map snapshot.
  - The privacy page must say what is kept on the server and in the ledger.
  - Release with `./release-blue.command claude` only.

## 6. Known problems found

- **The publish scrub took a 13-digit number in a test title for a phone number** and removed it.
- **A ledger error during Publish returns an HTML 500 page, not JSON** (`src/index.js`, around lines 1609–1614 of the offline copy).
- **The campaign page's "print" is an illustration, not a working mechanism.** That covers the 9 missing places, the red key, the match and the report. Its gaps hide about 5 bits, which anyone can rebuild (`ENCODING-SEQUENCE.md` Part A).
- **giving's server reads private Laps pages today**, for the Publish draft check. So "nobody reads your words" is only true of the pilot chat design.

## 7. Rules that bind this work

- Release only via `./release-blue.command claude`.
- Never deploy directly.
- Never run remote D1 commands on `consensor-giving`.
- Never edit `group/green-site`.
- **The microphone is locked.** ōkina, 15 Oct: "we keep the microphone the same". Do not change voiceLive, voiceText, the speech language or the AI binding in `static/laps.js`. This session changed only the save code in laps.js, and the voice functions were checked untouched.
- Do not add placement to `wrangler.jsonc`.
- Don't mark Cursor's work ready.
- Offline first. Nothing goes live without ōkina's word.

## 8. How ōkina works

- **Decisions as chat buttons:** one decision at a time, with a recommendation and one alternative. Never "type yes".
- **Map links:** when he asks to see something on giving, every bold name of a map node is a link to `http://127.0.0.1:8798/#<node id>`.
- **No explainer banners** across the top of tool pages.
- **Plain language, short.** Say what is real and what is a picture.

Memory files for all of this: `~/.claude/projects/-Users-okinaasagao-Desktop-consensorAI-design-systems-09Oct26/memory/`.
The relevant ones are giving-chat-pilot, giving-crisis-pathways, giving-public-board-only, giving-map-links, no-explainer-banners,
okina-decisions-as-buttons and giving-blue-green.
