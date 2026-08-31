#!/usr/bin/env python3
"""Generate CLAUDE-HANDOFF.md — a single self-contained brief.

Written to be pasted into a fresh Claude conversation that has none of this
context. It carries the DataForSEO numbers, the campaign as built, the
guardrails, and the mistakes already made so they are not made again.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

D = Path(__file__).parent
data = json.load(open(D / "research" / "keyword_data.json"))
C, H = data["Conroe"], data["Houston"]
rows = list(csv.DictReader(open(D / "import" / "03_keywords.csv")))

# unique keyword -> where it lives and which match types are bought
where, matches = {}, defaultdict(set)
for r in rows:
    k = r["Keyword"].lower()
    where[k] = (r["Campaign"].split("| ")[-1], r["Ad Group"], r["Max CPC"])
    matches[k].add(r["Criterion Type"][0])          # E / P

def n(x):
    return 0 if x is None else x

table = []
for k in sorted(where, key=lambda k: (-n(H.get(k, {}).get("v")), k)):
    c, h = C.get(k, {}), H.get(k, {})
    camp, grp, bid = where[k]
    table.append((k, n(c.get("v")), n(h.get("v")), c.get("cpc") or h.get("cpc") or 0,
                  n(h.get("comp")), camp, grp, bid, "".join(sorted(matches[k]))))

lines = []
for k, cv, hv, cpc, comp, camp, grp, bid, mt in table:
    lines.append(f"| {k} | {cv} | {hv} | ${cpc:.2f} | {comp} | {camp} | {grp} | ${bid} | {mt} |")

live = [t for t in table if t[2] > 0]
cheap = sorted([t for t in live if 0 < t[3] <= 10], key=lambda t: -t[2])
dear = sorted(live, key=lambda t: -t[3])[:12]
cpcs = [t[3] for t in live if t[3] > 0]

doc = f"""# TML Garage Door Services — Google Ads brief

Self-contained handoff. Everything needed to fine-tune this campaign without
prior context. Written {Path(__file__).stat().st_mtime and ''}25 Aug 2026.

---

## 1. The situation

**Client:** TML Garage Door Services, Conroe, Texas. Residential and commercial
garage doors, openers, springs and driveway gates across Montgomery County and
the north Houston corridor. Phone (832) 887-8747.

**Where this stands:** a full $10,000/month Search campaign is built, and a
$2,000/month 60-day lead test is built alongside it. Nothing has spent yet.
The client wants to prove leads before committing the larger budget.

**Local Services Ads is explicitly out of scope.** It would not consume budget
and the client asked for it removed from the playbook. Do not reintroduce it
without being asked.

---

## 2. Hard constraints — check these before proposing anything

1. **Advanced Verification.** Garage door services is one of only two categories
   worldwide (the other is locksmiths) requiring Google's Advanced Verification.
   Until it passes, **no Search or PMax campaign serves at all.** Needs business
   registration, government ID, licence docs, photos of premises/vehicles/tools,
   and a video interview with Google. Re-verified every 12 months; an expired
   insurance certificate stops delivery immediately.

2. **Conversion tracking does not exist.** Both conversion points on the site are
   cross-origin iframes — the booking widget (`online-booking.workiz.com`) and
   the contact form (`st.sendajob.com`). A browser will not let the parent page
   see inside either, so **Google Ads cannot record a booking or a form fill.**
   Only phone calls are trackable, via Google forwarding numbers. Any
   recommendation that depends on conversion data must account for this.

3. **The site is not live yet.** The repaired site sits at `/fixed/` on a staging
   worker under a sitewide `noindex`. Ads point at `www.tmlgarageservices.com`.
   Cutover must happen before launch.

4. **Claims policy.** Only statements the TML site already makes may appear in ad
   copy: same-day appointments, weekend appointments at no extra charge, trained
   and insured technicians, full price quoted before work starts, service area.
   **Do not add** prices, licence/bond claims, years in business, review counts
   or award badges — none are verified. Five such lines are deliberately held
   back in `import/12_copy_held_back.csv`.

5. **Trademark.** The Competitor campaign bids on rival brand names, which is
   permitted. **Naming a competitor in ad text is trademark infringement.** No
   copy in that campaign names anyone, and it must stay that way.

