# Importing the TML campaign

## The short version

Everything except assets is in **`import/00_FULL_IMPORT.csv`** — 1,382 rows:
6 campaigns, 18 ad groups, 240 keywords, 1,022 negatives, 18 responsive search
ads, and all location targeting.

1. Open **Google Ads Editor** and download the TML account
2. `Account > Import > From file…` and choose `00_FULL_IMPORT.csv`
3. Editor shows a proposed-changes preview — **read it before posting**
4. Then import `07`, `08`, `09` and `11` for sitelinks, callouts, structured
   snippets and the call asset
5. `Post`

**Every campaign imports Paused.** Nothing spends until you switch it on.

---

## Why assets are separate

Editor treats sitelinks, callouts, structured snippets and call assets as
different entity types with their own columns. Mixing them into the main file is
the most common reason an import half-succeeds and leaves you unpicking it.

---

## What is in each file

| File | Rows | What |
|---|---:|---|
| **00_FULL_IMPORT.csv** | 1,382 | **Everything below except assets — import this one** |
| 01_campaigns.csv | 6 | Campaigns, budgets, bid strategies |
| 02_ad_groups.csv | 18 | Ad groups and max CPCs |
| 03_keywords.csv | 240 | 122 exact + 118 phrase |
| 04_negative_keywords_shared_list.csv | 168 | Build as a shared list, apply to all six |
| 05_negative_keywords_campaign.csv | 14 | Cross-campaign traffic steering |
| 06_responsive_search_ads.csv | 18 | One RSA per ad group |
| 07_assets_sitelinks.csv | 36 | Six sitelinks per campaign, each with descriptions |
| 08_assets_callouts.csv | 48 | Eight callouts per campaign |
| 09_assets_structured_snippets.csv | 12 | Services and Brands |
| 10_geo_targets.csv | 78 | 25-mile radius plus named towns |
| 11_call_asset.csv | 6 | (832) 887-8747 with call reporting |
| 12_copy_held_back.csv | 5 | Ad copy withheld pending fact-checks — **not for import** |

Files 01–06 and 10 are the same data as `00_FULL_IMPORT.csv`, split by entity
type. Use them if the single-file import gives trouble. Do not import both.

Image assets are in `image-assets/` — 11 JPEGs, uploaded under Assets > Images.

---

## If an import throws warnings

**"Campaign language targeting is invalid" — fixed.** The Languages column was
sending `English`; Editor wants the ISO code `en`. Corrected. If you already
posted the earlier version, you do not need to redo the import — set language to
English on the six campaigns and carry on.

**"Location is invalid" on the radius rows.** Each campaign carries a
`25 mi radius around Conroe, Texas` row plus the individual towns. Editor cannot
always resolve a radius from a text string — it wants coordinates. If those six
rows fail, delete them and add the radius by hand in the web UI
(`Settings > Locations > Enter another location > Advanced search > Radius`).
The named towns are in the file, so coverage holds either way.

**"You can't post until you confirm EU political ads."** Web-UI only, cannot be
set from Editor. See `RECOMMENDATIONS-TRIAGE.md` section 1. After declaring, use
**Account > Get recent changes** in Editor — not a full re-download, which would
discard unposted work — then post again.

**Caution symbols on "Bid strategy" and "Include Display Network".** Two
different things:

- **Include Display Network must be unchecked.** The Networks value was written
  as `Google search` (lowercase s); the documented value is `Google Search`.
  An unparsed Networks value lets Editor fall back to a Search-campaign default
  that *includes* Display, which would leak budget to banner placements. Fixed
  in the current files. To correct campaigns already loaded: select all of them,
  and in the settings panel untick **Display Network**.
- **Bid strategy is almost certainly advisory** — Google nagging toward Smart
  Bidding, the same recommendation declined in `RECOMMENDATIONS-TRIAGE.md`
  section 2. Confirm the field reads `Manual CPC` and leave it. Hover the symbol
  to read the text: if it says the strategy is invalid rather than
  non-recommended, tell me and I will change the value.

Search Partners is now **off for the test** (`Google Search` only) and on for the
full plan. Partner sites cannot be inspected individually, and the test exists to
produce clean data on the core keywords.

Warnings are not errors: a yellow triangle means Editor skipped that one field
and imported the rest of the row.

---

## Set these in the web UI, not Editor

1. **Location targeting option.** Set every campaign to **"Presence: people in
   your targeted locations."** Google's default also includes people merely
   *interested* in the area — for a local trade that means paying for clicks from
   other states. The single most expensive default in Google Ads, and a CSV
   cannot set it.
2. **Shared negative list.** `04_…` is written as campaign negatives in the full
   import, which works, but a shared list is easier to maintain.
   `Tools > Shared library > Negative keyword lists`.
3. **Ad schedule.** Not in the files because nobody has confirmed TML's call
   hours.
4. **Conversion actions.** Calls from ads, calls from the website, and — once the
   native form exists — form submissions.
5. **Audience segments.** See `RECOMMENDATIONS-TRIAGE.md` section 6.

---

## Before you enable anything

- [ ] Advanced Verification approved (nothing serves without it)
- [ ] EU political ads declared
- [ ] Site cut over to the live domain, `noindex` removed
- [ ] Conversion tracking firing — calls at minimum
- [ ] Location targeting set to **Presence**
- [ ] Call asset using a Google forwarding number
- [ ] Budgets confirmed: $328.96/day across six campaigns
- [ ] Enable **Head Terms only** for week one, then the rest
- [ ] Search-term report reviewed daily for the first fortnight

---

## Rebuilding

```
python3 build_campaign.py       # all 13 CSVs
python3 build_image_assets.py   # the 11 image assets
```

`build_campaign.py` refuses to write anything that would fail on import or
misfire once live: headlines over 30 characters, descriptions over 90, a negative
that blocks one of your own keywords, a duplicate keyword inside a campaign, or
an ad group with no ad.
