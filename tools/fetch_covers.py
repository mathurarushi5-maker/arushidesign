"""Fetch missing book covers from Open Library into assets/covers/ and record them in content/library.json."""
import json, os, re, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = f"{ROOT}/content/library.json"
lib = json.load(open(P, encoding="utf-8"))
os.makedirs(f"{ROOT}/assets/covers", exist_ok=True)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "arushidesign-site"}), timeout=20).read()


for b in lib["books"]:
    if b.get("cover"):
        continue
    slug = re.sub(r"[^a-z0-9]+", "-", b["title"].lower()).strip("-")
    q = urllib.parse.urlencode({"title": b["title"].split(":")[0], "author": b["author"].split()[-1], "limit": 5, "fields": "cover_i,title"})
    try:
        docs = json.loads(get(f"https://openlibrary.org/search.json?{q}"))["docs"]
        cid = next((d["cover_i"] for d in docs if d.get("cover_i")), None)
        if not cid:
            print("no cover:", b["title"]); continue
        open(f"{ROOT}/assets/covers/{slug}.jpg", "wb").write(get(f"https://covers.openlibrary.org/b/id/{cid}-L.jpg"))
        b["cover"] = f"/assets/covers/{slug}.jpg"
        print("ok:", b["title"])
    except Exception as ex:
        print("fail:", b["title"], ex)
json.dump(lib, open(P, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
