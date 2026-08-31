# TML Garage Door Services — Google Ads

Everything for the $10,000/month Search campaign. Kept in the repo rather than
in `~/Downloads` because the first copy was lost when that folder was cleared.

| Start here | |
|---|---|
| **STRATEGY.md** | The plan, the market data, and why the budget is split as it is |
| **IMPORT-INSTRUCTIONS.md** | How to load it into Google Ads Editor |
| **RECOMMENDATIONS-TRIAGE.md** | Google's in-account nudges: which to act on, which to decline |
| **CLAUDE-HANDOFF.md** | Self-contained brief — paste into a fresh Claude session to fine-tune the campaign with full context |
| **TEST-PLAN.md** | The $2,000 / 60-day lead test: design, thresholds, what invalidates it |
| `import/00_FULL_IMPORT.csv` | The full $10,000 account in one file |
| `import-test/00_FULL_IMPORT.csv` | The $2,000 test — 4 campaigns, exact match only |
| `image-assets/` | 11 Search image assets, cropped from the site's own photography |

## Regenerating

```
python3 build_campaign.py          # the full $10,000 plan -> import/
python3 build_campaign.py --test   # the $2,000 test        -> import-test/
python3 build_handoff.py           # regenerate CLAUDE-HANDOFF.md from live data
python3 build_image_assets.py   # the 11 image assets
```

Both are idempotent. `build_campaign.py` validates before it writes and will
refuse to produce files if a negative keyword blocks an active keyword, a keyword
duplicates inside a campaign, an ad group has no ad, or any headline or
description is over length.

## Research data

`research/keyword_data.json` holds the DataForSEO volume and CPC pull for all 125
unique keywords, Conroe and Houston, re-pulled 25 Aug 2026. `build_handoff.py`
reads it to generate the keyword table in `CLAUDE-HANDOFF.md`, so the brief and
the campaign can never drift apart.

The radius forecast and the 5,174-keyword idea mining were not re-pulled — their
findings are written into `STRATEGY.md` and the handoff doc.

Credentials live in `~/GIT/tree-removal-huntsville-texas/.env`.
