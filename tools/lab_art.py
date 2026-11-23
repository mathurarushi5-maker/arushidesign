"""Soft painted SVG art for the Lab room (pastel version)."""
import math

DEFS = ('<defs>'
        '<linearGradient id="lbGrA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8fd08a"/><stop offset="1" stop-color="#3f9558"/></linearGradient>'
        '<linearGradient id="lbGrB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6cba75"/><stop offset="1" stop-color="#2f7c4a"/></linearGradient>'
        '<linearGradient id="lbTerra" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0b48a"/><stop offset="1" stop-color="#cf7f58"/></linearGradient>'
        '</defs>')


def lv(x, y, r, rx=11, ry=5.5, fill="url(#lbGrA)"):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" fill="{fill}" transform="rotate({r:.0f} {x:.1f} {y:.1f})"/>'


def burst(cx, cy, r0, r1, a0, a1, n, rx=11, ry=5.5):
    out = []
    for i in range(n):
        a = a0 + (a1 - a0) * i / max(1, n - 1)
        rad = r0 + (r1 - r0) * ((i * 7) % 5) / 4
        x = cx + rad * math.cos(math.radians(a))
        y = cy + rad * math.sin(math.radians(a))
        out.append(lv(x, y, a + 90 * (1 if i % 2 else -1) * 0 + 0, rx, ry,
                      "url(#lbGrA)" if i % 2 else "url(#lbGrB)"))
    return "".join(out)


def vine(x0, y0, x1, y1, bend, n, rx=6, ry=3.2):
    """A hanging vine with paired small leaves."""
    d = f'<path d="M{x0} {y0}Q{x0+bend} {(y0+y1)/2} {x1} {y1}" stroke="#58a063" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    leaves = []
    for i in range(1, n + 1):
        t = i / (n + 1)
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + bend) + t ** 2 * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2) + t ** 2 * y1
        leaves.append(lv(x - 5, y, -40, rx, ry, "url(#lbGrA)"))
        leaves.append(lv(x + 5, y + 3, 40, rx, ry, "url(#lbGrB)"))
    return d + "".join(leaves)


HANG1 = (
    '<svg class="lb-hang h1" viewBox="0 0 200 330" aria-hidden="true">' + DEFS +
    '<g stroke="#ead7b6" stroke-width="2.4" fill="none" stroke-linecap="round"><path d="M100 0V60M100 60L48 150M100 60L100 150M100 60L152 150"/></g>'
    + burst(100, 135, 22, 62, -170, -10, 16, 14, 7) +
    '<path d="M44 140h112l-12 78q-3 14-17 14H73q-14 0-17-14z" fill="url(#lbTerra)"/>'
    '<ellipse cx="100" cy="140" rx="56" ry="8" fill="#f6c9a4"/>'
    '<g stroke="#fbf0dc" stroke-width="2" fill="none" opacity=".9"><path d="M56 150L100 215L144 150M74 150L100 190L126 150M100 150V218M60 180L100 222L140 180"/></g>'
    + vine(62, 205, 48, 322, -22, 8) + vine(138, 205, 150, 300, 14, 6) +
    '</svg>')

HANG2 = (
    '<svg class="lb-hang h2" viewBox="0 0 150 300" aria-hidden="true">'
    '<g stroke="#ead7b6" stroke-width="2.2" fill="none" stroke-linecap="round"><path d="M75 0V50M75 50L36 100M75 50L114 100M75 50V100"/></g>'
    + burst(75, 96, 12, 34, -165, -15, 11, 10, 5) +
    '<path d="M38 96h74l-8 36q-2 9-11 9H57q-9 0-11-9z" fill="#efb394"/>'
    '<ellipse cx="75" cy="96" rx="37" ry="5.5" fill="#f7cdb0"/>'
    + vine(50, 135, 34, 292, -10, 12, 5.5, 3) + vine(75, 138, 82, 270, 6, 10, 5.5, 3) + vine(100, 135, 116, 285, 12, 11, 5.5, 3) +
    '</svg>')

VINE = (
    '<svg class="lb-vine" viewBox="0 0 70 360" aria-hidden="true">'
    + vine(35, 0, 30, 350, 12, 17, 8, 4) + '</svg>')


