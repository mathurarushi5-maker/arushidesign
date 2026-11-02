"""Generates the static site from content/site.json and content/images.json.

Usage: python3 tools/build.py
"""
import json
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
<link rel="stylesheet" href="/assets/css/style.css">
</head>"""


def nav(active=""):
    def a(href, label, key):
        cls = ' class="on"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'

    return f"""<nav class="pill" aria-label="Main">
  <a class="dot" href="/" aria-label="Home"></a>
  {a('/#work', 'Work', 'work')}
  {a('/#about', 'About', 'about')}
  {a('/#contact', 'Contact', 'contact')}
</nav>"""


def socials():
    out = []
    for k, label in (("linkedin", "LinkedIn"), ("behance", "Behance"), ("instagram", "Instagram")):
        if site.get(k):
            out.append(f'<a href="{e(site[k])}" target="_blank" rel="noopener">{label}</a>')
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
        inner = (
            f'<div class="laptop"><div class="screen"><img src="/assets/img/{t["main"]}" alt="{e(p["title"])} main screen" loading="lazy"></div>'
            '<div class="base"></div></div>'
            + img(fl[0], "f1", 5) + img(fl[1], "f2", -5)
        )
    elif t["type"] == "stat":
        fl = t["floats"]
        inner = (f'<b class="big">{e(t["stat"])}</b><p class="lbl">{e(t["label"])}</p>'
                 + img(fl[0], "f1", 5) + img(fl[1], "f2", -4))
    else:
        a, b, c = t["imgs"]
        inner = img(a, "c1", -5, p["title"]) + img(b, "c2", 6) + img(c, "c3", -2)
    return (f'<div class="work-art stage {t["type"]}" data-tilt style="--stage:{t["stage"]}" '
            f'role="img" aria-label="{e(p["title"])} preview">{inner}</div>')


def index():
    by_slug = {p["slug"]: p for p in projects}
    featured = [by_slug[s] for s in data["featured"]]
    more = [by_slug[s] for s in data["more"]]
    priv = data["private"]
    cards = [f"""
    <a class="work reveal private" href="mailto:{e(site['email'])}?subject=Adobe%20case%20study%20request" style="--tint:#C8F560">
      <div class="work-text">
        <span class="num">01</span>
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
    for i, p in enumerate(featured, start=1):
        flip = " flip" if i % 2 else ""
        tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
        cards.append(f"""
    <a class="work reveal{flip}" href="/{p['slug']}/" style="--tint:{p['color']}">
      <div class="work-text">
        <span class="num">{i + 1:02d}</span>
        <h3>{e(p['title'])}</h3>
        <p>{e(p['summary'])}</p>
        <ul class="tags">{tags}</ul>
        <span class="more">View case study <i>→</i></span>
      </div>
      {thumb(p)}
    </a>""")

    more_rows = "".join(f"""
      <a class="more-row reveal" href="/{p['slug']}/" style="--tint:{p['color']}">
        <img src="/assets/img/{p['cover']}" alt="" loading="lazy">
        <h3>{e(p['title'])}</h3>
        <span>{e(p['kind'])}</span>
        <i>→</i>
      </a>""" for p in more)

    exp = "".join(f"""
      <li class="reveal">
        <span class="when">{e(x['when'])}</span>
        <div><h4>{e(x['role'])} <em>· {e(x['org'])}</em></h4>
        <p>{e(x['desc'])}</p></div>
        <span class="where">{e(x['where'])}</span>
      </li>""" for x in experience)

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
    <div class="sticker s2" data-drag aria-hidden="true">✺</div>
    <div class="sticker s3" data-drag><span>8+ yrs</span></div>
    <div class="sticker s4" data-drag aria-hidden="true"></div>
    <p class="hint">psst — the stickers are draggable</p>
  </header>

  <div class="marquee" aria-hidden="true"><div>{marquee}</div></div>

  <section id="work" class="section">
    <div class="sec-head reveal"><h2>Selected <em>work</em></h2><span class="note n2">recent favourites</span></div>
    <div class="works">{''.join(cards)}
    </div>
    <div class="more-work">
      <h3 class="reveal">More <em>work</em></h3>
      {more_rows}
    </div>
  </section>

  <section id="about" class="about">
    <div class="about-in">
      <span class="note n3">a bit about me</span>
      <p class="about-big reveal">Bank-teller turned risk analyst turned <em>designer</em>. I don't believe in labels. I believe in <em>recognition</em> for the work I do, and in figuring out what people need.</p>
      <ul class="exp">{exp}
      </ul>
    </div>
  </section>

  <section id="contact" class="contact">
    <p class="note n4">currently seeking new opportunities · Adobe case study available on request</p>
    <h2 class="reveal">Work with <em>me.</em></h2>
    {email}
    <div class="social">{socials()}</div>
  </section>
</main>
<footer><span>© {2026} Arushi</span><span>Designed &amp; built by hand</span></footer>
<script src="/assets/js/main.js" defer></script>
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
<script src="/assets/js/main.js" defer></script>
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