---

## 3. Market data (DataForSEO, Conroe and Houston, August 2026)

### 3.1 Headline finding — clicks cost 2-4x the published benchmarks

Industry articles put garage door CPCs at $8-25. Reality in this market:

- **Average CPC across service-intent keywords: ${sum(cpcs)/len(cpcs):.2f}**
- **Highest: ${max(cpcs):.2f}** · Lowest: ${min(cpcs):.2f}
- Total monthly volume: **{sum(t[1] for t in table):,} searches in Conroe**,
  **{sum(t[2] for t in table):,} in Houston metro**

Any plan built on the $8-25 assumption is wrong.

### 3.2 The core opportunity — vocabulary arbitrage

The same customer costs radically different amounts depending on which words
they use. Someone typing "garage door sensor repair" has the same broken door
and the same wallet as someone typing "emergency garage door repair" — they just
know which part failed. National franchises bid the category vocabulary and
ignore the component vocabulary.

**Most expensive keywords (avoid or bid-cap):**

| Keyword | Houston vol | CPC |
|---|---:|---:|
""" + "\n".join(f"| {t[0]} | {t[2]} | ${t[3]:.2f} |" for t in dear) + f"""

**Cheapest service-intent keywords (the opportunity, CPC <= $10):**

| Keyword | Houston vol | CPC |
|---|---:|---:|
""" + "\n".join(f"| {t[0]} | {t[2]} | ${t[3]:.2f} |" for t in cheap[:20]) + f"""

This gap is why the account has a dedicated **Components & Symptoms** campaign.

### 3.3 Radius vs match type — how far to reach to spend a given budget

Google's own forecaster, 24 towns at increasing distance from Conroe:

| Radius | Exact @ $30 cap | Phrase @ $35 | Broad @ $60 |
|---|---:|---:|---:|
| Conroe only | $213 | $1,481 | $3,982 |
| 10 miles | $739 | $4,898 | $14,990 |
| 15 miles | $1,472 | $8,395 | $26,722 |
| 20 miles | $2,642 | $13,396 | $42,719 |
| 25 miles | $3,136 | $15,941 | $50,363 |
| 40 miles | $6,321 | $33,633 | $99,500 |
| 60 miles | $8,100 | $44,056 | $124,123 |

**Match type moves the number far more than geography.** Exact at a $30 cap never
reaches $10,000 — not even across the entire Houston metro. This drives two
decisions: the $10,000 plan uses phrase match at 25 miles; the $2,000 test uses
exact only at 25 miles, taking ~64% of available exact capacity.

Chasing Houston, Katy or Sugar Land for volume means longer drives, worse
margins, and a direct fight with A1 (see below). Not recommended.

### 3.4 Competitive position (Google Ads Transparency Center)

| Advertiser | Ads running | Type |
|---|---:|---|
| A1 Garage Door Service (TMII Enterprises) | ~2,000 | National; also owns Garage Door Doctor |
| Precision Garage Door Houston | ~200 | Franchise |
| Garage & Gate Service Pros | 44 | Regional |
| TJ's Garage Door Service (closest Conroe rival) | 1 | Local |

**The local operators are absent from paid search.** The auction is fought by
national franchises running generic multi-market copy. Nobody competes on being
*from Conroe* — which is the positioning every ad group leans on, and it is
defensible in a way outbidding a franchise is not.

A1 has acquired Garage Door Doctor, so one national operator now runs two brands
in The Woodlands. Expect their spend to rise.

### 3.5 Benchmarks from published sources

- Residential repair: $40-80 CPL on Search · cost per booked job $120-220
- Residential install: $110-220 CPL · cost per booked job $400-900
- Commercial overhead: $300-600 CPL · **45-90 day sales cycle**
- Non-brand garage door CPL measured at $173 across ten contractors
- Unprotected accounts waste 18-32% of spend on DIY, jobs, parts and decor searches

---

## 4. Full keyword dataset

{len(table)} unique keywords. `Match` shows what is bought: E = exact, P = phrase,
EP = both. Conroe and Houston columns are monthly searches. CPC is the Google Ads
estimate. Comp is competition index 0-100.

