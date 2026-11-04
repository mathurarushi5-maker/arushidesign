"""Generates the static site from content/site.json and content/images.json.

Usage: python3 tools/build.py
"""
import json
import time
import html
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(f"{ROOT}/content/site.json", encoding="utf-8"))
images = json.load(open(f"{ROOT}/content/images.json", encoding="utf-8"))
site, projects, experience = data["site"], data["projects"], data["experience"]
e = html.escape

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Inter:wght@400;500;600'
    '&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
)


def head(title, desc, og_image=None):
    og = f'<meta property="og:image" content="/assets/img/{og_image}">' if og_image else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
{og}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/assets/css/style.css?v={ASSET_V}">
</head>"""


def nav(active=""):
    def a(href, label, key):
        cls = ' class="on"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'

    return f"""<nav class="pill" aria-label="Main">
  <a class="dot" href="/" aria-label="Home"></a>
  {a('/#work', 'Work', 'work')}
  {a('/#about', 'Journey', 'about')}
  {a('/#life', 'Off the clock', 'life')}
  {a('/#blog', 'Blog', 'blog')}
  {a('/#contact', 'Contact', 'contact')}
</nav>"""


FACT_ICONS = [
    '<path d="M8 14c8-4 17-3 24 2 7-5 16-6 24-2v34c-8-4-17-3-24 2-7-5-16-6-24-2z"/><path d="M32 16v34"/><path d="M14 22c5-1.500 9-1 13 1M14 30c5-1.500 9-1 13 1M37 23c4-2 8-2.500 13-1M37 31c4-2 8-2.500 13-1"/>',
    '<path d="M46 8c6 4 8 10 4 16L30 44l-12 4 4-12z"/><path d="M40 14l8 8M12 56c6 0 6-4 12-4s6 4 12 4 6-4 12-4"/>',
    '<path d="M32 8C17 8 8 19 8 31c0 11 8 19 18 19 4 0 5-3 3-6-2-4 0-8 5-8h8c7 0 12-4 12-11C54 16 44 8 32 8z"/><circle cx="19" cy="30" r="3.500"/><circle cx="28" cy="19" r="3.500"/><circle cx="41" cy="20" r="3.500"/>',
    '<path d="M26 8c1 10 4 13 14 14-10 1-13 4-14 14-1-10-4-13-14-14 10-1 13-4 14-14z"/><path d="M46 34c.700 6 2.500 8 8 9-5.500 1-7.300 3-8 9-.700-6-2.500-8-8-9 5.500-1 7.300-3 8-9z"/>',
]


def life_section():
    l = data["life"]
    tilts = (-2, 1.5, -1, 2)
    cards = "".join(
        f'<div class="fact reveal" style="--r:{tilts[i % 4]}deg"><svg class="ico" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{FACT_ICONS[i % 4]}</svg><span class="note">{e(f["label"])}</span><p>{e(f["text"])}</p></div>'
        for i, f in enumerate(l["facts"])
    )
    return f"""<section id="life" class="life">
    <span class="note n3">the human part</span>
    <h2 class="reveal">{e(l['title'])}</h2>
    <p class="life-intro reveal">{e(l['intro'])}</p>
    <div class="facts">{cards}</div>
    <div class="sticker l1" data-drag aria-hidden="true"><svg viewBox="0 0 120 50" fill="none" stroke="#1f2bff" stroke-width="7" stroke-linecap="round"><path d="M6 28q14-26 28 0t28 0 28 0 22 0"/></svg></div>
    <div class="sticker l2" data-drag aria-hidden="true"><svg viewBox="0 0 64 64"><path d="M32 4l7 19 20 1-16 12 6 20-17-12-17 12 6-20L5 24l20-1z" fill="#c8f560" stroke="#c8f560" stroke-width="6" stroke-linejoin="round"/></svg></div>
    <div class="sticker l3" data-drag aria-hidden="true"><svg viewBox="0 0 64 64"><path d="M32 54C10 38 6 26 12 18c5-6 14-5 20 3 6-8 15-9 20-3 6 8 2 20-20 36z" fill="none" stroke="#16150f" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/></svg></div>
  </section>"""


BLOG_ART = [
    # AI-powered research to presentation: slide with chart + sparkle
    '<rect x="14" y="16" width="84" height="58" rx="8" fill="#fff"/><path d="M26 58l16-16 12 10 20-24" fill="none"/><circle cx="74" cy="28" r="3" fill="#c8f560"/><path d="M56 74v14M40 90h32"/><path d="M98 10l3 9 9 3-9 3-3 9-3-9-9-3 9-3z" fill="#c8f560"/>',
    # generative AI + design thinking: pen nib on a bezier with handles
    '<path d="M14 78C30 30 70 100 100 36" fill="none"/><circle cx="14" cy="78" r="6" fill="#fff"/><circle cx="100" cy="36" r="6" fill="#c8f560"/><path d="M14 78L34 46M100 36L84 70" stroke-dasharray="3 6"/><rect x="31" y="42" width="8" height="8" rx="2" fill="#ffb4a2"/><rect x="80" y="66" width="8" height="8" rx="2" fill="#ffb4a2"/><path d="M60 10l3 8 8 3-8 3-3 8-3-8-8-3 8-3z" fill="#c8f560"/>',
    # mobile-first banking: phone with card and coin
    '<rect x="34" y="8" width="52" height="86" rx="12" fill="#fff"/><path d="M52 16h16"/><rect x="42" y="34" width="36" height="24" rx="5" fill="#ffb4a2"/><path d="M42 42h36"/><path d="M44 70h32M44 80h20"/><circle cx="94" cy="30" r="12" fill="#c8f560"/><path d="M94 25v10M90 28h6"/>',
    # crowded market: a gem that stands out
    '<path d="M36 36h48l14 18-38 36L22 54z" fill="#c8f560"/><path d="M22 54h76M46 36l-8 18 22 36 22-36-8-18M50 36l10 18 10-18"/><path d="M100 14l2 7 7 2-7 2-2 7-2-7-7-2 7-2zM14 24l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="#ffb4a2"/>',
    # TransferWise to Wise: paper plane over a dotted route
    '<path d="M12 80C30 80 40 50 62 54" stroke-dasharray="2 7"/><path d="M104 18L18 50l30 10 10 30z" fill="#fff"/><path d="M104 18L48 60l10 30 14-22z" fill="#c8f560"/><circle cx="14" cy="80" r="5" fill="#ffb4a2"/>',
    # Revolut brand evolution: pencil sketching a rounded card
    '<rect x="14" y="30" width="72" height="48" rx="12" fill="#fff"/><path d="M14 46h72"/><path d="M26 64h20" /><circle cx="70" cy="64" r="6" fill="#ffb4a2"/><path d="M110 12l-4-4-34 34-4 14 14-4z" fill="#c8f560"/><path d="M72 52l8 8"/>',
]


def short(t, n=4):
    if t.startswith("Mobile-First Banking"):
        n = 3
    w = t.split()
    return t if len(w) <= n else " ".join(w[:n]) + "…"


def blog_section():
    from datetime import date
    posts = "".join(
        f'<a class="post reveal" href="{e(b["url"])}" target="_blank" rel="noopener">'
        f'<h3 title="{e(b["title"])}">{e(short(b["title"]))}</h3><span class="tag">{date.fromisoformat(b["date"]).strftime("%b %Y")}</span>'
        f'<svg class="art" viewBox="0 0 120 100" fill="none" stroke="#16150f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{BLOG_ART[i % len(BLOG_ART)]}</svg></a>'
        for i, b in enumerate(data["blog"])
    )
    return f"""<section id="blog" class="section blog">
    <div class="sec-head reveal"><h2>Notes &amp; <em>writing</em></h2><span class="note n2">on design, fintech &amp; AI</span></div>
    <div class="posts">{posts}</div>
  </section>"""


ICONS = {
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="5"/><path d="M8 10.5v6M8 7.6v.1M12 16.5v-6M12 13c0-1.6 1-2.5 2.3-2.5s1.7 1 1.7 2.3v3.7"/>',
    "behance": '<path d="M3 7h5a2.2 2.2 0 010 4.5H3zM3 11.5h5.5a2.4 2.4 0 010 5H3zM3 7v9.5M14 8.5h6M14.2 13.5h6c0-2-1-3-3-3s-3 1.1-3 3.2 1.1 3.3 3 3.3c1.3 0 2.2-.5 2.7-1.5"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5.5"/><circle cx="12" cy="12" r="4"/><path d="M17.3 6.7v.1"/>',
}


ASSET_V = int(time.time())


def socials():
    out = []
    for k, label in (("linkedin", "LinkedIn"), ("behance", "Behance"), ("instagram", "Instagram")):
        if site.get(k):
            out.append(f'<a href="{e(site[k])}" target="_blank" rel="noopener" aria-label="{label}" title="{label}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg></a>')
    return "".join(out)


def thumb(p):
    t = data["thumbs"].get(p["slug"])
    if not t:
        return (f'<div class="work-art" data-tilt><img src="/assets/img/{p["cover"]}" '
                f'alt="{e(p["title"])} preview" loading="lazy"></div>')

    def img(path, cls, rot, alt=""):
        return (f'<div class="t {cls}" style="--r:{rot}deg"><img src="/assets/img/{path}" '
                f'alt="{e(alt)}" loading="lazy"></div>')

    inner = ""
    if t["type"] == "device":
        fl = t["floats"]
        sattr = f' data-fit style="background:{t["sbg"]}"' if t.get("sbg") else ""
        main = (f'<div class="t photo"><img src="/assets/img/{t["main"]}" alt="{e(p["title"])} main image" loading="lazy"></div>'
                if t.get("plain") else
                f'<div class="laptop"><div class="screen"{sattr}><img src="/assets/img/{t["main"]}" alt="{e(p["title"])} main screen" loading="lazy"></div>'
            '<div class="base"></div></div>')
        inner = (
            main
            + img(fl[0], "f1", 5) + img(fl[1], "f2", -5)
        )
    elif t["type"] == "stat":
        fl = t["floats"]
        inner = (f'<b class="big">{e(t["stat"])}</b><p class="lbl">{e(t["label"])}</p>'
                 + img(fl[0], "f1", 5) + img(fl[1], "f2", -4))
    else:
        a, b, c = t["imgs"]
        inner = img(a, "c1", -5, p["title"]) + img(b, "c2", 6) + img(c, "c3", -2)
    return (f'<div class="work-art stage {t["type"]} s-{p["slug"]}{" cut" if t.get("cut") else ""}" data-tilt style="--stage:{t["stage"]}" '
            f'role="img" aria-label="{e(p["title"])} preview">{inner}</div>')


def index():
    by_slug = {p["slug"]: p for p in projects}
    featured = [by_slug[s] for s in data["featured"]]
    more = [by_slug[s] for s in data["more"]]
    priv = data["private"]
    cards = [f"""
    <a class="work reveal private" href="mailto:{e(site['email'])}?subject=Adobe%20case%20study%20request" style="--tint:#C8F560">
      <div class="work-text">
        <h3>{e(priv['title'])}</h3>
        <p>{e(priv['summary'])}</p>
        <ul class="tags">{''.join(f"<li>{e(t)}</li>" for t in priv['tags'])}</ul>
        <span class="more">{e(priv['note'])} <i>→</i></span>
      </div>
      <div class="work-art lock" data-tilt>
        <span class="note">shh, it's confidential</span>
        <b>Ad<em>obe</em></b>
        <small>{e(priv['kind'])}</small>
      </div>
    </a>"""]
    grid = "".join(f"""
      <a class="tile reveal" data-cat="{p['cat']}" href="/{p['slug']}/" style="--tint:{p['color']}">
        {thumb(p)}
        <div class="tile-info"><h3>{e(p['title'])}</h3><p>{e(p['kind'])}</p><i>→</i></div>
      </a>""" for p in featured + more)
    cards.append(f'<div class="grid">{grid}<p class="empty" hidden>Coming soon — illustrations &amp; art are on the way.</p></div>')

    exp = "".join(f"""
      <li class="reveal">
        <span class="when">{e(x['when'])}</span>
        <div><h4>{e(x['role'])} <em>· {e(x['org'])}</em></h4>
        <p>{e(x['desc'])}</p></div>
        <span class="where">{e(x['where'])}</span>
      </li>""" for x in experience)

    chips = "".join(f'<button class="chip" data-filter="{c["id"]}">{e(c["label"])}</button>' for c in data["categories"])
    marquee_words = ["Product design", "Brand identity", "Research", "Design systems", "AI experiences", "Strategy"]
    marquee = "".join(f"<span>{w}</span><b>✺</b>" for w in marquee_words) * 2
    email = f'<a class="big-link" href="mailto:{e(site["email"])}">{e(site["email"])}</a>' if site["email"] else ""

    return head(site["title"], site["tagline"], projects[0]["cover"]) + f"""
