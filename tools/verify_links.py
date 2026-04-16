from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[1]
htmls = list(root.rglob("*.html"))
issues = []
for f in htmls:
    soup = BeautifulSoup(f.read_text(encoding="utf-8", errors="replace"), "html.parser")
    for tag, attr in [("a", "href"), ("script", "src"), ("link", "href"), ("img", "src"), ("iframe", "src")]:
        for t in soup.find_all(tag):
            u = t.get(attr)
            if not u or u.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            clean = u.split("?")[0].split("#")[0]
            target = (f.parent / clean).resolve()
            if not target.exists():
                issues.append((str(f.relative_to(root)), tag, attr, u))
if issues:
    print("Broken links found:")
    for item in issues:
        print(item)
    raise SystemExit(1)
print(f"OK: checked {len(htmls)} HTML files, no broken local links found.")
