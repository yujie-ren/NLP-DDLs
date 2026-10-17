"""Wrap past dates in README tables with <sub> so they render in a smaller font.

A date counts as past once its whole day has ended Anywhere on Earth (UTC-12).
Dates already wrapped in <sub> are left alone; estimates like "2027-05 (e)" are ignored.
In tables with Conference and Location columns, the Location is shrunk too once the Conference date is.
"""
import datetime
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
today_aoe = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=12)).date().isoformat()

pattern = re.compile(r"(?<![>\d])(\d{4})-(\d{2})[-–](\d{2})(?![<\d])")


def shrink(m):
    date = f"{m[1]}-{m[2]}-{m[3]}"
    return f"<sub>{m[0]}</sub>" if date < today_aoe else m[0]


with open(path, encoding="utf-8") as f:
    text = f.read()

lines = [pattern.sub(shrink, line) if line.startswith("|") else line for line in text.split("\n")]

conf_col = loc_col = None
for i, line in enumerate(lines):
    if not line.startswith("|"):
        conf_col = loc_col = None
        continue
    cells = line.split("|")
    names = [c.strip() for c in cells]
    if "Conference" in names and "Location" in names:
        conf_col, loc_col = names.index("Conference"), names.index("Location")
        continue
    if conf_col is None or len(cells) <= max(conf_col, loc_col):
        continue
    loc = cells[loc_col].strip()
    if cells[conf_col].strip().startswith("<sub>") and loc and loc != "-" and not loc.startswith("<sub>"):
        cells[loc_col] = cells[loc_col].replace(loc, f"<sub>{loc}</sub>", 1)
        lines[i] = "|".join(cells)

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
