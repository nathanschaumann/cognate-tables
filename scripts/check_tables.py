"""Validate the published tables and print the per-direction counts used in the README.

Checks: header, class in {transparent, altered}, no empty cells, no duplicate receiver word per
direction, every word lowercase, no em-dashes, the markdown files match the CSVs.

    python3 scripts/check_tables.py
"""
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
HEADER = ["receiver_lang", "receiver_word", "donor_lang", "donor_word", "class"]
LANGS = {"en", "es", "pt", "fr", "ru", "hy"}


def main():
    problems = []
    counts = {}
    for p in sorted((ROOT / "csv").glob("*.csv")):
        with open(p, newline="", encoding="utf-8") as fh:
            rd = csv.reader(fh)
            if next(rd) != HEADER:
                problems.append(f"{p.name}: bad header")
            seen = set()
            for i, row in enumerate(rd, start=2):
                if len(row) != 5 or not all(row):
                    problems.append(f"{p.name}:{i}: malformed row {row}")
                    continue
                rl, rw, dl, dw, cl = row
                if rl not in LANGS or dl not in LANGS or rl == dl or rl == "en":
                    problems.append(f"{p.name}:{i}: bad language codes {rl}/{dl}")
                if cl not in ("transparent", "altered"):
                    problems.append(f"{p.name}:{i}: bad class {cl}")
                if (rl, dl, rw) in seen:
                    problems.append(f"{p.name}:{i}: duplicate receiver word {rw}")
                seen.add((rl, dl, rw))
                if rw != rw.lower() or dw != dw.lower():
                    problems.append(f"{p.name}:{i}: not lowercase {rw}/{dw}")
                c = counts.setdefault((rl, dl), [0, 0])
                c[cl == "altered"] += 1
    for p in ROOT.rglob("*"):
        if p.is_file() and ".git" not in p.parts and p.suffix in (".md", ".csv", ".py", ".json") and chr(0x2014) in p.read_text(encoding="utf-8"):
            problems.append(f"{p.relative_to(ROOT)}: contains an em-dash")
    for p in sorted((ROOT / "csv").glob("*.csv")):
        from build_markdown import render
        if (ROOT / "markdown" / f"{p.stem}.md").read_text(encoding="utf-8") != render(p):
            problems.append(f"markdown/{p.stem}.md is out of date")
    print(f"{'receiver':<9}{'donor':<7}{'rows':>8}{'transparent':>13}{'altered':>9}")
    tot = 0
    for (rl, dl), (t, a) in sorted(counts.items()):
        print(f"{rl:<9}{dl:<7}{t + a:>8,}{t:>13,}{a:>9,}")
        tot += t + a
    print(f"{'total':<16}{tot:>8,}   ({len(counts)} directional tables, {len(list((ROOT / 'csv').glob('*.csv')))} pairs)")
    if problems:
        print("\nPROBLEMS:")
        print("\n".join(problems[:40]))
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    main()