def _garland():
    pts = []
    for i in range(0, 41):
        x = i * 25
        y = 14 + 34 * math.sin(math.radians(i * 9 + 20)) ** 2
        pts.append((x, y))
    d = "M" + "L".join(f"{x} {y:.1f}" for x, y in pts)
    s = f'<path d="{d}" stroke="#6aa86a" stroke-width="3" fill="none" stroke-linecap="round"/>'
    for i, (x, y) in enumerate(pts[:-1]):
        nx, ny = pts[i + 1]
        ang = math.degrees(math.atan2(ny - y, nx - x))
        s += lv(x, y - 6, ang - 35, 11, 4.6, "url(#lbGrA)") + lv(x + 8, y + 6, ang + 35, 11, 4.6, "url(#lbGrB)")
        if i % 5 == 2:
            s += f'<circle cx="{x+6}" cy="{y+1:.1f}" r="3" fill="#f3c46a"/>'
    return s


GARLAND = ('<svg class="lb-garland" viewBox="0 0 1000 70" preserveAspectRatio="none" aria-hidden="true">' + DEFS + _garland() + '</svg>')

STAR = lambda c: f'<svg class="dd DD" viewBox="0 0 24 24"><path d="M12 1l3.2 8.2L23 12l-7.8 2.8L12 23l-3.2-8.2L1 12l7.8-2.8z" fill="{c}"/></svg>'


def _star(cls, c):
    return f'<svg class="dd {cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1l3.2 8.2L23 12l-7.8 2.8L12 23l-3.2-8.2L1 12l7.8-2.8z" fill="{c}"/></svg>'


