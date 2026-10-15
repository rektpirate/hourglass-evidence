# Handoff: research lab, idea web and the LAPS × BlueLabs map

**Session ID:** 012fZhS2iJf7mBXzHdwB8m7v
**Window:** Thu 15 Oct 2026, 11:27 pm → Fri 16 Oct 2026, 2:42 am (Brisbane)
**Project:** the research lab for giving.consensor.io, plus a two-sided map of Fondazione LAPS and BlueLabs

---

## 1. What happened, in order

| # | Time (Brisbane) | Ask | Result |
|---|---|---|---|
| 1 | 15 Oct 11:27 pm | Deep research on the best user experience for walking into an online laboratory research library, broken down top to bottom | Report written: **Online research library UX.md**. 5 research strands, about 9,300 words |
| 2 | 15 Oct 11:55 pm | Clarified: the visuals of "the deep interconnected web of cross-pollinated ideas", not a library catalogue | 5 new research strands on the idea web |
| 3 | 16 Oct 12:13 am | "Show a quick snapshot of what it might look like" | Inline mock shown in chat |
| 4 | 16 Oct 1:07 am | "Try it" | Built **idea-web-prototype.html**, a standalone draggable prototype |
| 5 | 16 Oct 1:08 am | Told: this is the research lab for giving.consensor.io | Noted |
| 6 | 16 Oct 1:13 am | Research Fondazione LAPS. Map BlueLabs / Habitat / consensor on one side and LAPS on the other. An integration room comes after | 3 research strands on LAPS. Built **laps-bluelabs-map.html** |
| 7 | 16 Oct 2:42 am | Handoff | This file |

The idea-web report (**Interconnected idea web visuals.md**) completed in the background and is included here. It was not sent in chat.

---

## 2. Files in this folder

| File | What it is | State |
|---|---|---|
| `handoff-012fZhS2iJf7mBXzHdwB8m7v.md` | This handoff | Final |
| `laps-bluelabs-map.html` | Two-sided map: BlueLabs left (16 ideas), LAPS right (24), empty integration room in the middle. Click for detail and sources. Drag dots or whole sides, resize sides, scroll to zoom | Working, tested in a headless browser with no errors |
| `idea-web-prototype.html` | Idea-web prototype: zoom (atlas → region → neighbourhood), typed links, link evidence panel, machine links on/off, drag and resize | Working, tested. Uses **sample data, not real papers**. The top-left name is the placeholder "Idea Web" |
| `Interconnected idea web visuals.md` | Full research report on the idea web, about 8,700 words | Final |
| `Online research library UX.md` | First research report (library-style layout). Kept for its identifier, metadata and accessibility sections | Final; you said its framing missed what you meant |
| `research-notes/` | All 13 underlying research note files, every claim with a source link | Raw material |

Both HTML files are self-contained, with no outside links or branding. Each remembers your dragged layout on the device it's opened on. **Copy layout** gives the positions as JSON.

---

## 3. The idea web: what the research says

### Core findings

| Topic | Finding | Strength |
|---|---|---|
| The big picture | A stable **2D atlas** to orient people, a **small live neighbourhood** (about 25–150 nodes) for the actual exploring, and a **text version** of everything | Strong for 2D and small neighbourhoods |
| Dividing the map | OpenAlex Topics: **4 domains → 26 fields → 252 subfields → 4,516 topics**, built from citation clusters. ANZSRC Fields of Research as an optional Australian tag | Strong (open standard) |
| Distance on the map | People read close as similar or agreeing. It isn't. Maps of this kind admit their distances "do not have concrete meaning", so the screen must say what closeness means | Strong |
| How many nodes people can read | Most studies tested 100 nodes or fewer. Error rates climb steeply at about 900–1,000 | Moderate |
| Links | Each link needs a type (supports / contradicts / uses method or data), who asserted it, confidence, quoted evidence and status. Machine links drawn differently from human ones | Standards exist (CiTO 2.9.0, Sep 2026). The display scheme is a design choice with no study behind it |
| Retractions | Should flag every link that depends on retracted work. Crossref's Retraction Watch data is free | Strong |
| Cross-field bridges | Measurable: field diversity, bridge position, unusual combinations, sleeping beauties. The **disruption index is in a live Nature dispute (Aug 2026)**, so mark it contested | Mixed |
| 3D / VR | Helps untangle a small cluster. Slower and worse for the big picture, and causes motion sickness. **Optional mode only** | Weak to moderate |
| Graph tools vs plain lists | The only controlled study is Apolo (12 people), which beat Google Scholar on relevance. Connected Papers, Litmaps, ResearchRabbit and others have **no peer-reviewed evaluation** | Weak |
| Browser rendering | cosmos.gl and deck.gl handle around 1M nodes. These are vendor numbers, not independent benchmarks | Vendor claims |
| Accessibility | Data Navigator and Olli make graphs navigable by keyboard and screen reader. Organise it as summary → detail | Moderate |

### Exploration journey (recommended)

```
Arrive (seed question or free wander)
  → Orient (2D atlas, labelled regions, "what distance means" shown)
    → Pick a thread (one click focuses a small neighbourhood)
      → Follow it (each hop shows why: link type, quote, who, confidence; list view one click away)
        → Cross-field jump (bridge papers as stepping stones)
          → Save the trail (automatic trail, named and annotated, shareable)
```

