"""Wrap past dates in README tables with <sub> so they render in a smaller font.

A date counts as past once its whole day has ended Anywhere on Earth (UTC-12).
Dates already wrapped in <sub> are left alone; estimates like "2027-05 (e)" are ignored.
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

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
