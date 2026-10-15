# Handoff — CP-2 KYC and age policy — 16 Oct 2026

**State:** drafted, waiting on ōkina. Documents only. Nothing is built, nothing is live, and nothing on consensor.io has
been changed.

## Files

| File | What it holds |
|---|---|
| `group/work/policy/KYC-AGE-POLICY.md` | The policy (sections 1–10, 32 sources). Each rule is marked Decided, Proposed, Open, Fact or ⚖️. Last edited 15 Oct 13:47. |
| `group/work/policy/GIVING-POLICY.md` §5 | Its headline rules, pointing to the policy. |
| `group/work/pathways/PATHWAYS.md` | The CP-2 row and the CP-2 section: decided, proposed, still open, lawyer list. |
| `~/Library/Application Support/Claude/side-session-notes/local_cf25325d-…/cp2-kyc-age-policy-ledger-impact.md` | What the policy means for the ledger and the board, for whoever builds them. |

## Decided by ōkina (15 Oct 2026). Don't reopen these.

- Sign-in is Google or Apple only, for now, through consensor.io. That is the KYC.
- Australian law is the base (Bluelabs Pty Ltd).
- 16 is the minimum everywhere; 18 for anything sensitive.
- The age check comes with the Google or Apple sign-in, with extra steps where needed.

## Next steps

1. **Get ōkina's answers to policy §10** (10 questions), as chat buttons, not prose. The three that matter most:
   - **Apple:** launch with Google only and add Apple later with a typed date of birth plus a second check. Which
     age-check company, and what budget?
   - **The board:** keep it free of likes, view counts, endless scroll, vanishing posts and picked-for-you posts?
     Since 26 Mar 2026 (Rules s 4A), any of those may bring giving under the under-16 law.
   - **The ledger:** record age checks as salted fingerprints only, with the result in a store that can be wiped? Do
     the same for an under-age account's sealed post records? Keep a one-word note of how each check was done?
2. **As ōkina answers,** change the rule from Proposed to Decided in all three files: the policy, GIVING-POLICY §5 and
   PATHWAYS CP-2. Replace the old text; don't annotate it.
3. **Lawyer pack:** turn policy §1.3 (L1–L6) into a brief for a lawyer. L1 is the big one: is giving an
   "age-restricted social media platform"?
4. **Build nothing before the decisions.** Once they're made, start with Google's approval of the birthday permission
   (policy §9 step 5). It takes 2–6 weeks, so it is the longest wait.

## Where this touches other work

- **Ledger (CP-1 build, offline copy).** An age result must never sit in a block. Each block holds only a fingerprint
  made with a random secret; the result and the secret live in a separate age store that can be wiped (OAIC Part 4A
  guidance; draft children's code s 32). Lawyer item L3.
- **Board features.** Under Rules s 4A, likes, counts, endless scroll, vanishing posts or picked-for-you posts may put
  giving in scope. Anyone adding these should check with ōkina first.
- **CP-3 team-chat pilot.** Members must be verified 18 or over. That matches "Verified 18" in policy §4.3: a stronger
  check from §3.5 on top of the sign-in. Team chat is a new kind of space (GIVING-POLICY §1) that policy §4.1 doesn't
  list yet. Add a row ("Team chat (pilot): 16–17 no; 18+ verified") once ōkina decides CP-3.

## Gaps and unconfirmed points

- **Google's classification of the birthday permission.** Google's scopes page lists `user.birthday.read` but doesn't
  say whether it is "sensitive". Before submitting, confirm on the Data Access page of consensor.io's Google Cloud
  Console. Policy §3.2 currently says approval is needed.
- **Which Google birthday to use.** The People API can return birthdays from more than one place: the Google Account,
  the profile, or a contact card. Google's documentation doesn't say which one is the account birthday. Test with real
  accounts; if the dates differ, treat it as "no birthday on file".
- **Rules s 4A wording.** Taken from eSafety's assessment page and Clayton Utz (May 2026). The instrument text on
  legislation.gov.au loads by script and couldn't be read directly.
- **Source [4] (Bird & Bird)** blocks scripted checks (403). It opens in a browser.
- **No run receipt.** The 15 Oct run receipt wasn't written: the sandbox blocks writes to `~/BlueLabs3/harness`. Record
  it from an unsandboxed shell with `scripts/record_run.py`.
