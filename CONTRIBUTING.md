# Contributing

Corrections and additions are welcome, especially from founders, lawyers and accountants in the US, Canada and Australia.

- **Checklist rows:** edit `checklist/data-room-checklist.csv` (the source of truth), keep the columns, and cite an official source (government, regulator or the instrument's publisher) in the `Official source` column when a row depends on a legal rule. Then regenerate or update the matching Markdown files.
- **Calculator:** add a test in `tests/` for any change to `cap-table/safe_cap_table.py`, ideally a worked example from a published source. `python3 -m unittest discover -s tests` must pass.
- **Templates:** keep them short and practical. No made-up statistics.
- Nothing here is legal, tax or investment advice; please don't add language that suggests it is.

By contributing you agree that documentation and templates are licensed under CC BY 4.0 and code under the MIT License.
