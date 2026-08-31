# TML Garage Door Services — Google Ads brief

Self-contained handoff. Everything needed to fine-tune this campaign without prior context. Data pulled 25 Aug 2026.
prior context. Written 25 Aug 2026.

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

- **Average CPC across service-intent keywords: $24.63**
- **Highest: $156.85** · Lowest: $0.28
- Total monthly volume: **1,860 searches in Conroe**,
  **15,210 in Houston metro**

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
| roll up door repair | 10 | $156.85 |
| garage door repair tomball tx | 30 | $131.24 |
| garage door repair montgomery tx | 10 | $86.81 |
| warehouse door repair | 10 | $71.99 |
| 24 hour garage door repair | 10 | $69.99 |
| garage door won't open | 30 | $61.29 |
| garage door wont open | 30 | $61.29 |
| garage door tune up | 40 | $55.95 |
| commercial door repair near me | 30 | $55.71 |
| garage door repair the woodlands | 30 | $54.44 |
| new garage door installation | 10 | $52.97 |
| broken garage door spring | 110 | $49.99 |

**Cheapest service-intent keywords (the opportunity, CPC <= $10):**

| Keyword | Houston vol | CPC |
|---|---:|---:|
| garage door opener repair | 1900 | $1.42 |
| insulated garage door | 590 | $1.25 |
| garage door installation near me | 480 | $4.18 |
| garage door installers near me | 480 | $4.18 |
| garage door opener installation | 390 | $5.39 |
| fix garage door sensor | 210 | $2.35 |
| garage door replacement | 210 | $5.90 |
| garage door replacement cost | 210 | $2.19 |
| garage door sensor repair | 210 | $2.35 |
| replace garage door | 210 | $5.90 |
| garage door panel replacement | 110 | $5.92 |
| modern garage doors | 110 | $1.35 |
| garage door opener replacement | 90 | $6.10 |
| garage door roller replacement | 70 | $6.92 |
| garage door service master | 70 | $5.09 |
| garage door torsion spring replacement | 70 | $4.32 |
| garage torsion spring replacement | 70 | $4.32 |
| new garage door | 70 | $6.74 |
| overhead door torsion spring replacement | 70 | $4.32 |
| pro garage door repair | 70 | $0.48 |

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

125 unique keywords. `Match` shows what is bought: E = exact, P = phrase,
EP = both. Conroe and Houston columns are monthly searches. CPC is the Google Ads
estimate. Comp is competition index 0-100.