| Keyword | Conroe | Houston | CPC | Comp | Campaign | Ad group | Bid | Match |
|---|---:|---:|---:|---:|---|---|---:|---|
""" + "\n".join(lines) + f"""

Four keywords were cut for zero volume even in Houston metro:
`garage door company conroe tx`, `garage door company the woodlands`,
`garage door install conroe`, `garage door stuck half way`.

---

## 5. The campaign as built

### Full plan — $10,000/month, 6 campaigns, 240 keywords (122 exact + 118 phrase)

| Campaign | Monthly | Daily | Bid cap |
|---|---:|---:|---:|
| Head Terms | $5,200 | $171.05 | $30 |
| Install & Replace | $2,500 | $82.24 | $26 |
| Commercial & Gates | $900 | $29.61 | $40 |
| Components & Symptoms | $800 | $26.32 | $6-12 |
| Competitor | $400 | $13.16 | $8 |
| Brand | $200 | $6.58 | $3 |

Allocation is **efficiency-first, not proportional to auction size**. Sized
proportionally, Head Terms would take 85% of the budget — $8,500 buying roughly
17 leads. Cheap tiers are bought out first; Head Terms absorbs the remainder with
bids capped **below market on purpose** ($30 against a $40-46 average). Paying
$46 for a click to win a $40 job is a subsidy, not a strategy.

Expected: ~560 clicks/mo at a blended ~$18 -> 45-58 leads at $170-220 CPL ->
18-25 booked jobs at a 40% booking rate.

### The $2,000 test — 4 campaigns, exact match only, 60 days

| Campaign | Monthly | Daily |
|---|---:|---:|
| Head Terms | $1,000 | $32.89 |
| Components & Symptoms | $600 | $19.74 |
| Install & Replace | $300 | $9.87 |
| Brand | $100 | $3.29 |

**Not the full plan scaled down.** Scaled proportionally, four campaigns would
get 1-2 clicks a day and teach nothing. Two deliberate changes:

- **Exact match only.** At $2,000, exact capacity within 25 miles (~$3,136)
  means this takes ~64% of it — high impression share on keywords that matter,
  rather than a thin smear across phrase traffic. Also removes the daily
  search-term review phrase demands.
- **Commercial & Gates and Competitor excluded.** Commercial carries a 45-90 day
  sales cycle and cannot produce a readable result in 60 days at any budget.

Install & Replace at $300 buys ~12 clicks and perhaps one lead. It is a lottery
ticket, not a measurement — one booked install is worth more than the test costs.

Expected: ~164 clicks/mo, ~330 over 60 days -> 26-33 leads -> 10-13 booked jobs.
**Run 60 days, not 30.** At 30 days you get 5-6 jobs and the difference between
5 and 8 is noise.

### Decision thresholds (judge on cost per BOOKED JOB, not cost per lead)

| Cost per booked job | Decision |
|---|---|
| Under $350 | Scale to the $10,000 plan |
| $350-600 | Optimise, do not scale — something is leaking |
| Over $600 | Stop |

**These are provisional.** They assume a typical repair ticket and ~50% gross
margin. TML's actual average job value and margin are unknown (see section 7).

**Key diagnostic:** if cost per lead is fine but booking rate is under 25%, the
ads are working and the business is not — unanswered calls, slow callbacks, or
quoting. That is the most common misreading of a test like this and it kills
campaigns that were performing.

### Settings

- **Location:** 25-mile radius around Conroe, plus named towns as fallback.
  Set to **"Presence: people in your targeted locations"** — Google's default
  also includes people merely *interested* in the area, which for a local trade
  means paying for out-of-state clicks. Most expensive default in Google Ads.
- **Networks:** `Google Search` for the test (Search Partners off for clean
  data), `Google Search;Search Partners` for the full plan. **Display never.**
- **Bidding:** Manual CPC throughout the test. For the full plan: Manual weeks
  1-3, Maximize Conversions weeks 4-8 once calls track, Target CPA week 9+ only
  on campaigns clearing 30 conversions/month. Do not start on Smart Bidding —
  at these click volumes it has nothing to learn from.
- **Languages:** `en` (ISO code — Editor rejects `English`).

---

## 6. Guardrails and known traps

Mistakes already made and fixed. Do not reintroduce them.

