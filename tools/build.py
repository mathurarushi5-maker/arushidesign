"""Generates the static site from content/site.json and content/images.json.

Usage: python3 tools/build.py
"""
import glob
import re
import json
import time
import html
import os
import shutil
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decor
import decor_cozy

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


def hl(t, words):
    for w in words:
        t = t.replace(w, '<mark class="hl">' + w + '</mark>', 1)
    return t.replace('to product designer', 'to <mark class="hl">product designer</mark>', 1)

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
<script>if(/[?&]embed/.test(location.search))document.documentElement.classList.add("embed");try{{var t=localStorage.getItem("theme");if(t&&t!=="cream")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="icon" href="/assets/favicon.png" type="image/png">
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
</nav>
<div class="themer" data-themer role="group" aria-label="Pick your vibe">
  <span class="themer-label">pick your vibe</span>
  <button data-set-theme="cream" aria-label="Cream theme" data-name="Cream" style="--a:#f6f1e7;--b:#1f2bff"></button>
  <button data-set-theme="midnight" aria-label="Midnight theme" data-name="Midnight" style="--a:#14131c;--b:#7c85ff"></button>
  <button data-set-theme="sunset" aria-label="Sunset theme" data-name="Sunset" style="--a:#fff1e6;--b:#e4442b"></button>
  <button data-set-theme="mint" aria-label="Mint theme" data-name="Mint" style="--a:#eaf6ee;--b:#0e7a5a"></button>
  <button data-set-theme="lilac" aria-label="Lilac theme" data-name="Lilac" style="--a:#f1ecff;--b:#6a3df5"></button>
  <button data-set-theme="mono" aria-label="Noir theme" data-name="Noir" style="--a:#fff;--b:#000"></button>
</div>"""


FACT_ICONS = [
    '<path d="M8 14c8-4 17-3 24 2 7-5 16-6 24-2v34c-8-4-17-3-24 2-7-5-16-6-24-2z"/><path d="M32 16v34"/><path d="M14 22c5-1.500 9-1 13 1M14 30c5-1.500 9-1 13 1M37 23c4-2 8-2.500 13-1M37 31c4-2 8-2.500 13-1"/>',
    '<path d="M46 8c6 4 8 10 4 16L30 44l-12 4 4-12z"/><path d="M40 14l8 8M12 56c6 0 6-4 12-4s6 4 12 4 6-4 12-4"/>',
    '<path d="M32 8C17 8 8 19 8 31c0 11 8 19 18 19 4 0 5-3 3-6-2-4 0-8 5-8h8c7 0 12-4 12-11C54 16 44 8 32 8z"/><circle cx="19" cy="30" r="3.500"/><circle cx="28" cy="19" r="3.500"/><circle cx="41" cy="20" r="3.500"/>',
    '<path d="M26 8c1 10 4 13 14 14-10 1-13 4-14 14-1-10-4-13-14-14 10-1 13-4 14-14z"/><path d="M46 34c.700 6 2.500 8 8 9-5.500 1-7.300 3-8 9-.700-6-2.500-8-8-9 5.500-1 7.300-3 8-9z"/>',
]


def life_section():
    return """<section id="life" class="life otc-sec">
    <iframe class="otc" src="/assets/off-the-clock.html?v=""" + str(ASSET_V) + """" title="Beyond the portfolio: off the clock" loading="lazy"></iframe>
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


HOME_POSTS = 5
NUM = re.compile(r"^\d+\. ")


def load_posts():
    """Reads content/blog/*.md. Only published, non-future posts are returned, newest first."""
    from datetime import date
    out = []
    for f in sorted(glob.glob(f"{ROOT}/content/blog/*.md")):
        slug = os.path.basename(f)[:-3]
        raw = open(f, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        if not m:
            sys.exit(f"blog/{slug}.md: missing front matter (--- ... ---)")
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        for req in ("title", "date"):
            if not meta.get(req):
                sys.exit(f"blog/{slug}.md: '{req}' is required")
        try:
            d = date.fromisoformat(meta["date"])
        except ValueError:
            sys.exit(f"blog/{slug}.md: date must be YYYY-MM-DD")
        if meta.get("status", "draft").lower() != "published" or d > date.today():
            continue
        body = m.group(2).strip()
        meta.update(slug=slug, d=d, body=body)
        meta.setdefault("summary", "")
        out.append(meta)
    out.sort(key=lambda x: x["d"], reverse=True)
    return out


def md_inline(t):
    t = e(t, quote=False)
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")


def md_html(src):
    out = []
    for blk in re.split(r"\n{2,}", src.strip()):
        blk = blk.strip()
        if not blk:
            continue
        lines = blk.splitlines()
        if blk.startswith("!["):
            out.append(f'<figure>{md_inline(blk)}</figure>')
        elif re.match(r"#{1,6} ", blk):
            lvl = min(len(blk.split()[0]) + 1, 4)
            out.append(f"<h{lvl}>{md_inline(blk.lstrip('# ').strip())}</h{lvl}>")
        elif all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{md_inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"\d+\. ", l) for l in lines):
            out.append("<ol>" + "".join("<li>" + md_inline(NUM.sub("", l)) + "</li>" for l in lines) + "</ol>")
        elif blk.startswith("> "):
            out.append("<blockquote>" + md_inline(" ".join(l.lstrip("> ") for l in lines)) + "</blockquote>")
        else:
            out.append(f"<p>{md_inline(blk)}</p>")
    return "\n".join(out)


def blog_section():
    allp = load_posts()
    posts = "".join(
        f'<a class="post reveal" href="/blog/{b["slug"]}/">'
        f'<h3 title="{e(b["title"])}">{e(short(b["title"]))}</h3><span class="tag">{b["d"].strftime("%b %Y")}</span>'
        f'<svg class="art" viewBox="0 0 120 100" fill="none" stroke="#16150f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{BLOG_ART[i % len(BLOG_ART)]}</svg></a>'
        for i, b in enumerate(allp[:HOME_POSTS])
    )
    more = '<a class="blog-all" href="/blog/">All posts &rarr;</a>' if len(allp) > HOME_POSTS else ""
    return f"""<section id="blog" class="section blog">
    <div class="sec-head reveal"><h2>Blog &amp; <em>writing</em></h2><span class="note n2">on design, fintech &amp; AI</span></div>
    <div class="posts">{posts}</div>
    {more}
  </section>"""


def blog_shell(title, desc, body, og=None):
    return head(title, desc, None) + f"""
<body class="blogpage">
<div class="grain"></div>
{nav('blog')}
<main>
{body}
</main>
<footer><span>© 2026 Arushi</span><span><a href="/#contact">Let's talk</a></span></footer>
<div class="lightbox" hidden><img alt=""></div>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def blog_index_page():
    rows = "".join(
        f'<a class="bl-row" href="/blog/{b["slug"]}/"><span class="bl-date">{b["d"].strftime("%b %Y")}</span>'
        f'<span class="bl-main"><h2>{e(b["title"])}</h2><p>{e(b["summary"])}</p></span><i>&rarr;</i></a>'
        for b in load_posts()
    )
    body = f"""<header class="bl-head"><a class="back" href="/#blog">← Home</a><h1>Blog &amp; <em>writing</em></h1><p class="lede">On design, fintech &amp; AI.</p></header>
<section class="bl-list">{rows}</section>"""
    return blog_shell("Blog — Arushi", "Writing on design, fintech and AI.", body)


def short_txt(t, n=110):
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


def blog_post_page(i, b, allp):
    cover = ""
    if b.get("cover") and os.path.exists(f"{ROOT}{b['cover']}"):
        cover = f'<img class="bp-cover" src="{e(b["cover"])}" alt="">'
    def card(p, label, cls):
        img = p.get("cover") if p.get("cover") and os.path.exists(f"{ROOT}{p['cover']}") else ""
        th = f'<img src="{e(img)}" alt="" loading="lazy">' if img else ""
        return (f'<div class="bp-col {cls}"><span class="note">{label}</span><a class="bp-card" href="/blog/{p["slug"]}/"><span class="bpc-img">{th}</span>'
                f'<span class="bpc-txt"><h3>{e(p["title"])}</h3>'
                f'<p>{e(short_txt(p["summary"], 80))}</p></span></a></div>')
    prv = allp[i - 1] if i > 0 else None
    nxt = allp[i + 1] if i + 1 < len(allp) else None
    cards = (card(prv, "← previous", "is-prev") if prv else "") + (card(nxt, "next →", "is-next") if nxt else "")
    nx = f'<nav class="bp-nav">{cards}</nav>' if cards else ""
    body = f"""<article class="bp">
  <header class="bp-head">
    <a class="back" href="/blog/">← All posts</a>
    <span class="note n1">{b["d"].strftime("%d %b %Y").lstrip("0")}</span>
    <h1>{e(b["title"])}</h1>
  </header>
  {cover}
  <div class="bp-body">
{md_html(b["body"])}
  </div>
</article>
{nx}"""
    return blog_shell(f"{b['title']} — Arushi", b["summary"], body)


def redirect_page(to):
    return (f'<!doctype html><meta charset="utf-8"><title>Redirecting…</title>'
            f'<link rel="canonical" href="{to}"><meta http-equiv="refresh" content="0;url={to}">'
            f'<script>location.replace("{to}")</script><a href="{to}">Continue</a>')


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

    PINS = {
      "work": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/></svg>',
      "grad": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.500 6-3v-4.500M22 9v6"/></svg>',
    }
    exp = "".join(f"""
      <li>
        <i class="pin" aria-hidden="true">{PINS.get(x.get('icon','work'))}</i>
        <span class="when">{e(x['when'])}</span>
        <div><span class="when2">{e(x['when'])}</span><h4>{e(x['role'])} <em>· {e(x['org'])}</em></h4>
        <span class="loc">{x.get('flag','')} {e(x.get('loc',''))}</span>
        <p>{e(x['desc'])}</p></div>
        <span class="where">{e(x['where'])}</span>
      </li>""" for x in experience)

    chips = "".join(f'<button class="chip" data-filter="{c["id"]}">{e(c["label"])}</button>' for c in data["categories"])
    marquee_words = ["Product design", "B2B / B2C", "UX research", "Generative AI", "Design systems", "Human-centric AI", "Design strategy", "Brand identity", "Illustration & art", "Team leadership"]
    marquee = "".join(f"<span>{w}</span><b>✺</b>" for w in marquee_words) * 2
    email = f'<a class="big-link" href="mailto:{e(site["email"])}">{e(site["email"])}</a>' if site["email"] else ""

    return head(site["title"], site["tagline"], projects[0]["cover"]) + f"""
<body>
<div class="grain"></div>
{nav()}
<main>
  <header class="hero" id="top">
    <div class="note n1">hi, I'm Arushi <svg viewBox="0 0 80 40"><path d="M2 8 C30 2 60 12 74 32 M74 32 l-10 -2 M74 32 l-3 -10"/></svg></div>
    <h1>I design things <br>people <em>actually</em> <span class="u">use.</span><span class="h1-sub">And a few they just like.</span></h1>
    <p class="lede">{hl(e(site['intro']), ["lead product designer", "8+ years", "retail banker", "what people need"])}</p>
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
    <div class="works">{''.join(cards)}
    </div>
  </section>

  <section id="about" class="about">
    <div class="about-in">
      <span class="note n3">a bit about me</span>
      <p class="about-big reveal">Bank-teller turned risk analyst turned <em>designer</em>. I don't believe in labels. I believe in <em>recognition</em> for the work I do, and in figuring out what people <span class="need">need.</span></p>
      <div class="jv" id="jv" hidden></div>
      <div class="exp-wrap">
      <ul class="exp" data-v="path">{exp}
      </ul></div>
      <script src="/assets/js/journey-v.js?v={ASSET_V}" defer></script>
    </div>
    <div class="sticker a1" data-drag><span>ex-bank<br>teller</span></div>
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


def cover_colors(path):
    """Spine colours taken from the cover: dominant saturated colour, a second accent, and a readable text colour."""
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB").resize((40, 60))
    except Exception:
        return None
    buckets = {}
    for r, g, b in im.getdata():
        mx, mn = max(r, g, b), min(r, g, b)
        w = 1 + 3 * (mx - mn) / (mx or 1) + (0.5 if 50 < mx < 235 else 0)
        a = buckets.setdefault((r // 40, g // 40, b // 40), [0, 0, 0, 0, 0])
        a[0] += w; a[1] += 1; a[2] += r; a[3] += g; a[4] += b
    top = sorted(buckets.values(), reverse=True)[:2]
    avg = lambda a: tuple(round(a[i] / a[1]) for i in (2, 3, 4))
    c1 = avg(top[0]); c2 = avg(top[-1])
    lum = lambda c: (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2])
    fg = "#16150f" if lum(c1) > 140 else "#fbf6ea"
    hx = lambda c: "#%02x%02x%02x" % c
    return hx(c1), fg, hx(c2)


def cozy_rows(sp):
    flame = lambda x, y, d: f'<g transform="translate({x} {y})"><path d="M0 0C-4.5 -6 -2.5 -12 0 -17C2.5 -12 4.5 -6 0 0z" fill="#ffd36e"><animateTransform attributeName="transform" type="scale" values="1 1;.88 1.14;1.06 .94;1 1" dur="{d}s" repeatCount="indefinite"/></path><path d="M0 -1C-2 -4 -1 -8 0 -10C1 -8 2 -4 0 -1z" fill="#fff4c9"/></g>'
    glow = lambda x, y: f'<circle cx="{x}" cy="{y}" r="16" fill="#ffe6a0" opacity=".35"><animate attributeName="opacity" values=".25;.45;.3;.25" dur="2.6s" repeatCount="indefinite"/></circle>'
    bookend = lambda flip="": f'<svg class="deco bookend {flip}" viewBox="0 0 40 110" aria-hidden="true"><defs><linearGradient id="beg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b9573a"/><stop offset=".45" stop-color="#ee9d7c"/><stop offset="1" stop-color="#a94d33"/></linearGradient><linearGradient id="beb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8b04f"/><stop offset="1" stop-color="#9a6a1c"/></linearGradient></defs><ellipse cx="20" cy="106" rx="19" ry="3" fill="#000" opacity=".2"/><path d="M14 98 V20 Q14 4 26 4 Q36 4 36 18 V98z" fill="url(#beg)"/><path d="M19 22 V92" stroke="#fff" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/><path d="M14 40 H36 M14 60 H36" stroke="#7d3a26" stroke-opacity=".35" stroke-width="1.5"/><path d="M26 12 l3 5 -3 5 -3 -5z" fill="url(#beb)"/><rect x="2" y="96" width="36" height="9" rx="3" fill="url(#beb)"/><rect x="2" y="96" width="36" height="3" rx="1.5" fill="#fff" opacity=".35"/></svg>'
    candles = '<svg class="deco candles" viewBox="0 0 76 100" aria-hidden="true"><ellipse cx="38" cy="96" rx="34" ry="4" fill="#000" opacity=".12"/><rect x="6" y="90" width="64" height="8" rx="3" fill="#caa070"/><rect x="12" y="36" width="20" height="54" rx="3" fill="#fbf1de"/><rect x="12" y="36" width="6" height="54" rx="3" fill="#fff" opacity=".6"/><rect x="42" y="56" width="20" height="34" rx="3" fill="#f6c9c4"/><rect x="42" y="56" width="6" height="34" rx="3" fill="#fff" opacity=".45"/><path d="M22 36 v-5 M52 56 v-5" stroke="#6b4a33" stroke-width="2"/>' + glow(22, 22) + glow(52, 44) + flame(22, 31, 1.9) + flame(52, 51, 2.4) + '</svg>'
    jar = '<svg class="deco jar" viewBox="0 0 44 50" aria-hidden="true"><rect x="6" y="20" width="32" height="28" rx="6" fill="#cfe6dc" opacity=".9"/><rect x="9" y="26" width="26" height="19" rx="3" fill="#fbe6c8"/><path d="M12 22 v22" stroke="#fff" stroke-width="3" opacity=".6" stroke-linecap="round"/><rect x="8" y="16" width="28" height="6" rx="2" fill="#caa070"/><path d="M22 26 v-4" stroke="#6b4a33" stroke-width="2"/>' + glow(22, 10) + flame(22, 20, 2.1) + '</svg>'
    stack = lambda items, top="": '<div class="hstack">' + ''.join(f'<span class="fl">{x}</span>' for x in items) + top + '</div>'
    row = lambda *c: '<div class="srow">' + ''.join(c) + '</div>'
    lean = lambda x: x.replace('class="bk-w"', 'class="bk-w lean"', 1)
    flat = lambda x: x.replace('class="bk-w"', 'class="bk-w flat"', 1)
    return (
        row(*sp[0:8], candles)
        + row(*sp[8:14], stack([flat(x) for x in (sp[16], sp[15], sp[14])], jar))
        + row(*sp[17:21], lean(sp[21]), jar, candles)
    ).replace('<div class="srow">', '<div class="srow">')


PAL = [("#D2F26F", "#16150f", "#16150f"), ("#F4B3A3", "#16150f", "#16150f"), ("#2233FF", "#fff", "#D2F26F")]
ROT = ["-1.6deg", "1.2deg", "-0.8deg"]
RAD = ["28px 14px 26px 16px", "14px 28px 16px 26px", "24px 18px 30px 14px"]


def library_page():
    lib = json.load(open(f"{ROOT}/content/library.json", encoding="utf-8"))
    byt = {b["title"]: b for b in lib["books"]}
    cards = ""
    for i, s in enumerate(lib["shelf"]):
        b = byt[s["title"]]
        cc = cover_colors(f"{ROOT}{b['cover']}") or ("#d2f26f", "#16150f", "#16150f")
        cards += (
            f'<article class="rl-card" style="--bg:{PAL[i%3][0]};--fg:{PAL[i%3][1]};--hc:{PAL[i%3][2]};--r:{ROT[i%3]};--rad:{RAD[i%3]};--i:{i}">'
            f'<div class="rl-cv"><img src="{e(b["cover"])}" alt="Cover of {e(b["title"])}"></div>'
            f'<div class="rl-info"><h3 class="rl-l">{e(s["label"])}</h3><h2>{e(b["title"])}</h2><p>by {e(b["author"])}</p></div></article>'
        )
    return head("Library — Arushi", lib["intro"]) + f"""
<body class="lib-page rl-page">
{nav('life')}
<main class="rl">
  <header class="rl-head">
    <a class="back" href="/#life">← Beyond the portfolio</a>
    <div class="lib-title"><h1>{e(lib['title'])}</h1><span class="note n3">always reading</span></div>
    <p class="lede">{e(lib['intro'])}</p>
  </header>
  <section class="rl-row" aria-label="Reading list">{cards}</section>
</main>
<footer><span>© 2026 Arushi</span><span><a href="/#life">Back to Off the clock</a></span></footer>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def poems_page():
    pm = json.load(open(f"{ROOT}/content/poems.json", encoding="utf-8"))
    pj = json.dumps(pm["poems"], ensure_ascii=False).replace("</", "<\\/")
    return head("Poems — Arushi", pm["intro"]) + f"""
<body class="pm-page">
{nav('life')}
<main class="pm">
  <header class="pm-head">
    <a class="back" href="/#life">← Beyond the portfolio</a>
    <div class="pm-title"><h1>{e(pm['title'])}</h1><span class="note n3">poetry on the side</span></div>
    <p class="lede">{e(pm['intro'])}</p>
    <p class="pm-count"><b id="poemN">{len(pm['poems'])}</b> poems</p>
  </header>
  <div class="pm-grid" id="poemGrid"></div>
  <p class="pm-hint">move your cursor left or right to flip through ↔</p>
  <section class="pm-desk" id="pmDesk" hidden aria-label="Poetry notebook on a desk">
    <svg class="dk dk-pencil" viewBox="0 0 220 28" aria-hidden="true"><path d="M8 14 L34 3 H196 a8 8 0 0 1 0 22 H34 Z" fill="#ffe27a" stroke="#16150f" stroke-width="3" stroke-linejoin="round"/><path d="M8 14 L34 3 V25 Z" fill="#f2d3a8" stroke="#16150f" stroke-width="3" stroke-linejoin="round"/><path d="M8 14 L18 9.5 V18.5 Z" fill="#16150f"/><rect x="190" y="3" width="26" height="22" rx="8" fill="#ffb4a2" stroke="#16150f" stroke-width="3"/><path d="M60 8 H180 M60 20 H180" stroke="#16150f" stroke-width="2" opacity=".35"/></svg>
    <svg class="dk dk-mug" viewBox="0 0 150 120" aria-hidden="true"><path d="M112 40 a26 26 0 0 1 0 46" fill="none" stroke="#16150f" stroke-width="14" stroke-linecap="round"/><path d="M112 40 a26 26 0 0 1 0 46" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/><circle cx="62" cy="62" r="52" fill="#fff" stroke="#16150f" stroke-width="3.5"/><circle cx="62" cy="62" r="42" fill="#a9d8ff" stroke="#16150f" stroke-width="3"/><circle cx="62" cy="62" r="34" fill="#6b4331"/><path d="M42 54 q20 -14 40 0" fill="none" stroke="#c8a083" stroke-width="3" stroke-linecap="round"/></svg>
    <svg class="dk dk-clip" viewBox="0 0 40 90" aria-hidden="true"><path d="M12 72 V22 a8 8 0 0 1 16 0 V74 a12 12 0 0 1 -24 0 V28" fill="none" stroke="#16150f" stroke-width="3.5" stroke-linecap="round"/></svg>
  </section>
  <p class="pm-empty" hidden>Poems are on their way. Check back soon.</p>
  <noscript><p>Please enable JavaScript to read the poems.</p></noscript>
  <div class="pm-admin" hidden>
    <b>Edit mode</b> <span>Changes show only in this browser until you export poems.json and replace content/poems.json.</span>
    <form><input type="text" name="title" placeholder="Title" required><input type="text" name="date" placeholder="Date, e.g. March 2025"><textarea name="text" placeholder="The poem (line breaks are kept)" required></textarea>
    <label><input type="checkbox" name="published"> Published somewhere</label><input type="text" name="link" placeholder="Link to where it was published (optional)">
    <button>Add poem</button></form>
    <div><button class="pm-export">Export poems.json</button> <button class="pm-reset">Discard my edits</button></div>
  </div>
</main>
<div class="pm-pop" id="pmPop" hidden role="dialog" aria-modal="true" aria-label="Poem">
  <div class="pm-sheet"><button class="pm-x" aria-label="Close">×</button>
    <h2 class="pm-h"></h2><div class="pm-d"></div><span class="pm-b">★ published</span><a class="pm-l" target="_blank" rel="noopener">read it where it was published →</a>
    <div class="pm-t"></div>
    <button class="pm-del" hidden>Remove this poem</button>
    <div class="pm-nav"><button class="pm-prev">← previous</button><button class="pm-next">next →</button></div></div>
</div>
<footer><span>© 2026 Arushi</span><span><a href="/#life">Back to Off the clock</a></span></footer>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
<script>window.__POEMS={pj};</script>
<script src="/assets/js/poems.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def gallery_page():
    g = json.load(open(f"{ROOT}/content/gallery.json", encoding="utf-8"))
    gj = json.dumps(g["items"], ensure_ascii=False).replace("</", "<\\/")
    return head("Pen & colors — Arushi", g["intro"]) + f"""
<body class="gl-page">
{nav('life')}
<main class="gl">
  <header class="gl-head">
    <a class="back" href="/#life">← Beyond the portfolio</a>
    <div class="gl-title"><h1>{e(g['title'])}</h1><span class="note n3">hands busy, eye sharp</span></div>
    <p class="lede">{e(g['intro'])}</p>
    <div class="gl-filters" role="group" aria-label="Filter">
      <button class="on" data-f="all">All</button><button data-f="pencil">Pen</button><button data-f="paint">Colors</button>
      <span class="gl-count"><b id="glN">0</b> pieces</span>
    </div>
  </header>
  <section class="gl-wall" id="glWall" aria-label="Art wall"></section>
  <p class="gl-empty" hidden>The wall is being hung. Check back soon.</p>
  <noscript><p>Please enable JavaScript to see the art.</p></noscript>
  <div class="gl-admin" hidden>
    <b>Edit mode</b> <span>Put image files in assets/art/, add them here, then export gallery.json and replace content/gallery.json. Changes show only in this browser until then.</span>
    <form><input type="text" name="title" placeholder="Title" required><input type="text" name="image" placeholder="Image path, e.g. /assets/art/cat.jpg">
    <select name="medium"><option value="pencil">Pen</option><option value="paint">Colors</option></select>
    <input type="text" name="year" placeholder="Year"><input type="text" name="note" placeholder="Short note (optional)">
    <label><input type="checkbox" name="wip"> Work in progress</label><button>Add piece</button></form>
    <div><button class="gl-export">Export gallery.json</button> <button class="gl-reset">Discard my edits</button></div>
  </div>
</main>
<div class="gl-lb" id="glLb" hidden role="dialog" aria-modal="true" aria-label="Artwork">
  <button class="gl-x" aria-label="Close">×</button><button class="gl-prev" aria-label="Previous">←</button><button class="gl-next" aria-label="Next">→</button>
  <figure><div class="gl-img"></div><figcaption><h2></h2><p class="gl-meta"></p><p class="gl-note"></p><button class="gl-del" hidden>Remove this piece</button></figcaption></figure>
</div>
<div class="es" id="es" hidden aria-label="Artwork on an easel">
  <div class="es-stage">
    <svg class="es-legs" viewBox="0 0 300 450" aria-hidden="true">
      <g stroke-linecap="round"><path d="M150 190 L150 430" stroke="#16150f" stroke-width="14"/><path d="M150 190 L150 430" stroke="#9c6a40" stroke-width="8"/>
      <path d="M70 20 L28 440" stroke="#16150f" stroke-width="18"/><path d="M70 20 L28 440" stroke="#b98355" stroke-width="12"/>
      <path d="M230 20 L272 440" stroke="#16150f" stroke-width="18"/><path d="M230 20 L272 440" stroke="#b98355" stroke-width="12"/>
      <path d="M44 372 L256 372" stroke="#16150f" stroke-width="14"/><path d="M44 372 L256 372" stroke="#9c6a40" stroke-width="8"/></g>
      <rect x="24" y="298" width="252" height="16" rx="6" fill="#b98355" stroke="#16150f" stroke-width="3.5"/>
      <rect x="96" y="10" width="108" height="18" rx="6" fill="#b98355" stroke="#16150f" stroke-width="3.5"/>
    </svg>
    <div class="es-canvas"><img id="esImg" alt=""></div>
    <div class="es-cap"><span id="esCap"></span></div>
    <button class="es-nav es-prev" aria-label="Previous">←</button><button class="es-nav es-next" aria-label="Next">→</button>
  </div>
</div>
<footer><span>© 2026 Arushi</span><span><a href="/#life">Back to Off the clock</a></span></footer>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
<script>window.__ART={gj};</script>
<script src="/assets/js/easel.js?v={ASSET_V}" defer></script>
<script src="/assets/js/gallery.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


from lab_art import GARLAND, HANG1, HANG2, VINE, DOODLES, MUG, MONSTERA, VASE, DISH


SCREEN_SPOTS = [
 ("moodboard","Moodboard",[(170,245),(395,225),(400,208),(565,205),(570,265),(603,300),(603,420),(560,440),(235,478),(210,470)]),
 ("wireframe","Wireframe",[(607,205),(885,180),(920,383),(648,420)]),
 ("sketch","Sketch",[(220,515),(405,490),(418,595),(245,630)]),
 ("concept","Concept",[(440,490),(580,470),(608,590),(460,620)]),
 ("landscape","Landscape",[(610,475),(752,445),(770,560),(630,592)]),
 ("mockup","Mockup",[(790,440),(925,422),(948,530),(810,558)]),
 ("code","Code",[(248,645),(430,630),(443,700),(430,745),(262,763),(248,700)]),
 ("build","Build",[(820,580),(880,578),(885,640),(822,648)]),
 ("flow","Flow",[(905,568),(962,563),(968,625),(910,632)]),
]
def screen_links(links):
    out=[]
    for k,label,pts in SCREEN_SPOTS:
        poly=" ".join(f"{580+x/3:.0f},{490+y/3:.0f}" for x,y in pts)
        l=links.get(k,{})
        u=l.get("url",""); name=l.get("name","")
        href=f' href="{e(u)}" target="_blank" rel="noopener"' if u else ''
        aria=f' aria-label="{e(name)}"' if name else ' aria-hidden="true" tabindex="-1"'
        tag=""
        if name:
            cx=sum(580+x/3 for x,_ in pts)/len(pts); ty=min(490+y/3 for _,y in pts)
            w=len(name)*7+18
            tag=f'<g class="tag" transform="translate({cx:.0f},{ty-6:.0f})"><rect x="{-w/2:.0f}" y="-20" width="{w}" height="20" rx="10"/><text y="-6" text-anchor="middle">{e(name)}</text></g>'
        out.append(f'<a{href}{aria}><polygon points="{poly}"/>{tag}</a>')
    return '<svg class="sc-links" viewBox="0 0 1536 1024" preserveAspectRatio="none">'+"".join(out)+'</svg>'

def lab_page(v2=False):
    g = json.load(open(f"{ROOT}/content/lab.json", encoding="utf-8"))
    gj = json.dumps(g["items"], ensure_ascii=False).replace("</", "<\\/")
    return head("Lab — Arushi", g["intro"]).replace("</head>", f'<link rel="stylesheet" href="/assets/css/lab2.css?v={ASSET_V}">\n</head>') + f"""
<body>
<div class="grain"></div>
{nav('life')}
<main class="li">
  <div class="li-top"><a class="li-back" href="/#life">← Beyond the portfolio</a></div>
  <h1>{e(g['title'])} <span class="note">ai tinkering</span></h1>
  <p class="li-sub">{e(g['intro'])}</p>
  <div id="views"></div>
  <span class="sample">Entries marked “Sample …” are placeholders until I add real experiments.</span>
</main>
<div class="pop" id="pop"><div class="pop-s"><button aria-label="Close">×</button><div id="popIn"></div></div></div>
<footer><span>© 2026 Arushi</span><span><a href="/#life">Back to Off the clock</a></span></footer>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
<script>window.__LAB={gj};</script>
<script src="/assets/js/lab2.js?v={ASSET_V}" defer></script>
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
shutil.rmtree(f"{ROOT}/library", ignore_errors=True)
write(f"{ROOT}/library/index.html", library_page())
shutil.rmtree(f"{ROOT}/poems", ignore_errors=True)
write(f"{ROOT}/poems/index.html", poems_page())
shutil.rmtree(f"{ROOT}/gallery", ignore_errors=True)
write(f"{ROOT}/gallery/index.html", gallery_page())
shutil.rmtree(f"{ROOT}/lab", ignore_errors=True)
write(f"{ROOT}/lab/index.html", lab_page())
shutil.rmtree(f"{ROOT}/blog", ignore_errors=True)
shutil.rmtree(f"{ROOT}/post", ignore_errors=True)
_posts = load_posts()
write(f"{ROOT}/blog/index.html", blog_index_page())
for _i, _b in enumerate(_posts):
    write(f"{ROOT}/blog/{_b['slug']}/index.html", blog_post_page(_i, _b, _posts))
    write(f"{ROOT}/post/{_b['slug']}/index.html", redirect_page(f"/blog/{_b['slug']}/"))
write(f"{ROOT}/.nojekyll", "")
print("built", 3 + len(projects) + len(_posts), "pages")