| Keyword | Conroe | Houston | CPC | Comp | Campaign | Ad group | Bid | Match |
|---|---:|---:|---:|---:|---|---|---:|---|
| garage door repair near me | 170 | 2900 | $28.83 | 47 | Head Terms | Repair Core | $24.00 | EP |
| garage door repair | 170 | 2400 | $19.28 | 49 | Head Terms | Repair Core | $24.00 | EP |
| garage door opener repair | 140 | 1900 | $1.42 | 13 | Head Terms | Repair Core | $24.00 | EP |
| insulated garage door | 70 | 590 | $1.25 | 100 | Install & Replace | Door Types | $6.40 | EP |
| garage door installation near me | 10 | 480 | $4.18 | 16 | Components & Symptoms | Install Near Me | $6.40 | EP |
| garage door installers near me | 10 | 480 | $4.18 | 16 | Install & Replace | New Door Install | $20.80 | EP |
| garage door installation | 50 | 390 | $34.49 | 27 | Install & Replace | New Door Install | $20.80 | EP |
| garage door opener installation | 20 | 390 | $5.39 | 48 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| garage door spring repair | 10 | 260 | $16.72 | 14 | Head Terms | Springs Head | $24.00 | EP |
| garage door spring replacement | 10 | 260 | $16.72 | 14 | Head Terms | Springs Head | $24.00 | EP |
| fix garage door sensor | 20 | 210 | $2.35 | 15 | Components & Symptoms | Sensors & Safety | $4.80 | EP |
| garage door repair service | 20 | 210 | $41.87 | 26 | Head Terms | Repair Core | $24.00 | EP |
| garage door replacement | 30 | 210 | $5.90 | 34 | Install & Replace | New Door Install | $20.80 | EP |
| garage door replacement cost | 10 | 210 | $2.19 | 43 | Install & Replace | New Door Install | $20.80 | EP |
| garage door sensor repair | 20 | 210 | $2.35 | 15 | Components & Symptoms | Sensors & Safety | $4.80 | EP |
| replace garage door | 30 | 210 | $5.90 | 34 | Install & Replace | New Door Install | $20.80 | EP |
| garage door service | 20 | 170 | $30.36 | 27 | Head Terms | Repair Core | $24.00 | EP |
| liftmaster garage door opener installation | 10 | 140 | $0.00 | 1 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| broken garage door spring | 10 | 110 | $49.99 | 67 | Head Terms | Springs Head | $24.00 | EP |
| chamberlain garage door opener repair | 10 | 110 | $0.00 | 15 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| garage door panel replacement | 10 | 110 | $5.92 | 89 | Components & Symptoms | Rollers Tracks Panels | $7.20 | EP |
| garage door spring broke | 10 | 110 | $49.99 | 67 | Head Terms | Springs Head | $24.00 | EP |
| genie garage door opener repair | 10 | 110 | $0.00 | 5 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| modern garage doors | 10 | 110 | $1.35 | 100 | Install & Replace | Door Types | $6.40 | EP |
| garage door opener replacement | 10 | 90 | $6.10 | 79 | Components & Symptoms | Opener Mechanics | $7.20 | EP |
| garage door repair spring tx | 10 | 90 | $27.18 | 59 | Head Terms | Local Towns | $20.80 | EP |
| commercial garage door repair | 10 | 70 | $34.55 | 46 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| commercial overhead door repair | 10 | 70 | $34.55 | 46 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| craftsman garage door opener repair | 10 | 70 | $0.00 | 7 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| garage door maintenance | 10 | 70 | $35.76 | 59 | Head Terms | Tune Up | $11.20 | EP |
| garage door roller replacement | 10 | 70 | $6.92 | 82 | Components & Symptoms | Rollers Tracks Panels | $7.20 | EP |
| garage door service master | 10 | 70 | $5.09 | 20 | Competitor | Competitor Brands | $8.00 | E |
| garage door torsion spring replacement | 10 | 70 | $4.32 | 44 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| garage torsion spring replacement | 10 | 70 | $4.32 | 44 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| gate opener repair | 10 | 70 | $15.13 | 23 | Commercial & Gates | Gates | $16.00 | EP |
| new garage door | 10 | 70 | $6.74 | 100 | Install & Replace | New Door Install | $20.80 | EP |
| new garage door cost | 10 | 70 | $11.17 | 93 | Install & Replace | New Door Install | $20.80 | EP |
| overhead door repair | 10 | 70 | $44.16 | 20 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| overhead door torsion spring replacement | 10 | 70 | $4.32 | 44 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| pro garage door repair | 10 | 70 | $0.48 | 4 | Competitor | Competitor Brands | $8.00 | E |
| same day garage door repair | 10 | 70 | $15.73 | 49 | Head Terms | Emergency Capped | $17.60 | EP |
| driveway gate repair | 10 | 50 | $11.83 | 48 | Commercial & Gates | Gates | $16.00 | EP |
| garage door bottom seal replacement | 10 | 50 | $0.36 | 100 | Components & Symptoms | Rollers Tracks Panels | $7.20 | EP |
| garage door opener repair near me | 10 | 50 | $47.14 | 96 | Head Terms | Repair Core | $24.00 | EP |
| garage door sensor replacement | 10 | 50 | $0.57 | 74 | Components & Symptoms | Sensors & Safety | $4.80 | EP |
| commercial garage door repair near me | 10 | 40 | $7.50 | 15 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| commercial gate repair | 10 | 40 | $28.68 | 86 | Commercial & Gates | Gates | $16.00 | EP |
| custom garage doors | 10 | 40 | $2.79 | 92 | Install & Replace | Door Types | $6.40 | EP |
| electric gate repair | 10 | 40 | $47.27 | 38 | Commercial & Gates | Gates | $16.00 | EP |
| garage door cable repair | 10 | 40 | $11.15 | 16 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| garage door cable replacement | 10 | 40 | $21.48 | 84 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| garage door off track | 10 | 40 | $0.00 | 51 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door spring repair near me | 10 | 40 | $0.00 | 12 | Head Terms | Springs Head | $24.00 | EP |
| garage door tune up | 10 | 40 | $55.95 | 79 | Head Terms | Tune Up | $11.20 | EP |
| garage door wire replacement | 10 | 40 | $21.48 | 84 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| overhead door cable replacement | 10 | 40 | $21.48 | 84 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| speedy garage door repair | 10 | 40 | $1.62 | 59 | Competitor | Competitor Brands | $8.00 | E |
| automatic gate installation | 10 | 30 | $0.00 | 36 | Commercial & Gates | Gates | $16.00 | EP |
| automatic gate repair | 10 | 30 | $8.31 | 47 | Commercial & Gates | Gates | $16.00 | EP |
| carriage garage doors | 10 | 30 | $3.15 | 100 | Install & Replace | Door Types | $6.40 | EP |
| commercial door repair near me | 10 | 30 | $55.71 | 45 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| garage door motor replacement | 10 | 30 | $9.32 | 84 | Components & Symptoms | Opener Mechanics | $7.20 | EP |
| garage door opener not working | 10 | 30 | $17.19 | 71 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door repair the woodlands | 30 | 30 | $54.44 | 44 | Head Terms | Local Towns | $20.80 | EP |
| garage door repair tomball tx | 10 | 30 | $131.24 | 100 | Head Terms | Local Towns | $20.80 | EP |
| garage door track repair | 10 | 30 | $0.00 | 2 | Components & Symptoms | Rollers Tracks Panels | $7.20 | EP |
| garage door won't close | 10 | 30 | $11.14 | 70 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door won't open | 10 | 30 | $61.29 | 67 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door wont close | 10 | 30 | $11.14 | 70 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door wont open | 10 | 30 | $61.29 | 67 | Components & Symptoms | Symptoms | $9.60 | EP |
| commercial garage door installation | 10 | 20 | $0.00 | 3 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| elite garage door repair | 10 | 20 | $6.21 | 90 | Competitor | Competitor Brands | $8.00 | E |
| garage door belt replacement | 10 | 20 | $4.47 | 81 | Components & Symptoms | Opener Mechanics | $7.20 | EP |
| garage door drive belt replacement | 10 | 20 | $4.47 | 81 | Components & Symptoms | Opener Mechanics | $7.20 | EP |
| garage door hinge replacement | 10 | 20 | $0.28 | 100 | Components & Symptoms | Rollers Tracks Panels | $7.20 | EP |
| garage door repair conroe | 70 | 20 | $40.30 | 41 | Head Terms | Local Towns | $20.80 | EP |
| garage door track replacement | 10 | 20 | $1.67 | 58 | Components & Symptoms | Rollers Tracks Panels | $7.20 | EP |
| gate motor repair | 10 | 20 | $1.94 | 17 | Commercial & Gates | Gates | $16.00 | EP |
| new garage door opener | 10 | 20 | $11.81 | 84 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| replace garage door lock | 10 | 20 | $0.30 | 91 | Components & Symptoms | Opener Mechanics | $7.20 | EP |
| 24 hour garage door repair | 10 | 10 | $69.99 | 14 | Head Terms | Emergency Capped | $17.60 | EP |
| after hours garage door repair | 0 | 10 | $0.00 | 0 | Head Terms | Emergency Capped | $17.60 | EP |
| double garage door replacement | 0 | 10 | $0.00 | 0 | Install & Replace | Door Types | $6.40 | EP |
| driveway gate installation | 10 | 10 | $0.00 | 46 | Commercial & Gates | Gates | $16.00 | EP |
| garage door cable off drum | 0 | 10 | $0.00 | 0 | Components & Symptoms | Springs & Cables | $6.40 | EP |
| garage door came off track | 10 | 10 | $0.00 | 61 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door conroe | 20 | 10 | $17.07 | 79 | Head Terms | Local Towns | $20.80 | EP |
| garage door crooked | 10 | 10 | $0.00 | 11 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door hinge repair | 10 | 10 | $0.00 | 0 | Components & Symptoms | Rollers Tracks Panels | $7.20 | EP |
| garage door inspection | 10 | 10 | $0.00 | 14 | Head Terms | Tune Up | $11.20 | EP |
| garage door lubrication service | 0 | 10 | $0.00 | 0 | Head Terms | Tune Up | $11.20 | EP |
| garage door making noise | 10 | 10 | $0.00 | 57 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door not working | 10 | 10 | $0.00 | 77 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door off track repair | 10 | 10 | $0.00 | 0 | Components & Symptoms | Symptoms | $12.00 | P |
| garage door opener wont work | 10 | 10 | $0.00 | 29 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door repair conroe tx | 30 | 10 | $48.55 | 63 | Head Terms | Local Towns | $20.80 | EP |
| garage door repair magnolia tx | 10 | 10 | $35.07 | 58 | Head Terms | Local Towns | $20.80 | EP |
| garage door repair montgomery tx | 10 | 10 | $86.81 | 0 | Head Terms | Local Towns | $20.80 | EP |
| garage door repair open now | 0 | 10 | $0.00 | 57 | Head Terms | Emergency Capped | $17.60 | EP |
| garage door repair the woodlands tx | 10 | 10 | $31.14 | 44 | Head Terms | Local Towns | $20.80 | EP |
| garage door repair today | 0 | 10 | $0.00 | 100 | Head Terms | Emergency Capped | $17.60 | EP |
| garage door repair willis tx | 10 | 10 | $20.12 | 74 | Head Terms | Local Towns | $20.80 | EP |
| garage door safety inspection | 0 | 10 | $0.00 | 0 | Head Terms | Tune Up | $11.20 | EP |
| garage door safety sensor replacement | 10 | 10 | $0.00 | 0 | Components & Symptoms | Sensors & Safety | $4.80 | EP |
| garage door stuck | 10 | 10 | $26.69 | 48 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door stuck open | 10 | 10 | $0.00 | 74 | Components & Symptoms | Symptoms | $9.60 | EP |
| garage door tune up near me | 10 | 10 | $41.89 | 92 | Head Terms | Tune Up | $11.20 | EP |
| gate operator repair | 10 | 10 | $0.00 | 16 | Commercial & Gates | Gates | $16.00 | EP |
| glass garage door installation | 0 | 10 | $0.00 | 0 | Install & Replace | Door Types | $6.40 | EP |
| insulated garage door installation | 10 | 10 | $0.00 | 0 | Install & Replace | Door Types | $8.00 | P |
| liftmaster dealer near me | 10 | 10 | $25.05 | 100 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| loading dock door repair | 0 | 10 | $0.00 | 0 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| new garage door installation | 10 | 10 | $52.97 | 45 | Install & Replace | New Door Install | $20.80 | EP |
| roll up door repair | 10 | 10 | $156.85 | 71 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| rolling steel door repair | 0 | 10 | $0.00 | 0 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| smart garage door opener installation | 10 | 10 | $0.00 | 1 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| steel garage door installation | 10 | 10 | $0.00 | 0 | Install & Replace | Door Types | $6.40 | EP |
| tml garage door services | 10 | 10 | $46.88 | 49 | Brand | TML Brand | $3.00 | E |
| tml garage services | 10 | 10 | $0.00 | 54 | Brand | TML Brand | $3.00 | E |
| wall mount garage door opener installation | 10 | 10 | $0.00 | 0 | Install & Replace | Opener Install & Brands | $12.80 | EP |
| warehouse door repair | 0 | 10 | $71.99 | 100 | Commercial & Gates | Commercial Overhead | $32.00 | EP |
| weekend garage door repair | 0 | 10 | $0.00 | 0 | Head Terms | Emergency Capped | $17.60 | EP |
| wood garage door installation | 10 | 10 | $0.00 | 0 | Install & Replace | Door Types | $6.40 | EP |
| tml garage door | 0 | 0 | $0.00 | 0 | Brand | TML Brand | $3.00 | P |
| tml garage door conroe | 0 | 0 | $0.00 | 0 | Brand | TML Brand | $3.00 | E |

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