DOODLES = (
    '<div class="lb-doodles" aria-hidden="true">'
    # rocket
    '<svg class="dd d1" viewBox="0 0 70 100"><path d="M24 82q-8 14 2 18 6-8 4-18zM18 74q-12 8-8 22 8-4 12-12z" fill="#ffb54d" opacity=".9"/>'
    '<path d="M22 70L8 58l6-14 14 8zM46 70l14-12-6-14-14 8z" fill="#e8574d"/>'
    '<path d="M35 4C52 18 54 46 46 74H24C16 46 18 18 35 4z" fill="#fbfbff"/><path d="M35 4C44 12 49 22 51 34H35z" fill="#e6e8f6"/>'
    '<path d="M35 4C41 9 45 14 47 20H23C25 14 29 9 35 4z" fill="#e8574d"/><circle cx="35" cy="38" r="9" fill="#5b9ad8"/><circle cx="35" cy="38" r="5" fill="#2f4f96"/><path d="M26 74h18l-4 12H30z" fill="#ffd36a"/></svg>'
    # bulb
    '<svg class="dd d2" viewBox="0 0 80 90"><circle cx="40" cy="38" r="30" fill="#ffe9a8" opacity=".55"/><path d="M40 14a20 20 0 0113 36c-3 3-4 6-4 10H31c0-4-1-7-4-10A20 20 0 0140 14z" fill="#ffd25a"/><path d="M33 22a12 12 0 00-6 12" stroke="#fff6cf" stroke-width="3" fill="none" stroke-linecap="round"/><rect x="31" y="60" width="18" height="6" rx="3" fill="#9d8fc4"/><rect x="33" y="67" width="14" height="6" rx="3" fill="#8a7db3"/></svg>'
    # palette
    '<svg class="dd d3" viewBox="0 0 90 80"><path d="M16 14C2 26 0 52 14 64c14 12 36 10 52 2 10-5 4-14 8-20 4-5 14-4 14-18C88 12 62 2 40 4 30 5 22 8 16 14z" fill="#e8c28a"/><circle cx="24" cy="30" r="6" fill="#e9786a"/><circle cx="40" cy="20" r="6" fill="#f3c24f"/><circle cx="58" cy="22" r="6" fill="#7bc27f"/><circle cx="72" cy="32" r="6" fill="#6aa5e8"/><circle cx="30" cy="50" r="6" fill="#b99be8"/><path d="M52 66l22-38" stroke="#6a8fd8" stroke-width="5" stroke-linecap="round"/><path d="M72 30l6-10" stroke="#c9885a" stroke-width="4" stroke-linecap="round"/></svg>'
    # camera
    '<svg class="dd d4" viewBox="0 0 90 70"><rect x="4" y="14" width="82" height="52" rx="10" fill="#b7a2e0"/><path d="M26 14l5-9h28l5 9z" fill="#9a86cf"/><rect x="10" y="20" width="14" height="6" rx="3" fill="#e8dcfa"/><circle cx="45" cy="40" r="19" fill="#e8e4f8"/><circle cx="45" cy="40" r="14" fill="#2f3f7a"/><circle cx="45" cy="40" r="8" fill="#4d73c9"/><circle cx="40" cy="35" r="3" fill="#cfe0ff"/></svg>'
    # line chart card
    '<svg class="dd d5" viewBox="0 0 100 78"><rect x="2" y="4" width="96" height="70" rx="6" fill="#fffaf2"/><rect x="2" y="4" width="96" height="70" rx="6" fill="none" stroke="#ecd9c6" stroke-width="2"/><path d="M12 56l20-18 16 12 22-26 16 10" stroke="#4aa59a" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 64l22-10 18 4 24-16 12 4" stroke="#e8745f" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    # globe
    '<svg class="dd d9" viewBox="0 0 60 60"><circle cx="30" cy="30" r="27" fill="#5b8fe0"/><path d="M14 16c8-6 16-4 18 2s-6 8-6 14-8 8-12 2-4-14 0-18zM38 34c6-4 14 0 12 8s-10 10-14 4 0-8 2-12z" fill="#5fb272"/><path d="M12 14a27 27 0 0120-10" stroke="#cfe0ff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/></svg>'
    # check badge
    '<svg class="dd d10" viewBox="0 0 50 50"><circle cx="25" cy="25" r="22" fill="#f27fa5"/><path d="M15 26l7 7 14-15" stroke="#fff" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    # cart
    '<svg class="dd d11" viewBox="0 0 56 56"><circle cx="28" cy="28" r="26" fill="#fffaf8"/><path d="M13 17h5l4 15h16l4-11H20" stroke="#7a5fc4" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="39" r="2.6" fill="#7a5fc4"/><circle cx="36" cy="39" r="2.6" fill="#7a5fc4"/></svg>'
    # cursor
    '<svg class="dd d12" viewBox="0 0 40 44"><path d="M6 4l26 16-11 3-5 11z" fill="#6f7fe0"/><path d="M6 4l26 16-11 3z" fill="#8795ee"/></svg>'
    # bar chart
    '<svg class="dd d13" viewBox="0 0 80 64"><path d="M6 4v54h72" stroke="#6b78b8" stroke-width="2" fill="none"/><rect x="14" y="34" width="10" height="24" rx="1" fill="#b9a3e3"/><rect x="30" y="24" width="10" height="34" rx="1" fill="#f3c24f"/><rect x="46" y="14" width="10" height="44" rx="1" fill="#f08a6a"/><rect x="62" y="20" width="10" height="38" rx="1" fill="#4aa59a"/></svg>'
    + _star("d6", "#f6c445") + _star("d7", "#f0a0c4") + _star("d8", "#b99be8") + _star("d14", "#f3a85a") + _star("d15", "#f6c445") + _star("d16", "#b99be8")
    + '<svg class="dd sp k1" viewBox="0 0 24 24"><path d="M12 0c1 7 5 11 12 12-7 1-11 5-12 12-1-7-5-11-12-12 7-1 11-5 12-12z" fill="#fff"/></svg>'
    + '<svg class="dd sp k2" viewBox="0 0 24 24"><path d="M12 0c1 7 5 11 12 12-7 1-11 5-12 12-1-7-5-11-12-12 7-1 11-5 12-12z" fill="#fff"/></svg>'
    + '</div>')

