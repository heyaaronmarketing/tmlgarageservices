# TML Garage Door Services — Google Ads lead generation strategy
$10,000/month · **Search only**

Local Services Ads is deliberately excluded. Everything below assumes the whole
budget runs through Search. LSA notes are parked in Appendix A.

---

## 1. Three things that must be true before you spend anything

### 1.1 Advanced Verification — hard gate, start today

Garage door services is one of only two categories worldwide (the other is
locksmiths) that Google singles out for **Advanced Verification**. Until TML
passes, **no Search campaign runs at all.** Not throttled — it does not serve.

Google requires the true legal business name or registered DBA, business
registration, government ID, licence documentation where applicable,
photographs of the premises, vehicles and tools, and **a video interview
conducted by Google**. Re-verification every 12 months, and an expired insurance
certificate stops delivery immediately.

### 1.2 The site has to be the one people land on

The campaign points at `www.tmlgarageservices.com/…`. The repaired site is still
at `/fixed/` on the staging worker under a sitewide `noindex`. Ads will serve to
a noindexed page, but sending paid clicks to the un-repaired mirror wastes them.

### 1.3 Conversion tracking is currently impossible

Both conversion points are **cross-origin iframes** — the booking widget
(`online-booking.workiz.com`) and the contact form (`st.sendajob.com`). A browser
will not let the parent page see inside either. **Google Ads cannot record a
booking or a form fill.**

Calls can be tracked via Google forwarding numbers and click-to-call. That is
about half the picture, and it means any later move to Smart Bidding would be
optimising on partial data.

**Fix:** two dedicated PPC landing pages with a *native* form posting to a
Cloudflare Worker, forwarding to Workiz or email and redirecting to a real
thank-you URL. Trackable conversion, faster page, message match with the ad.
About one day of work.

---

## 2. The competitive position

All twenty local competitors, checked in Google's Ads Transparency Center:

| Advertiser | Ads running | Type |
|---|---:|---|
| A1 Garage Door Service (TMII Enterprises) | **~2,000** | National; also owns Garage Door Doctor |
| Precision Garage Door Houston | ~200 | Franchise |
| Garage & Gate Service Pros | 44 | Regional |
| **TJ's Garage Door Service** — closest Conroe rival | **1** | Local |

**The local operators are absent from paid search.** The auction is fought by
national franchises running generic multi-market copy. Nobody is competing on
being *from Conroe* — defensible in a way outbidding a franchise is not.

A1 has bought Garage Door Doctor, so one national operator now runs two brands
in The Woodlands. Their spend will rise.

---

## 3. What the market data says

Real volume and CPC from DataForSEO, Conroe and Houston.

### 3.1 Clicks cost 2–4× the published benchmarks

| Keyword | Conroe/mo | Houston/mo | CPC |
|---|---:|---:|---:|
| garage door repair | 170 | 2,400 | **$40.68** |
| garage door repair near me | 170 | 2,900 | **$46.40** |
| garage door company near me | 20 | 210 | **$73.69** |
| garage door conroe | 20 | 10 | **$97.22** |
| emergency garage door repair | — | 70 | **$106.26** |

Average across service-intent keywords: **$38.39**. Peak: **$178.93**. Every
guide claiming $8–25 is wrong for this market.

### 3.2 The gap: the same customer costs 45× less depending on vocabulary

| What they type | Volume | CPC |
|---|---:|---:|
| emergency garage door repair | 70 | $106.26 |
| **garage door sensor repair** | 210 | **$2.35** |
| garage door repair company | 110 | $92.22 |
| **garage door cable replacement** | 40 | **$1.40** |
| garage door spring repair cost | 70 | $51.41 |
| **garage door torsion spring replacement** | 70 | **$4.32** |
| garage door installation | 390 | $29.47 |
| **garage door installation near me** | 480 | **$4.18** |

Someone typing "garage door sensor repair" has the same broken door and the same
wallet as someone typing "emergency garage door repair" — they just know which
part failed. The franchises bid the category vocabulary and ignore the component
vocabulary.

From 5,174 mined keywords, **27 have real service intent under $10 a click** —
2,030 searches a month averaging **$3.40**. That is its own campaign tier. Four
turned out to be competitor brand names at $0.48–$6.21; bidding on those is
permitted, but **naming a competitor in ad text is trademark infringement**, so
they sit in their own campaign and no copy names anyone.

### 3.3 How far you must reach to spend $10,000

