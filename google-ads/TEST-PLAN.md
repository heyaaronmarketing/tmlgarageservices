# TML Google Ads — $2,000 lead test

Files: `import-test/` · build with `python3 build_campaign.py --test`

**$2,000/month · $65.79/day · 4 campaigns · 102 keywords · run for 60 days**

---

## Why this is not the $10,000 plan scaled down

Scaled proportionally, four of the six campaigns would receive one or two clicks
a day. At the end of a month you would have a handful of clicks spread across
everything and no basis to decide anything. A test budget has to buy
**concentration**, not coverage.

Two decisions follow from that.

### Exact match only

The $10,000 plan uses phrase match because exact tops out around $8,100 a month
across the whole Houston metro and cannot absorb $10,000. At $2,000 that ceiling
stops mattering: exact capacity within 25 miles is about **$3,136/month**, so
$2,000 takes roughly **64% of it**.

That is the difference between being reliably present on the keywords that matter
and being thinly spread across loose traffic. It also removes the daily
search-term review phrase match demands — which matters if nobody has capacity
for that yet.

The question this test answers is *"do these leads exist and convert at a price
that works"*, not *"can we win a loose auction"*.

### Four campaigns, not six

**Commercial & Gates and Competitor are excluded.**

Commercial leads cost $300–600 each and carry a **45–90 day sales cycle**. It
cannot produce a readable result in 60 days at any budget, and at $2,000 it would
consume a fifth of the money to deliver perhaps two enquiries that close after the
test has ended. Competitor traffic is a nice-to-have, not a lead test.

Both stay in the main build, ready for the scale-up.

---

## The allocation

| Campaign | Monthly | Daily | Why it is in the test |
|---|---:|---:|---|
| Head Terms | $1,000 | $32.89 | The core question — do the expensive keywords pay? |
| Components & Symptoms | $600 | $19.74 | Cheapest clicks, so most data per dollar |
| Install & Replace | $300 | $9.87 | A lottery ticket, not a measurement — see below |
| Brand | $100 | $3.29 | Cheap, and stops competitors buying the name mid-test |
| **Total** | **$2,000** | **$65.79** | |

**On Install & Replace, honestly:** $300 a month buys about 12 clicks and perhaps
one lead. That is not a measurement of anything. It is in because a single booked
installation is worth more than the entire test costs, and leaving it out means
guaranteeing zero. Treat any install lead as a bonus, not a data point.

---

## What to expect

About **164 clicks a month**, so roughly **330 across 60 days**. At an 8–10%
conversion rate that is **26–33 leads**, and at a 40% booking rate **10–13 booked
jobs**.

Which puts cost per booked job somewhere around **$300–400** if things go well.

**This is why the test runs 60 days, not 30.** At 30 days you get 13–16 leads and
5–6 jobs. The difference between 5 jobs and 8 jobs is noise, and you would be
making a $10,000 decision on it. Sixty days and $4,000 gets you to a number you
can actually trust.

---

## Decision thresholds

Judge on **cost per booked job**, not cost per lead. A cheap lead that nobody
books is worth nothing.

| Cost per booked job | Decision |
|---|---|
| **Under $350** | **Scale.** Move to the $10,000 plan, add phrase match and the two parked campaigns |
| **$350–600** | **Optimise, do not scale.** The demand is real but something is leaking — search terms, landing page, or call handling |
| **Over $600** | **Stop.** Either the market is too expensive for this model, or the problem is not the ads |

**Caveat you should close before relying on these numbers:** they assume a
typical repair ticket and roughly 50% gross margin. Nobody has confirmed TML's
actual average job value or margin — it is one of the nine unknown business
facts. Give me the real figures and I will set the thresholds against them
properly. Until then, treat the table as directional.

### The diagnostic that matters most

If cost per lead is fine but **booking rate is under 25%**, the ads are working
and the business is not. That points at unanswered calls, slow callbacks, or
quoting. Do not conclude the ads failed — that is the most common misreading of a
test like this, and it kills campaigns that were performing.

---

## What would invalidate the test

Fix all four before spending a pound:

1. **No conversion tracking.** $4,000 spent with nothing counting leads teaches
   you nothing. Google forwarding numbers on the call assets are the minimum.
   Both site forms are cross-origin iframes and cannot be tracked as they stand.
2. **Advanced Verification not approved.** Nothing serves at all.
3. **Traffic landing on the un-repaired mirror.** The site must be cut over.
4. **Nobody answering the phone.** Google throttles nothing here, but you will
   simply lose the leads you paid for, and the test will read as a failure.

---

## Operating rhythm

Exact match needs far less babysitting than phrase. Realistically:

- **Week 1:** check search terms twice. Even exact match matches close variants —
  synonyms and reworded queries — so a few negatives will still be needed.
- **Weeks 2–8:** search terms once a week. Log every lead and whether it booked.
- **Do not touch bids for the first three weeks.** Changing them resets what you
  are measuring.
- **Stay on Manual CPC the whole way.** At 164 clicks a month there will never be
  enough conversions for Smart Bidding to learn from. Do not let the
  recommendation nag you into it mid-test.

---

## What this test will not tell you

Worth being clear so the result is not over-read:

- **Commercial and gate work** — excluded entirely
- **Install at volume** — $300 a month is not a sample
- **Phrase-match performance** — deliberately untested; it is how you add volume
  *after* exact is proven
- **Whether $10,000 is deployable** — the radius analysis says yes at 25 miles
  with phrase match, but this test does not verify it

A pass here means *the core repair keywords produce bookable work at an
acceptable price*. That is the right thing to establish first, and everything
else builds on it.

---

## Importing

Same process as the full campaign — see `IMPORT-INSTRUCTIONS.md` — but point at
`import-test/00_FULL_IMPORT.csv` (874 rows). Everything imports paused.

If the full $10,000 campaign is already loaded in the account, do not import this
on top of it. Either start from a clean account, or pause Commercial and
Competitor and edit the four remaining budgets by hand to match the table above.