MUG = (
    '<svg class="lb-mug" viewBox="0 0 130 200" aria-hidden="true">'
    '<g stroke-linecap="round"><path d="M44 96L22 22" stroke="#9a5a3c" stroke-width="6"/><path d="M58 96L48 12" stroke="#e9a45a" stroke-width="6"/><path d="M74 96L72 10" stroke="#5b7a96" stroke-width="6"/><path d="M90 96L106 28" stroke="#4a5268" stroke-width="6"/></g>'
    '<path d="M14 6l10 14-6 10-8-14z" fill="#c4583c"/><path d="M42 4l10-2v18l-10 2z" fill="#a8c4d8"/><path d="M64 2h16l-2 18H66z" fill="#d9a05c"/><path d="M100 22l10 6-8 12-8-6z" fill="#3f4658"/>'
    '<path d="M104 112h8a18 18 0 010 36h-12" stroke="#c9d6e6" stroke-width="9" fill="none" stroke-linecap="round"/>'
    '<path d="M24 92h86v62a32 32 0 01-32 32H56a32 32 0 01-32-32z" fill="#eef1f6"/>'
    '<path d="M24 130c14 8 30-10 52-2 14 5 26 2 34-2v28a32 32 0 01-32 32H56a32 32 0 01-32-32z" fill="#bcd0e0"/>'
    '<path d="M30 100v50" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/>'
    '<path d="M22 92h90" stroke="#d9b36a" stroke-width="5" stroke-linecap="round"/></svg>')

_SLITS = "M-64 -30L-24 -34M64 -30L24 -34M-62 -58L-22 -60M62 -58L22 -60M-46 -86L-16 -84M46 -86L16 -84"
_LEAF = "M0 0C-48 -6 -68 -44 -44 -82C-32 -98 -12 -104 0 -108C12 -104 32 -98 44 -82C68 -44 48 -6 0 0Z"


def _leaf(x, y, r, s, fill):
    return (f'<use href="#lbLeaf" transform="translate({x} {y}) rotate({r}) scale({s})" fill="{fill}"/>')


MONSTERA = (
    '<svg class="lb-monstera" viewBox="0 0 230 320" aria-hidden="true">'
    '<defs><mask id="lbLeafMk" maskUnits="userSpaceOnUse" x="-90" y="-130" width="180" height="150"><rect x="-90" y="-130" width="180" height="150" fill="#fff"/>'
    f'<path d="{_SLITS}" stroke="#000" stroke-width="7" stroke-linecap="round"/></mask>'
    f'<g id="lbLeaf" mask="url(#lbLeafMk)"><path d="{_LEAF}"/><path d="M0 0V-104" stroke="#fff" stroke-opacity=".3" stroke-width="3"/></g>'
    '<linearGradient id="lbPot" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbeedd"/><stop offset="1" stop-color="#ecd3bd"/></linearGradient></defs>'
    '<g stroke="#4a9460" stroke-width="4" fill="none" stroke-linecap="round"><path d="M112 216C100 170 78 140 66 112M112 216C120 160 150 120 160 96M112 216C112 160 110 110 114 70M112 216C90 190 60 180 46 168M112 216C140 196 170 180 184 162"/></g>'
    + _leaf(66, 112, -38, 1.0, "#3f9558") + _leaf(160, 96, 28, 1.1, "#2f7c4a") + _leaf(114, 70, -4, .95, "#58a862")
    + _leaf(46, 168, -72, .72, "#4a9460") + _leaf(184, 162, 66, .78, "#3b8a52") +
    '<path d="M54 214h116l-12 72q-3 20-22 20H88q-19 0-22-20z" fill="url(#lbPot)"/>'
    '<ellipse cx="112" cy="214" rx="58" ry="9" fill="#f6e6d2"/><ellipse cx="112" cy="214" rx="48" ry="5.5" fill="#7a5a3a" opacity=".55"/>'
    '<path d="M62 238l12-12 12 12 12-12 12 12 12-12 12 12 12-12 12 12 12-12 10 12" stroke="#e8967a" stroke-width="5" fill="none" stroke-linejoin="round"/>'
    '<path d="M66 262l12-12 12 12 12-12 12 12 12-12 12 12 12-12 12 12 12-12" stroke="#7fbfb8" stroke-width="5" fill="none" stroke-linejoin="round"/>'
    '<path d="M70 284h86" stroke="#e8967a" stroke-width="4" opacity=".5"/></svg>')


def _flower(x, y, r, petal, centre):
    s = ""
    for i in range(6):
        a = i * 60
        s += f'<ellipse cx="{x}" cy="{y-r*0.55:.1f}" rx="{r*0.52:.1f}" ry="{r*0.6:.1f}" fill="{petal}" transform="rotate({a} {x} {y})"/>'
    return s + f'<circle cx="{x}" cy="{y}" r="{r*0.3:.1f}" fill="{centre}"/><circle cx="{x}" cy="{y}" r="{r*0.14:.1f}" fill="#fff" opacity=".6"/>'