1. **Negatives must be phrases, not words.** An early build stored them as
   space-separated text and split on whitespace, turning "entry door" and
   "home depot" into the negatives **"door"** and **"home"** — enough to block
   every keyword in the account.

2. **Never put a blanket `repair` negative on Install & Replace.** That campaign
   holds `chamberlain garage door opener repair` and three sibling brand
   keywords. A campaign-level `repair` negative silently switches all four off.

3. **`overhead door` must NOT be a commercial negative.** Components legitimately
   holds `overhead door torsion spring replacement` and `overhead door cable
   replacement`, and many Texas homeowners call a residential door an overhead
   door.

4. **Do not negative these**, despite appearances: `free` (blocks "free
   estimate", a buying search), `reviews` (blocks comparison shoppers),
   `license` (blocks "licensed garage door repair"), and `spring` / `houston` /
   `cypress` — real places TML serves.

5. **Commercial and gate traffic is fenced out of the three residential
   campaigns** via 29 campaign-level negatives (`commercial`, `warehouse`,
   `loading dock`, `rolling steel`, `roll up door`, `storefront`, `gate`,
   `driveway gate` and similar).

6. **Editor CSV formats that were wrong and are now fixed:** `Languages` needs
   `en` not `English`; `Networks` needs `Google Search` with a capital S — an
   unparsed value lets Editor default to a Search campaign that *includes*
   Display.

7. **168 shared negatives** in eight groups: DIY/how-to, jobs/training,
   parts/retail, design/decor, not-our-service, research/complaints,
   business/franchise, outside-service-area.

The generator validates before writing and refuses to produce files if any
negative blocks an active keyword, any keyword duplicates within a campaign, any
ad group lacks an ad, or any headline exceeds 30 characters / description 90.

---

## 7. Open questions — unresolved, and they matter

1. **Nine unconfirmed business facts:** prices, service-call fee, warranty terms,
   licence number, years in business, background-check status. These block both
   ad copy improvements and the Advanced Verification application.
2. **Average job value and gross margin** — needed to set the decision thresholds
   properly rather than provisionally.
3. **Google Ads account status** — verified? billing? conversion history?
4. **Google Business Profile** — claimed and verified?
5. **Call handling** — who answers, what hours, after-hours cover? Ad scheduling
   depends on it and is currently unset.
6. **Workiz shows no Saturday availability** while every ad and page promises no
   weekend surcharge. Contradiction must be resolved before launch.

---

## 8. Files

Repo: `~/GIT/tmlgarageservices/google-ads/`

| Path | What |
|---|---|
| `build_campaign.py` | Generates everything. `--test` for the $2,000 build |
| `import/00_FULL_IMPORT.csv` | Full $10,000 account, one file, 1,475 rows |
| `import-test/00_FULL_IMPORT.csv` | $2,000 test, 967 rows |
| `import/01-12_*.csv` | Same data split by entity type |
| `image-assets/` | 11 Search image assets (photographs — Google forbids overlaid text on these, so the 47 Meta creatives are ineligible) |
| `STRATEGY.md` | The full plan |
| `TEST-PLAN.md` | The $2,000 test |
| `IMPORT-INSTRUCTIONS.md` | Editor import steps and known warnings |
| `RECOMMENDATIONS-TRIAGE.md` | Google's in-account nudges, which to act on |
| `research/keyword_data.json` | Raw DataForSEO output behind section 4 |

Regenerate: `python3 build_campaign.py` and `python3 build_campaign.py --test`.

---

## 9. Two Google recommendations that were declined on purpose

- **Automated bidding.** No conversion history, no working conversion tracking,
  ~6 clicks/day on the biggest campaign. Target CPA needs ~30 conversions in 30
  days first.
- **Display Network expansion.** Lets a Search campaign spend budget on banner
  placements to people who are not searching. For an emergency trade whose value
  is catching someone whose door just broke, that is a different and worse
  customer. Note the phrase "unspent budget" in Google's wording — if a campaign
  is not spending, fix targeting or bids.

Declining both holds Optimization Score in the 70s. That is fine; it is not a
performance metric.
"""

(D / "CLAUDE-HANDOFF.md").write_text(doc, "utf-8")
print(f"CLAUDE-HANDOFF.md — {len(doc):,} chars, {len(table)} keywords in the table")
