#!/usr/bin/env python3
"""Create a startup data room folder structure from the checklist.

    python3 scripts/make_data_room.py --stage seed --out ./data-room

Creates the numbered folders (00 Start here ... 09 Round), a README.md in each
folder listing the documents that belong there for your stage, and
"00 Start here/INDEX.csv" with Status / Owner / Link columns to fill in.
Upload the folder to Google Drive, Dropbox, Notion or your data room tool.
No dependencies beyond Python 3.8+.
"""
import argparse, csv, pathlib, sys

STAGES = ["pre-seed", "seed", "series-a"]
LABEL = {"Pre-seed": "pre-seed", "Seed": "seed", "Series A": "series-a"}
ROOT = pathlib.Path(__file__).resolve().parent.parent


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=STAGES, default="seed", help="include documents needed up to this stage (default: seed)")
    ap.add_argument("--out", default="data-room", help="output folder (default: ./data-room)")
    ap.add_argument("--checklist", default=str(ROOT / "checklist" / "data-room-checklist.csv"))
    a = ap.parse_args(argv)

    with open(a.checklist, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    limit = STAGES.index(a.stage)
    rows = [r for r in rows if STAGES.index(LABEL[r["Needed from"]]) <= limit]

    out = pathlib.Path(a.out)
    folders = {}
    for r in rows:
        folders.setdefault(r["Folder"], []).append(r)
    for folder, docs in folders.items():
        d = out / folder
        d.mkdir(parents=True, exist_ok=True)
        lines = [f"# {folder}", "", f"Documents for a {a.stage} data room:", ""]
        for r in docs:
            lines.append(f"- [ ] **{r['Document']}** ({r['Needed from']}) - {r['Why investors ask']}")
            note = r["US / Canada / Australia note"]
            if note and note != "All":
                lines.append(f"  - {note}")
        (d / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    idx = out / "00 Start here" / "INDEX.csv"
    idx.parent.mkdir(parents=True, exist_ok=True)
    with open(idx, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["#", "Folder", "Document", "Needed from", "Status", "Owner", "Link to file"])
        for r in rows:
            w.writerow([r["#"], r["Folder"], r["Document"], r["Needed from"], "Not started", "", ""])
    print(f"Created {len(folders)} folders and an index of {len(rows)} documents for a {a.stage} data room in {out.resolve()}")


if __name__ == "__main__":
    sys.exit(main())
