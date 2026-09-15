import re
from bs4 import BeautifulSoup

TIME_RE = re.compile(r"choiceTime\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]")
COURT_RE = re.compile(r"choiceCourt\(['\"](TC\d+)['\"]\s*,\s*['\"](\d+)['\"]")

def available_times(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for li in soup.find_all("li"):
        classes = li.get("class", [])
        onclick = li.get("onclick", "")
        if "off_court" in classes:
            continue
        m = TIME_RE.search(onclick)
        if m:
            out.append({"code": m.group(1), "from": m.group(2), "to": m.group(3)})
    return out

def available_courts(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for li in soup.find_all("li"):
        classes = li.get("class", [])
        onclick = li.get("onclick", "")
        if "off_court" in classes:
            continue
        m = COURT_RE.search(onclick)
        if m:
            out.append({"code": m.group(1), "no": int(m.group(2))})
    return out