<body>
<div class="grain"></div>
{nav()}
<main>
  <header class="hero" id="top">
    <div class="note n1">hi, I'm Arushi <svg viewBox="0 0 80 40"><path d="M2 8 C30 2 60 12 74 32 M74 32 l-10 -2 M74 32 l-3 -10"/></svg></div>
    <h1>I design things <br>people <em>actually</em> <span class="u">use.</span></h1>
    <p class="lede">{e(site['intro'])}</p>
    <div class="cta"><a class="btn" href="#work">See my work</a><a class="btn ghost" href="#contact">Say hello</a></div>
    <div class="sticker s1" data-drag><span>lead product designer<br>@ Adobe</span></div>
    <div class="sticker s2" data-drag aria-hidden="true"><svg viewBox="0 0 100 100" width="100" height="100" fill="currentColor"><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(0 50 50)"/><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(45 50 50)"/><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(90 50 50)"/><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(135 50 50)"/><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(180 50 50)"/><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(225 50 50)"/><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(270 50 50)"/><ellipse cx="50" cy="24" rx="12" ry="22" transform="rotate(315 50 50)"/><circle cx="50" cy="50" r="13" fill="#c8f560"/></svg></div>
    <div class="sticker s3" data-drag><span>8+ yrs</span></div>
    <div class="sticker s4" data-drag aria-hidden="true"><svg viewBox="0 0 90 90" fill="none" stroke="#16150f" stroke-width="5" stroke-linecap="round"><g class="f f1"><circle cx="31" cy="38" r="4" fill="#16150f" stroke="none"/><circle cx="59" cy="38" r="4" fill="#16150f" stroke="none"/><path d="M26 54Q45 74 64 54"/></g><g class="f f2"><path d="M25 40Q31 32 37 40M53 40Q59 32 65 40"/><path d="M26 52Q45 78 64 52Z" fill="#16150f"/></g><g class="f f3"><circle cx="31" cy="38" r="4" fill="#16150f" stroke="none"/><path d="M53 40h12"/><path d="M26 54Q45 70 64 54"/></g><g class="f f4"><circle cx="31" cy="38" r="4" fill="#16150f" stroke="none"/><circle cx="59" cy="38" r="4" fill="#16150f" stroke="none"/><ellipse cx="45" cy="60" rx="7" ry="9" fill="#16150f"/></g></svg></div>
    <p class="hint">psst — the stickers are draggable</p>
  </header>

  <div class="marquee" aria-hidden="true"><div>{marquee}</div></div>

  <section id="work" class="section">
    <div class="sec-head reveal"><h2>Selected <em>work</em></h2><span class="note n2">recent favourites</span></div>
    <div class="filters reveal" role="group" aria-label="Filter projects"><button class="chip on" data-filter="all">All</button>{chips}</div>
    <div class="works">{''.join(cards)}
    </div>
  </section>

  <section id="about" class="about">
    <div class="about-in">
      <span class="note n3">a bit about me</span>
      <p class="about-big reveal">Bank-teller turned risk analyst turned <em>designer</em>. I don't believe in labels. I believe in <em>recognition</em> for the work I do, and in figuring out what people need.</p>
      <ul class="exp">{exp}
      </ul>
    </div>
    <div class="sticker a1" data-drag><span>ex-bank<br>teller</span></div>
    <div class="sticker a2" data-drag><span>risk<br>analyst</span></div>
    <div class="sticker a3" data-drag aria-hidden="true">✦</div>
    <div class="sticker a4" data-drag><span>now:<br>designer</span></div>
  </section>

  {life_section()}

  {blog_section()}

  <section id="contact" class="contact">
    <p class="note n4">currently seeking new opportunities · Adobe case study available on request</p>
    <h2 class="reveal">Work with <em>me.</em></h2>
    {email}
    <div class="social">{socials()}</div>
    <div class="sticker c2" data-drag data-pop><span>let's<br>talk!</span></div>
    <div class="sticker c3" data-drag data-pop aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6 5L17.5 10.5L12.5 12.5L10.5 17.5Z" fill="#1f2bff" stroke="#1f2bff" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/></svg></div>
  </section>
