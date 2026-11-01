# Startup Data Room Checklist (Pre-Seed, Seed, Series A) + Investor Update Template + SAFE Cap Table Calculator

[![License: CC BY 4.0](https://img.shields.io/badge/Docs-CC_BY_4.0-lightgrey.svg)](LICENSE)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE-CODE)
[![Tests](https://github.com/unboxth/startup-data-room-checklist/actions/workflows/test.yml/badge.svg)](https://github.com/unboxth/startup-data-room-checklist/actions/workflows/test.yml)
![Documents](https://img.shields.io/badge/checklist-50_documents-2563EB)

A free, open **startup data room checklist**: the 50 documents investors ask for, sorted into 10 numbered folders and tagged by the stage they're usually needed (pre-seed, seed, Series A), with notes where the US, Canada and Australia differ. Plus a **monthly investor update template** and a tested **post-money SAFE cap table calculator** in Python.

Built for founders raising in the US, Canada and Australia. Fork it, copy it into Notion, or run one script to create the folder structure.

## Contents

- [Quick start](#quick-start)
- [Pre-seed data room checklist](#pre-seed-data-room-checklist-20-documents)
- [Checklists by stage](#checklists-by-stage)
- [Data room folder structure](#data-room-folder-structure)
- [Investor update template](#investor-update-template)
- [Post-money SAFE cap table calculator](#post-money-safe-cap-table-calculator)
- [Country notes](#country-notes-us-canada-australia)
- [FAQ](#faq)
- [Sources](#sources)
- [Contributing](#contributing) · [License](#license)

## Quick start

```bash
git clone https://github.com/unboxth/startup-data-room-checklist.git
cd startup-data-room-checklist

# 1. Create your data room folders + an index for your stage (pre-seed | seed | series-a)
python3 scripts/make_data_room.py --stage seed --out ./data-room

# 2. Model your SAFEs and next round
python3 cap-table/safe_cap_table.py cap-table/examples/yc-example-1.json
```

Upload `./data-room` to Google Drive, Dropbox, Notion or your data room tool, then fill in `00 Start here/INDEX.csv` (Status, Owner, Link) as you go. No Python? Use the [CSV](checklist/data-room-checklist.csv) or the [XLSX with status dropdowns and a progress sheet](https://www.unboxth.xyz/resources/startup-data-room-checklist/?utm_source=github&utm_medium=readme&utm_campaign=data-room).

## Pre-seed data room checklist (20 documents)

Keep a pre-seed room small. These are the documents investors usually ask for first:

**00 Start here**

- [ ] Data room index (this checklist) with a contact for questions
- [ ] Current pitch deck (PDF)
- [ ] One-page company summary

**01 Corporate**

- [ ] Certificate of incorporation and any amendments
- [ ] Bylaws (or constitution) and any shareholder agreement
- [ ] Board and stockholder consents and minutes

**02 Cap table**

- [ ] Fully diluted cap table (spreadsheet or Carta/Pulley export)
- [ ] Stock ledger / securities register / members register
- [ ] Founder stock purchase agreements with vesting
- [ ] Founder 83(b) elections with proof of timely filing
- [ ] All SAFEs, convertible notes and side letters (signed)

**03 Financial**

- [ ] Financial model with assumptions (monthly, 18-24 months)
- [ ] Use of funds for this round

**05 Legal and IP**

- [ ] Founder IP assignment / invention assignment agreements
- [ ] Employee and contractor agreements with IP assignment

**06 Product**

- [ ] Product demo video or sandbox login

**07 Customers**

- [ ] Key metrics definitions and dashboard export
- [ ] Pipeline and signed LOIs

**08 Team**

- [ ] Team bios and org chart

**09 Round**

- [ ] Term sheet or SAFE terms for this round

Every row, with *why investors ask* and the country notes, is in [checklist/full-checklist.md](checklist/full-checklist.md).

## Checklists by stage

| Stage | Documents | File |
|---|---|---|
| Pre-seed | 20 | [pre-seed-data-room-checklist.md](checklist/pre-seed-data-room-checklist.md) |
| Seed | 44 | [seed-data-room-checklist.md](checklist/seed-data-room-checklist.md) |
| Series A | 50 | [series-a-data-room-checklist.md](checklist/series-a-data-room-checklist.md) |
| All, as a spreadsheet | 50 | [data-room-checklist.csv](checklist/data-room-checklist.csv) (columns: Folder, Document, Why investors ask, Needed from, Country note, Status, Owner, Link, Source) |

The CSV doubles as your **data room index**: share it (or the generated `INDEX.csv`) as the table of contents.

## Data room folder structure

```
data-room/
├── 00 Start here/      index, deck, one-page summary
├── 01 Corporate/       incorporation, bylaws/constitution, consents, good standing
├── 02 Cap table/       cap table, stock ledger/registers, founder stock + 83(b), SAFEs, option plan
├── 03 Financial/       model, management accounts, bank statements, revenue schedule, use of funds
├── 04 Tax/             tax returns, sales tax/GST/HST, payroll filings
├── 05 Legal and IP/    IP assignments, contractor agreements, material contracts, privacy/terms
├── 06 Product/         demo, architecture, security, roadmap
├── 07 Customers/       metric definitions, cohorts, pipeline/LOIs, references
├── 08 Team/            bios, hiring plan, key employment agreements, visa status
└── 09 Round/           term sheet or SAFE terms, pro forma cap table, past investor updates
```

Numbered names keep folders in the order investors read them.

## Investor update template

[investor-updates/](investor-updates/) has a monthly template (TL;DR, metrics table, wins, lowlights, learnings, product, team, asks), a quarterly version and a plain-text email you can paste anywhere. Same metrics, same order, every month, and file each one in `09 Round/`.

## Post-money SAFE cap table calculator

[cap-table/safe_cap_table.py](cap-table/) converts YC-style post-money SAFEs (valuation cap or discount) and models a priced round with an option pool top-up. It reproduces **YC's Post-Money SAFE User Guide Example 1** (company capitalization 11,764,705; founders 51.54% after the round), and the tests check it.

```text
$ python3 cap-table/safe_cap_table.py cap-table/examples/yc-example-1.json
Company capitalization (SAFE conversion): 11,764,705
  Investor A: safe price $0.3400, converts at cap
  Investor B: safe price $0.6800, converts at cap
Round price per share: $1.1145   pool increase: 1,694,570   post-money: $20,000,000
...
  Founders                          9,250,000    51.54%
  New investors (priced round)      4,486,425    25.00%
```

Prefer a spreadsheet? Use the free [cap table template with SAFE (XLSX)](https://www.unboxth.xyz/resources/cap-table-template/?utm_source=github&utm_medium=readme&utm_campaign=data-room). New to SAFEs? Read [post-money SAFE explained](https://www.unboxth.xyz/founder-playbooks/post-money-safe-explained/?utm_source=github&utm_medium=readme&utm_campaign=data-room).

## Country notes (US, Canada, Australia)

- **US (Delaware C-corp):** investors check good standing and franchise tax ([Delaware Division of Corporations](https://corp.delaware.gov/paytaxes/)), founder 83(b) elections and proof they were filed within 30 days ([IRS Form 15620](https://www.irs.gov/pub/irs-pdf/f15620.pdf)), and every signed SAFE ([YC documents](https://www.ycombinator.com/documents)).
- **Canada (CBCA):** corporations keep corporate records including a securities register and, for most, a register of individuals with significant control ([Corporations Canada](https://www.ised-isde.canada.ca/site/corporations-canada/en/business-corporations/corporate-records-and-other-corporate-obligations)).
- **Australia:** every company keeps a register of members with share allotment details ([ASIC](https://www.asic.gov.au/for-business-and-companies/companies/company-share-and-shareholder-rules-and-changes/members-register-requirements-and-changes)). If you flipped into a Delaware parent, add the org chart showing the Australian subsidiary.

## FAQ

**What should be in a startup data room?**
Corporate documents, the cap table and every signed equity document, financials and tax filings, IP assignments and key contracts, product and customer evidence, team information, and the current round's terms. The [full checklist](checklist/full-checklist.md) lists 50 documents in 10 folders.

**What goes in a pre-seed data room?**
About 20 documents: the deck and summary, incorporation documents and consents, the cap table and registers, founder stock agreements and 83(b) proofs, signed SAFEs, IP assignments, a simple model, metrics and the round's terms.

**When should I set up a data room?**
Before you start pitching. Signatures and certificates (IP assignments, good standing, 83(b) proofs) take the longest to collect.

**Do I need paid data room software?**
Not at pre-seed or seed. A shared folder with view-only links works; paid tools add view tracking and permissions.

**Is this legal advice?**
No. It's a general checklist. Your lawyer and lead investor may ask for more.

## Sources

- [Y Combinator: SAFE documents, User Guide and FAQ](https://www.ycombinator.com/documents)
- [Y Combinator: SAFE conversion calculator](https://www.ycombinator.com/safe/calculator)
- [Delaware Division of Corporations: annual report and franchise tax](https://corp.delaware.gov/paytaxes/)
- [IRS Form 15620 (83(b) election)](https://www.irs.gov/pub/irs-pdf/f15620.pdf)
- [Corporations Canada: corporate records and obligations](https://www.ised-isde.canada.ca/site/corporations-canada/en/business-corporations/corporate-records-and-other-corporate-obligations)
- [ASIC: members register requirements](https://www.asic.gov.au/for-business-and-companies/companies/company-share-and-shareholder-rules-and-changes/members-register-requirements-and-changes)

Checked 1 Nov 2026.

## Contributing

Fixes and additions welcome, especially from founders, lawyers and accountants in the US, Canada and Australia. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Checklists, templates and docs: [CC BY 4.0](LICENSE). Code (`cap-table/`, `scripts/`, `tests/`): [MIT](LICENSE-CODE). Attribution: "Startup data room checklist by unboxth (unboxth.xyz)".

---

Made by **[unboxth](https://www.unboxth.xyz/?utm_source=github&utm_medium=readme&utm_campaign=data-room)**, practical guides and tools for startup and AI founders in the US, Canada and Australia. More free templates: [83(b) election template](https://www.unboxth.xyz/resources/83b-election-template/?utm_source=github&utm_medium=readme&utm_campaign=data-room) · [cap table template](https://www.unboxth.xyz/resources/cap-table-template/?utm_source=github&utm_medium=readme&utm_campaign=data-room) · [all resources](https://www.unboxth.xyz/resources/?utm_source=github&utm_medium=readme&utm_campaign=data-room).