Google's forecaster, 24 towns at increasing distance from Conroe:

| Radius | Exact @ $30 cap | Phrase @ $35 | Broad @ $60 |
|---|---:|---:|---:|
| Conroe only | $213 | $1,481 | $3,982 |
| 10 miles | $739 | $4,898 | **$14,990** |
| 15 miles | $1,472 | $8,395 | $26,722 |
| **20 miles** | $2,642 | **$13,396** | $42,719 |
| **25 miles** | $3,136 | **$15,941** | $50,363 |
| 40 miles | $6,321 | $33,633 | $99,500 |
| 60 miles | **$8,100** | $44,056 | $124,123 |

**Match type moves the number far more than geography.** Exact at a $30 cap never
reaches $10,000 — not across every town within 60 miles, the entire Houston
metro. Ceiling: $8,100.

**The plan: a 25-mile radius, phrase match.** Forecasts **$15,900 of capacity
against a $10,000 target — about 60% headroom.** Covers Willis, Shenandoah, Oak
Ridge North, The Woodlands, Montgomery, Magnolia, Spring, New Caney, Splendora,
Porter and Tomball: the area TML already claims. No reason to chase Houston,
Katy or Sugar Land — longer drives, worse margins, a direct fight with A1.

**The catch.** Phrase buys reach by loosening what matches. The 168 negatives
matter far more here than under exact. Budget for search-term review — daily for
the first fortnight, weekly after — and expect the list past 250 within two
months. If nobody will do that, run exact and accept the $8,000 ceiling.

---

## 4. Where the $10,000 goes

Efficiency-first, not proportional to auction size. Proportionally, Head Terms
would take 85% — $8,500 buying about 17 leads. Instead cheap tiers are bought
out first and Head Terms absorbs the rest, bid-capped.

| Campaign | Monthly | Daily | Bid cap | Why |
|---|---:|---:|---:|---|
| Head Terms | $5,200 | $171.05 | $30 | Most volume, worst prices. Capped below the $40–46 market |
| Install & Replace | $2,500 | $82.24 | $26 | High ticket |
| Commercial & Gates | $900 | $29.61 | $40 | Low volume, $1,800–4,500 a booked job |
| Components & Symptoms | $800 | $26.32 | $6–12 | The $3.40 gap |
| Competitor | $400 | $13.16 | $8 | Cheap clicks from people already shopping |
| Brand | $200 | $6.58 | $3 | Defence |
| **Total** | **$10,000** | **$328.96** | | |

Head-term bids are capped **below market on purpose**. Paying $46 for a click to
win a $40 job is a subsidy, not a strategy.

### Honest expectations

~560 clicks a month at a blended ~$18 → **45–58 leads at $170–220 CPL**, and
**18–25 booked jobs** at a 40% booking rate. That sits on the $173 non-brand
benchmark measured across ten garage door contractors, slightly worse because
Houston is expensive.

**What excluding LSA costs, said once.** Local Services leads run $25–50 against
$170–220 here, so the same $10,000 buys roughly a third of the leads it would
have with LSA sharing the load. Reasonable trade while LSA is unproven; nothing
here depends on it.

**If you would rather not commit $10,000 unproven:** start at **$4,000** —
Components, Commercial, Competitor and Brand in full plus $1,700 of Head Terms —
and scale once cost per booked job is real.

---

## 5. Campaign structure

Six campaigns, 18 ad groups, **240 keywords** — 122 exact, 118 phrase. No broad
match until conversion data can steer it. Brand and Competitor stay exact-only.

Repair, install and commercial are kept apart because their cost per lead differs
by a factor of ten, and blending them lets bidding chase cheap residential volume
at the expense of the commercial jobs that pay best.

Four keywords were cut for **zero volume even in Houston metro**:
`garage door company conroe tx`, `garage door company the woodlands`,
`garage door install conroe`, `garage door stuck half way`.

### Negatives

**168 shared negatives** in eight groups. Industry sources put unprotected waste
in this vertical at 18–32%.

Two bugs were caught during the build, both expensive:

1. Negatives stored as space-separated text and split on whitespace turned
   "entry door" and "home depot" into the negatives **"door"** and **"home"** —
   enough to block every keyword in the account.
2. A campaign-level `repair` negative on Install & Replace would have silently
   switched off all four brand-opener keywords living in that campaign.

`build_campaign.py` now refuses to write the files if any negative blocks an
active keyword, any keyword duplicates within a campaign, or any ad group lacks
an ad.