---

## 4. Fondazione LAPS: the facts

| Item | Fact | Source |
|---|---|---|
| Name | **Libera Accademia Progetti Sperimentali**. "Laboratorio Alte Professionalità Sociali" has no source and was wrong | Statute Art. 1; site footer |
| Founded | 23 Feb 2016, Turin, by Lapo Elkann alone, by notarial deed. €80k endowment plus €80k operating funds | lapsonlus.org statute PDF |
| Legal status | ONLUS Nov 2016. Entered in Italy's Third Sector register as an Ente Filantropico, 19 May 2026 (Regione Piemonte decree DD 803). Codice fiscale 97804180012. Permanent branch in Portugal | Decree PDF; statute |
| Official site | lapsonlus.org | — |
| Governance | President Lapo Elkann, Vice-President Joana Lemos Elkann, 14-member board (incl. Alain Elkann, Diane von Fürstenberg, Andrea Stroppa). Founder appoints the President. All posts unpaid | lapsonlus.org/governance |
| Core values (Code of Ethics 2018) | The person is the central value; freedom, self-determination, self-realisation; children "the most precious good", with a right to be happy and to be heard; UN Convention on the Rights of the Child as inspiration | Code of Ethics PDF |
| Mission | Fight educational poverty; minors with special educational needs (disability, learning disorders, addiction, abuse, poverty) | lapsonlus.org/la-fondazione |
| Founder's own reasons | Has said publicly that his childhood dyslexia is why he created LAPS. Has spoken publicly about addiction and recovery and about asking for help | MeteoWeb Oct 2019; Verissimo Sep 2020 |
| Flagship now | **Casa LAPS Cascais**, opened 2 Oct 2026 (10th year). A shelter for women and children escaping domestic violence: 9 suites, stays up to 6 months, 24h security and psychological support, about €900k. Aim is autonomy, not only safety. Plans for an international network | ANSA 2 Oct 2026; Euronews 3 Oct 2026 |
| Past work | 2019 ADHD/dyslexia and Red Cross pilots; 2020–22 emergency campaigns (#NeverGiveUp over €1M; #OurDuty €414,084.70 in Italy); housing in Funchal and Milan | Press and partner releases |

### Gaps and cautions on the LAPS side

| Item | Detail |
|---|---|
| Accounts | Not published; the site's reports page is missing. Deloitte certification claimed but unverified |
| Impact | Output counts only (6,000 minors and 600 teachers, 2017–19, no method) |
| Quiet stretch | Site shows no projects after 2022 and no events after Dec 2023, until Cascais. Social channels were not checked |
| Technology stance | Only wary positions found (quit social media in 2017; digital-addiction projects). Nothing on AI, data rights or crisis technology |
| 2026 statute | Required for the new registration but not published |
| March 2025 allegations | A former collaborator made allegations reported by La Verità. LAPS denies them and says the person demanded €5M. No court outcome reported. **Unproven** |

---

## 5. BlueLabs side of the map: what it's built from

Only things you stated yourself, taken from your saved notes. Nothing invented.

| Group | Ideas on the map |
|---|---|
| Beliefs | Dignity and sovereign connection · Fighting for those who can't · Mechanism, not mind · Human always in the loop · Maslow as the measure · Your rails (Rudin, Galloway, Gottschlich, Harris) |
| What it builds | THEUS · HOURGLASS · O-KID ledger · consensor · Research lab · Six-part system |
| Who it serves | Suicide prevention (paced, 12–24 months) · People in recovery and children online · Turning inquiry recommendations into rules |
| Proof and gaps | Facts, not hopium · The weak spots you name yourself |

**Missing:** the names of your six pillars. They're not in the saved notes. Give them and they go on the map.

---

## 6. Open items

| # | Item | Waiting on |
|---|---|---|
| 1 | **Integration room**: aligned ideas from both sides meet and get fleshed out together | Your go |
| 2 | Names of the six pillars | You |
| 3 | Name for the idea-web prototype (replaces "Idea Web" top-left only) | You |
| 4 | Swap the prototype's sample data for real papers | Your go |
| 5 | Check LAPS's Instagram, Facebook and LinkedIn for 2024–26 activity the website doesn't show | Your go |

### Strongest overlaps to take into the integration room (from the research, not yet tested)

| BlueLabs | LAPS | Shared ground |
|---|---|---|
| Fighting for those who can't fend for themselves | The person and the child at the centre | Protecting people who can't protect themselves |
| Human always in the loop | Asking for help as part of recovery | Getting a person to real human help |
| Suicide prevention; people in recovery | Founder's openness on addiction and recovery; minors with addiction | Recovery |
| HOURGLASS: people control access to their data | Cascais: safety, dignity, privacy, autonomy | Safety that leads to autonomy |
| Kids' phones filter; recovery feed blur | Digital-addiction projects for young people | Young people's digital harm |
| Facts, not hopium; ledger that binds you too | No published accounts or outcome data | **A gap BlueLabs could fill**: verifiable impact records |

---

## 7. Where things live

| Thing | Location |
|---|---|
| This folder | `~/Desktop/16Oct26-the-day-in-full/` |
| Lapo / LAPS notes | Saved memory, Lapo file (now covers the foundation too) |
| Research lab notes | Saved memory, online research library file |
