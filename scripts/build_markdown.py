"""Render csv/<a>-<b>.csv into markdown/<a>-<b>.md (one file per language pair, one table per direction).

    python3 scripts/build_markdown.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent
NAMES = {"en": "English", "es": "Spanish", "pt": "Portuguese", "fr": "French", "ru": "Russian", "hy": "Armenian"}


def render(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    a, b = path.stem.split("-")
    out = [f"# Cognates: {NAMES[a]} and {NAMES[b]}", ""]
    directions = []
    for r in rows:
        d = (r["receiver_lang"], r["donor_lang"])
        if d not in directions:
            directions.append(d)
    for recv, donor in directions:
        sub = [r for r in rows if r["receiver_lang"] == recv and r["donor_lang"] == donor]
        t = sum(r["class"] == "transparent" for r in sub)
        out += [f"## {NAMES[recv]} words credited from {NAMES[donor]} ({len(sub):,} rows: {t:,} transparent, {len(sub) - t:,} altered)", "",
                f"| {NAMES[recv]} | {NAMES[donor]} | class |", "|---|---|---|"]
        out += [f"| {r['receiver_word']} | {r['donor_word']} | {r['class']} |" for r in sub]
        out.append("")
    return "\n".join(out)


def main():
    (ROOT / "markdown").mkdir(exist_ok=True)
    for p in sorted((ROOT / "csv").glob("*.csv")):
        (ROOT / "markdown" / f"{p.stem}.md").write_text(render(p), encoding="utf-8")
        print("wrote", f"markdown/{p.stem}.md")


if __name__ == "__main__":
    main()