VASE = (
    '<svg class="lb-vase" viewBox="0 0 120 240" aria-hidden="true">'
    '<g stroke="#5ea866" stroke-width="3" fill="none" stroke-linecap="round"><path d="M44 150C36 110 26 80 24 58M58 150C58 110 62 70 62 36M74 150C80 112 92 84 98 60M52 150C48 120 44 100 36 88M66 150C70 120 78 100 84 80"/></g>'
    + lv(34, 110, -50, 9, 4.5, "url(#lbGrA)") + lv(86, 110, 50, 9, 4.5, "url(#lbGrB)")
    + _flower(24, 50, 22, "#f6c0d4", "#4a3a7a") + _flower(62, 30, 22, "#fff", "#3a2f6a") + _flower(98, 54, 22, "#ee8fb4", "#3a2f6a")
    + _flower(38, 90, 16, "#f4a48a", "#4a3a7a") + _flower(84, 76, 16, "#f9d4e2", "#4a3a7a") +
    '<path d="M32 144h56l6 6-6 78q-1 10-11 10H43q-10 0-11-10l-6-78z" fill="#dff1f4" fill-opacity=".72"/>'
    '<path d="M36 176h48v48q0 8-8 8H44q-8 0-8-8z" fill="#a9d4dc" fill-opacity=".6"/>'
    '<path d="M38 152v70" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".75"/></svg>')

DISH = (
    '<svg class="lb-dish" viewBox="0 0 170 80" aria-hidden="true">'
    '<ellipse cx="85" cy="46" rx="80" ry="30" fill="#e6c3a6"/><ellipse cx="85" cy="40" rx="80" ry="30" fill="#fbeadb"/><ellipse cx="85" cy="40" rx="66" ry="22" fill="#f6d9c4"/>'
    '<path d="M44 34l12-8 8 16z" fill="#3f9aa0"/><path d="M80 26l16 4-10 14z" fill="none" stroke="#3f9aa0" stroke-width="3" stroke-linejoin="round"/><path d="M104 40l14-4 4 14z" fill="#f0a24c"/><path d="M66 46l16 2-8 8z" fill="none" stroke="#e8745f" stroke-width="3" stroke-linejoin="round"/></svg>')


def _bez(p0, p1, p2, t):
    return tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t ** 2 * c for a, b, c in zip(p0, p1, p2))


def _garland2():
    segs = [((0, 2), (70, 78), (220, 66)), ((220, 66), (370, 54), (440, 8)), ((440, 8), (460, 0), (500, 0))]
    pts = []
    for s in segs:
        for i in range(0, 13):
            pts.append(_bez(*s, i / 12))
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    out = f'<path d="{d}" stroke="#6a9a58" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    for i in range(0, len(pts) - 1, 2):
        x, y = pts[i]
        nx, ny = pts[i + 1]
        ang = math.degrees(math.atan2(ny - y, nx - x))
        out += lv(x, y - 4, ang - 50, 9, 3.6, "url(#lbGrA)") + lv(x + 3, y + 4, ang + 50, 9, 3.6, "url(#lbGrB)")
        if i % 8 == 4:
            out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="#f3c46a"/>'
    return out


GARLAND = '<svg class="lb-garland" viewBox="0 0 500 90" aria-hidden="true">' + DEFS + _garland2() + '</svg>'

# tilt the rocket like the reference
DOODLES = DOODLES.replace('<svg class="dd d1" viewBox="0 0 70 100">', '<svg class="dd d1" viewBox="-25 -8 120 118"><g transform="rotate(32 35 50)">', 1)
DOODLES = DOODLES.replace('<path d="M26 74h18l-4 12H30z" fill="#ffd36a"/></svg>', '<path d="M26 74h18l-4 12H30z" fill="#ffd36a"/></g></svg>', 1)
_SP = '<path d="M12 0c1 7 5 11 12 12-7 1-11 5-12 12-1-7-5-11-12-12 7-1 11-5 12-12z" fill="#fff"/>'
DOODLES = DOODLES.replace('</div>', ''.join(f'<svg class="dd sp k{i}" viewBox="0 0 24 24">{_SP}</svg>' for i in (3, 4)) + '</div>', 1) if DOODLES.endswith('</div>') else DOODLES