Deliberately **not** negatives: `free` (blocks "free estimate"), `reviews`
(blocks comparison shoppers), `license` (blocks "licensed garage door repair"),
and `spring` / `houston` / `cypress` — real places served.

**Commercial and gate work is fenced out of the residential campaigns.** Head
Terms, Components & Symptoms and Install & Replace carry commercial negatives —
`commercial`, `warehouse`, `loading dock`, `rolling steel`, `roll up door`,
`storefront`, `gate`, `driveway gate` and similar — so those searches land in
Commercial & Gates, where the $40 bid and the matching landing page belong,
rather than being bought at a residential bid against a residential page.

`overhead door` is deliberately **not** among them: Components holds "overhead
door torsion spring replacement" and "overhead door cable replacement", and many
Texas homeowners call a residential door an overhead door.

### Targeting

One **25-mile radius around Conroe**, plus the named towns as fallback. A radius
catches the unincorporated gaps between them, which is most of Montgomery County.

**Set location targeting to "Presence: people in your targeted locations."**
Google's default also includes people merely *interested* in the area — for a
local service that means paying for clicks from other states.

---

## 6. Bidding — do not start on Smart Bidding

Head Terms at $171/day and a $30 CPC is about six clicks a day. Target CPA needs
roughly 30 conversions in 30 days before it has anything to learn from.

| Weeks | Strategy |
|---|---|
| 1–3 | **Manual CPC (enhanced)**. Search-term review daily; add negatives aggressively. |
| 4–8 | **Maximize Conversions**, once call tracking is confirmed firing. |
| 9+ | **Target CPA** on campaigns clearing 30 conversions/month. Pool Head Terms and Components into one portfolio strategy. |

Commercial, Competitor and Brand stay Manual CPC indefinitely — too little volume
to train an algorithm.

---

## 7. Ad copy: what is in, and what is held back

Every claim is one the TML site already makes: same-day appointments, weekend
appointments at no extra charge, trained and insured technicians, full price
quoted before work starts, and the service area.

Five lines are **held back** pending fact-checks — `import/12_copy_held_back.csv`:

| Copy | Why it is not running |
|---|---|
| `$69 Garage Door Tune-Up` | On the site, not in the verified facts. Google requires offer terms and limitations alongside a price. |
| `5.0 From 213 Google Reviews` | Must match the live Business Profile on the day it runs. |
| `Licensed, Bonded & Insured` | No licence or bond number on file. |
| `Family Owned Since 20XX` | Years in business unknown. |
| `Angi Super Service Award` | The award on the site is dated 2019. |

---

## 8. What I still need from you

1. **The nine unconfirmed business facts** — prices, service-call fee, warranty
   terms, licence number, years in business, background-check status. They feed
   the ad copy *and* the Advanced Verification application.
2. **Google Ads account status** — verified? billing set up? conversion history?
3. **Google Business Profile** — claimed and verified?
4. **Call handling** — who answers, what hours, any after-hours cover? Ad
   scheduling depends on it.
5. **Workiz Saturday availability** — still none, while every ad and page
   promises no weekend surcharge. Fix it or drop the claim.

---

## Appendix A — Local Services Ads (parked)

Not part of this playbook. Kept because the diagnosis is done and the budget can
be rebalanced toward it in an afternoon.

**Why the budget would not spend, in likelihood order:**

1. **Check impressions first.** Zero impressions is a delivery problem; no budget
   or bid change touches it.
2. **Advanced Verification** — the same gate as Search. Incomplete verification,
   or an expired insurance certificate, leaves a budget that can never spend.
3. **Job types not switched on.** Google does not infer services from your site
   or Business Profile. Any job type not explicitly toggled on makes you invisible
   for those searches regardless of bid or reviews.
4. **Reviews** — roughly five needed before LSA populates at all. Confirm the 213
   sit on the Business Profile *linked to the LSA account*.
5. **Hours, service area, bid mode, weekly budget.** LSA budgets are weekly.
   Switch manual bidding to Maximize Leads.
6. **Responsiveness** — Google throttles delivery for businesses that miss calls.
7. **It may be demand.** Conroe generates ~1,800 relevant searches a month. At
   $35 a lead, $4,000/month implies ~114 leads from those 1,800 — not plausible
   for one advertiser in one town. If revived, LSA needs the same 25-mile
   footprint as Search.