</main>
<footer><span>© {2026} Arushi</span><span>Designed &amp; built by hand</span></footer>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def project_page(i, p):
    meta = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["meta"].items())
    stats = ""
    if p.get("stats"):
        stats = '<div class="stats">' + "".join(
            f'<div class="reveal"><b>{e(n)}</b><span>{e(l)}</span></div>' for n, l in p["stats"]
        ) + "</div>"
    blocks = ""
    for key, label in (("challenge", "The challenge"), ("insight", "Key insight"), ("vision", "Vision"), ("mission", "Mission")):
        if p.get(key):
            blocks += f'<div class="block reveal"><h3>{label}</h3><p>{e(p[key])}</p></div>'
    shots = images[p["slug"]]
    gallery = "".join(
        f'<figure class="shot reveal"><img src="/{s["file"]}" alt="{e(p["title"])} — image {n}" '
        f'width="{s.get("w", "")}" height="{s.get("h", "")}" loading="lazy"></figure>'
        for n, s in enumerate(shots, 1)
    )
    nxt = projects[(i + 1) % len(projects)]
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    return head(f"{p['title']} — Arushi", p["summary"], p["cover"]) + f"""
<body class="case" style="--tint:{p['color']}">
<div class="grain"></div>
{nav('work')}
<main>
  <header class="case-hero">
    <a class="back" href="/#work">← All work</a>
    <span class="note n1">{e(p['kind'])}</span>
    <h1>{e(p['title'])}</h1>
    <p class="lede">{e(p['intro'])}</p>
    <ul class="tags">{tags}</ul>
    <dl class="meta">{meta}</dl>
  </header>
  {stats}
  <section class="blocks">{blocks}</section>
  <section class="gallery">{gallery}</section>
  <a class="next" href="/{nxt['slug']}/" style="--tint:{nxt['color']}">
    <span class="note">up next</span>
    <h2>{e(nxt['title'])} <i>→</i></h2>
  </a>
</main>
<footer><span>© 2026 Arushi</span><span><a href="/#contact">Let's talk</a></span></footer>
<div class="lightbox" hidden><img alt=""></div>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)


write(f"{ROOT}/index.html", index())
for i, p in enumerate(projects):
    shutil.rmtree(f"{ROOT}/{p['slug']}", ignore_errors=True)
    write(f"{ROOT}/{p['slug']}/index.html", project_page(i, p))
write(f"{ROOT}/.nojekyll", "")
print("built", 1 + len(projects), "pages")
