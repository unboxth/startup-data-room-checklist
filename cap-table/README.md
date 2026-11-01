# Post-money SAFE cap table calculator (Python)

`safe_cap_table.py` converts post-money SAFEs and models a priced round with an option pool top-up. No dependencies; Python 3.8+.

```bash
python3 cap-table/safe_cap_table.py cap-table/examples/yc-example-1.json
python3 cap-table/safe_cap_table.py my-company.json --csv after-round.csv
```

## Input format

```json
{
  "holders": {"Founders": 9250000, "Options outstanding": 300000, "Promised options": 350000},
  "unissued_pool": 100000,
  "safes": [
    {"name": "Investor A", "amount": 200000, "cap": 4000000},
    {"name": "Investor B", "amount": 800000, "cap": 8000000},
    {"name": "Bridge", "amount": 300000, "discount": 0.20}
  ],
  "pre_money": 15000000,
  "investment": 5000000,
  "pool_target_post": 0.10
}
```

Leave out `pre_money` to see ownership right after the SAFEs (before any priced round). A SAFE with `cap` and no `discount` is YC's valuation-cap SAFE; `discount` with no `cap` is YC's discount SAFE.

## The maths (from YC's Post-Money SAFE User Guide)

- **Company capitalization** = issued shares + outstanding and promised options + existing unissued pool + all SAFE conversion shares. It excludes the new money and the pool increase in the priced round.
- **Safe price** = post-money valuation cap ÷ company capitalization. With every SAFE converting at its cap, company capitalization = existing fully diluted shares ÷ (1 − Σ amount/cap).
- **Discount price** = round price × (1 − discount). Each SAFE converts at the lowest price that applies to it. When any SAFE converts below its cap the script iterates until the share counts are stable.
- **Priced round:** new investors own investment ÷ post-money, and the pool increase is solved so the unissued pool equals your target % after the round.

## Verified against

| Example | Check | Result |
|---|---|---|
| [YC User Guide, Example 1](examples/yc-example-1.json) | Company capitalization 11,764,705; SAFE prices $0.34 / $0.68; founders 51.54% after a $5M round at $15M pre with a 10% pool | Matches (pool increase solved exactly at 1,694,570; YC rounds it to 1,695,000) |
| [Two SAFEs + Series A](examples/two-safes-series-a.json) | 12,500,000 capitalization, $1.2174 round price, 16,428,571 shares after the round | Matches the [worked example on unboxth](https://www.unboxth.xyz/founder-playbooks/post-money-safe-explained/?utm_source=github&utm_medium=readme&utm_campaign=data-room) |

Run the tests: `python3 -m unittest discover -s tests`.

## What it does not model

MFN SAFEs, convertible notes with interest, pre-money SAFEs, pro rata side letters, multiple share classes and exit waterfalls. Your lawyer's closing cap table is the source of truth.

Prefer a spreadsheet? The [cap table template with SAFE (XLSX)](https://www.unboxth.xyz/resources/cap-table-template/?utm_source=github&utm_medium=readme&utm_campaign=data-room) uses the same maths with live formulas. YC also has a free [SAFE conversion calculator](https://www.ycombinator.com/safe/calculator).
