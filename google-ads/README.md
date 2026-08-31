# TML Garage Door Services — Google Ads

Everything for the $10,000/month Search campaign. Kept in the repo rather than
in `~/Downloads` because the first copy was lost when that folder was cleared.

| Start here | |
|---|---|
| **STRATEGY.md** | The plan, the market data, and why the budget is split as it is |
| **IMPORT-INSTRUCTIONS.md** | How to load it into Google Ads Editor |
| **RECOMMENDATIONS-TRIAGE.md** | Google's in-account nudges: which to act on, which to decline |
| `import/00_FULL_IMPORT.csv` | The whole account in one file — this is the one to import |
| `image-assets/` | 11 Search image assets, cropped from the site's own photography |

## Regenerating

```
python3 build_campaign.py       # all 13 CSVs including 00_FULL_IMPORT.csv
python3 build_image_assets.py   # the 11 image assets
```

Both are idempotent. `build_campaign.py` validates before it writes and will
refuse to produce files if a negative keyword blocks an active keyword, a keyword
duplicates inside a campaign, an ad group has no ad, or any headline or
description is over length.

## Not in here

The DataForSEO research JSON (volumes, keyword ideas, radius forecasts) was lost
with the original folder. Its findings are written into `STRATEGY.md`; the raw
files can be re-pulled for about $4 in API credits if they are ever needed again.

Credentials live in `~/GIT/tree-removal-huntsville-texas/.env`.
