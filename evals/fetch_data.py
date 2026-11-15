"""Fetch the human text sets. Stdlib only. Run from the repo root: python evals/fetch_data.py"""
import csv, html, json, re, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

UA = {"User-Agent": "ultimate-humanizer-eval/1.0 (github.com/DrARaj/ultimate-humanizer)"}
DATA = Path(__file__).parent / "data"
TODAY = time.strftime("%Y-%m-%d")

TOPICS = [  # science, history, geography, biography, medicine, public health
    "Photosynthesis", "Plate tectonics", "Superconductivity", "Black hole", "Enzyme",
    "Coral reef", "Cell nucleus", "Gravitational wave", "Periodic table", "Tardigrade",
    "Roman Republic", "Black Death", "Meiji Restoration", "Hanseatic League", "Peace of Westphalia",
    "Mali Empire", "Industrial Revolution", "Byzantine Empire", "Silk Road", "Treaty of Versailles",
    "Lake Baikal", "Danube", "Atacama Desert", "Mount Kilimanjaro", "Madagascar",
    "Ada Lovelace", "Marie Curie", "Srinivasa Ramanujan", "Florence Nightingale", "Alan Turing",
    "Tuberculosis", "Insulin", "Malaria", "Hypertension", "Penicillin",
    "Vaccination", "Cholera", "Smallpox", "Tobacco smoking", "Antimicrobial resistance",
]


class Paras(HTMLParser):
    """Collect plain text of <p> elements outside tables/blockquotes; drop <sup>, <style>, edit links."""
    def __init__(self):
        super().__init__(); self.out = []; self.cur = None; self.depth = 0; self.skip_tag = None; self.skip_n = 0
    def handle_starttag(self, tag, attrs):
        if self.skip_tag:
            self.skip_n += tag == self.skip_tag
            return
        if tag in ("table", "blockquote"):
            self.depth += 1
        elif tag == "p" and self.cur is None and not self.depth:
            self.cur = []
        elif self.cur is not None and (tag in ("sup", "style") or "mw-editsection" in dict(attrs).get("class", "")):
            self.skip_tag, self.skip_n = tag, 1
    def handle_endtag(self, tag):
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_n -= 1
                if not self.skip_n:
                    self.skip_tag = None
            return
        if tag in ("table", "blockquote") and self.depth:
            self.depth -= 1
        elif tag == "p" and self.cur is not None:
            self.out.append("".join(self.cur)); self.cur = None
    def handle_data(self, d):
        if self.cur is not None and not self.skip_tag:
            self.cur.append(d)


def get(url):
    for wait in (5, 20, 60, 120, None):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code != 429 or wait is None:
                raise
            time.sleep(wait)


def api(**p):
    p["format"] = "json"; p["formatversion"] = "2"
    return json.loads(get("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)))


def clean(t):
    t = re.sub(r"\[\s*(?:\d+|[a-z]|citation needed|note \d+)\s*\]", "", t)  # citation markers
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def wiki_para(title):
    q = api(action="query", prop="revisions", titles=title, rvprop="ids", rvlimit=1,
            rvstart="2021-12-31T00:00:00Z", rvdir="older")
    revid = q["query"]["pages"][0]["revisions"][0]["revid"]
    h = api(action="parse", oldid=revid, prop="text")["parse"]["text"]
    p = Paras(); p.feed(h)
    paras = [clean(x) for x in p.out]
    ok = [x for x in paras if 90 <= len(x.split()) <= 240 and not re.search(r"[|{}]|\bcoord\b", x)]
    return revid, (ok[1] if len(ok) > 1 else ok[0])  # second qualifying paragraph: avoid pure lead boilerplate


def wiki():
    rows = []
    cache = DATA / "wiki_cache.json"  # lets an interrupted run resume
    done = json.loads(cache.read_text()) if cache.exists() else {}
    for i, t in enumerate(TOPICS, 1):
        id_ = f"wiki{i:02d}"
        if id_ in done and (DATA / f"{id_}.txt").exists():
            rows.append(done[id_]); continue
        revid, text = wiki_para(t)
        (DATA / f"{id_}.txt").write_text(text + "\n", encoding="utf-8")
        url = f"https://en.wikipedia.org/w/index.php?title={urllib.parse.quote(t.replace(' ', '_'))}&oldid={revid}"
        rows.append([id_, "human-wiki", url, "CC BY-SA 4.0", TODAY, t, len(text.split())])
        done[id_] = rows[-1]; cache.write_text(json.dumps(done))
        time.sleep(2)
    return rows


ARXIV_Q = ["cat:q-bio.PE", "cat:q-bio.GN", "cat:stat.ME", "cat:stat.AP", "cat:cs.CL",
           "cat:physics.soc-ph", "cat:physics.bio-ph", "cat:q-bio.QM", "cat:stat.ML", "cat:cs.CL"]


def arxiv():
    ns = {"a": "http://www.w3.org/2005/Atom"}
    rows, seen = [], set()
    for qi, cat in enumerate(ARXIV_Q):
        # 2 per query; submittedDate filter keeps everything before 2021-01-01
        q = f"{cat} AND submittedDate:[201501010000 TO 202012312359]"
        url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": q, "start": qi * 7, "max_results": 25, "sortBy": "submittedDate"})
        root = ET.fromstring(get(url))
        time.sleep(3)
        got = 0
        for e in root.findall("a:entry", ns):
            abs_ = clean(e.find("a:summary", ns).text)
            link = e.find("a:id", ns).text.strip()
            if link in seen or not 80 <= len(abs_.split()) <= 250 or "$" in abs_:
                continue
            seen.add(link); got += 1
            n = len(rows) + 1; id_ = f"abs{n:02d}"
            (DATA / f"{id_}.txt").write_text(abs_ + "\n", encoding="utf-8")
            rows.append([id_, "human-abstracts", link, "CC0 (arXiv metadata)", TODAY, cat.split(":")[1], len(abs_.split())])
            if got == 2 or len(rows) == 20: break
        if len(rows) == 20: break
    return rows


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    rows = wiki() + arxiv()
    with open(DATA / "manifest_human.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id", "set", "source_url", "licence", "retrieved", "topic", "words"]); w.writerows(rows)
    print(len(rows), "human passages")
