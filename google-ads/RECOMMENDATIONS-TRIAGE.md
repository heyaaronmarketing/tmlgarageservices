# Google's recommendations — what to act on

Optimization Score is Google's own metric, and several of the things that raise
it also raise Google's revenue. Some of these are worth doing; two should be
declined on purpose.

---

## 1. EU political ads — **blocking**

> "You can't post your campaign until you confirm if your campaign has EU
> political ads."

A hard block, and **web-UI only** — it cannot be declared from Google Ads Editor,
which is where that error comes from ("post" is Editor's word).

The menu location differs between account layouts, in order of reliability:

1. **Campaigns > tick the campaigns > Edit > "Confirm EU setting."**
2. **Admin > Account settings** — look for *EU political ads* or *Political
   content*. On older layouts, **Settings > Account settings**. Declaring here
   covers all six campaigns and any future one.
3. **If neither menu looks right:** type **political** into the search box at the
   top of Google Ads. It indexes settings pages, not just campaigns, and jumps
   straight there whichever navigation version the account is on.
4. During new campaign setup it also appears under *Audience controls >
   Geographic location > EU Political Ads*.

Then in Editor: **Account > Get recent changes** — not a full re-download, which
would discard unposted work — and post again.

TML is a Conroe garage door company, so the answer is plainly no. It blocks
rather than nags because the deadline for existing campaigns was 31 March 2026.

---

## 2. Manual bidding → automated — **decline, for now**

Manual CPC is deliberate and should stay for three weeks.

Smart Bidding learns from conversions. This account has none — no history, and
tracking is not wired up because both forms are cross-origin iframes. Head Terms
at $171/day and a $30 cap is about six clicks a day; Target CPA wants ~30
conversions in 30 days first. Switching now means Google spends real money
guessing.

Ramp: Manual CPC weeks 1–3, Maximize Conversions weeks 4–8 once calls are
tracking, Target CPA from week 9 on campaigns clearing 30 conversions a month.

---

## 3. Fewer than 3 image assets — **fixed, 11 built**

In `image-assets/`. Upload under Assets > Images.

Five subjects — crew and truck, technician fitting a LiftMaster, suburban home
with a closed door, modern dark sectional at dusk, crew holding torsion springs —
each at 1.91:1 and 1:1, plus one 4:5.

**Why not the 47 creatives in the ad-review set:** Search image assets must be
photographs. Google prohibits overlaid text, logos, buttons or graphics, and
every one of those creatives has a headline burned into it. They are correct for
Meta and wrong for this. Natural branding inside a photograph — a logo on a shirt
or a truck door — is fine; it is *added* graphics that are not.

Regenerate with `python3 build_image_assets.py`.

---

## 4 & 5. Sitelinks and structured snippets — **built, just not imported**

Both already exist; the warning only means the asset files have not been imported
yet. They are deliberately separate from `00_FULL_IMPORT.csv`.

- `import/07_assets_sitelinks.csv` — **6 sitelinks per campaign**, each with two
  description lines, which clears the "4 with descriptions" threshold
- `import/09_assets_structured_snippets.csv` — Services and Brands
- `import/08_assets_callouts.csv` — 8 callouts per campaign

---

## 6. Audience segments — **worth doing, in Observation mode**

**Campaign > Audiences > Edit audience segments > scope: Campaign** (not ad
group — segment data is thin enough at this budget without splitting it 18 ways).

Search campaigns default to **Observation**. Confirm the toggle says that before
saving. Targeting *restricts* ads to those people and would gut reach;
Observation changes delivery not at all and just reports by segment.

| Segment | Where in the picker | Why |
|---|---|---|
| Home Improvement | In-market > Home & Garden | Broadest genuine buyer pool |
| Home Improvement Services | In-market, if listed | Closer to hiring than DIY |
| Recently moved / Moving soon | Life events | The strongest of these |
| Homeowners | Detailed demographics > Homeownership status | Renters cannot authorise the work |
| All visitors | Your data | Needs the remarketing tag — add at cutover |

Recent movers deserve the emphasis: a door ignored for fifteen years tends to be
dealt with in the first six months of new ownership, which predicts better than
general home-improvement interest.

**Also build a custom segment** — New custom segment > *people who searched for
any of these terms*:

    garage door repair
    broken garage door spring
    garage door opener repair
    garage door won't open
    garage door replacement

A tighter definition of the buyer than any off-the-shelf category, and it becomes
the seed list if Display or YouTube retargeting ever runs off the Meta creative.

**Leave bid adjustments at 0%.** With no conversion history an adjustment is a
guess applied to every auction. Revisit at 60–90 days: pull the audience report,
see which segments booked jobs, adjust then.

**Honest expectation:** this is data-gathering, not performance. In Observation
it will not change a single impression this month. Its value is that in two
months you will know whether recent movers convert at three times everyone else.

---

## 7. Display Network expansion — **decline, firmly**

> "Get more conversions at a similar CPA using unspent budget."

The worst recommendation in the list.

Display expansion lets a Search campaign spend its budget on banner placements
across the Display Network. That traffic is not searching for anything — it is
someone reading an unrelated page. For an emergency trade whose entire value is
catching somebody whose door has just broken, that is not the same customer at a
lower price; it is a different, worse customer.

Note "unspent budget" doing the work in that sentence. If a campaign is not
spending, fix targeting or bids — do not hand the remainder to Display.

For reach beyond search, the 47 Meta creatives already built are a far better use
of the money.

---

## Summary

| # | Recommendation | Action |
|---|---|---|
| 1 | EU political ads | **Declare "No" — blocking** |
| 2 | Automated bidding | Decline until week 4 |
| 3 | Image assets | Fixed — upload the 11 files |
| 4 | Sitelinks | Import `07_assets_sitelinks.csv` |
| 5 | Structured snippets | Import `09_assets_structured_snippets.csv` |
| 6 | Audience segments | Add in **Observation** mode |
| 7 | Display expansion | **Decline** |

Ignoring 2 and 7 holds Optimization Score in the 70s. That is fine. It is not a
performance metric — booked jobs are.
