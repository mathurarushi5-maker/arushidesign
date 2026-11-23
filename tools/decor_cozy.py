"""Soft storybook ("cozy illustration") decor. Same class names as decor.py plus `cz`,
so positions come from the shared .decor.* rules. No outlines, pastel flat shapes."""

TABLE = '''<svg class="decor cz table" viewBox="0 0 160 300" aria-hidden="true">
<g fill="none" stroke="#e8e8f0" stroke-width="5" stroke-linecap="round" opacity=".8"><path d="M70 60 q-8 -12 0 -22 q8 -12 0 -22"/><path d="M92 62 q-8 -12 0 -22 q8 -12 0 -22"/></g>
<rect x="64" y="64" width="44" height="40" rx="12" fill="#f1a9a0"/><path d="M108 74 q22 2 0 24" stroke="#f1a9a0" stroke-width="7" fill="none"/>
<rect x="30" y="104" width="100" height="12" rx="6" fill="#c99a6b"/>
<rect x="38" y="116" width="84" height="12" rx="4" fill="#9fc7b0"/><rect x="44" y="128" width="72" height="12" rx="4" fill="#f4d58d"/>
<rect x="76" y="140" width="8" height="140" rx="4" fill="#b98b55"/><ellipse cx="80" cy="284" rx="34" ry="8" fill="#b98b55"/></svg>'''

PLANT = '''<svg class="decor cz plant" viewBox="0 0 150 300" aria-hidden="true">
<g fill="#8fbf86"><ellipse cx="46" cy="150" rx="22" ry="60" transform="rotate(-28 46 150)"/><ellipse cx="104" cy="146" rx="22" ry="62" transform="rotate(26 104 146)"/></g>
<g fill="#a9d29a"><ellipse cx="75" cy="120" rx="22" ry="74"/><ellipse cx="26" cy="190" rx="16" ry="44" transform="rotate(-50 26 190)"/><ellipse cx="124" cy="190" rx="16" ry="44" transform="rotate(50 124 190)"/></g>
<path d="M75 60 V210" stroke="#7aa874" stroke-width="3" opacity=".6"/>
<path d="M32 206 H118 L108 290 Q75 298 42 290 Z" fill="#e2a384"/><rect x="28" y="198" width="94" height="16" rx="8" fill="#eab79c"/>
<g fill="#fff" opacity=".6"><circle cx="64" cy="244" r="4"/><circle cx="90" cy="256" r="4"/></g></svg>'''

import math, random

WINDOW = """<svg class="decor cz window" viewBox="0 0 240 330" aria-hidden="true" style="overflow:visible"><defs>
<linearGradient id="czsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc3ee"/><stop offset=".55" stop-color="#cfe4f2"/><stop offset="1" stop-color="#fbe0c6"/></linearGradient>
<clipPath id="czglass"><rect x="32" y="32" width="176" height="226"/></clipPath>
<linearGradient id="czsheer" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity=".45"/></linearGradient></defs>
<rect x="18" y="18" width="204" height="250" rx="5" fill="#fffaf0"/>
<g clip-path="url(#czglass)"><rect x="32" y="32" width="176" height="226" fill="url(#czsky)"/>
<circle cx="170" cy="96" r="34" fill="#fff4cf" opacity=".45"/><circle cx="170" cy="96" r="18" fill="#fff8de"/>
<g fill="#fff" opacity=".92"><g><ellipse cx="80" cy="62" rx="30" ry="9"/><ellipse cx="98" cy="56" rx="20" ry="10"/><ellipse cx="64" cy="58" rx="16" ry="7"/><animateTransform attributeName="transform" type="translate" values="-14 0;22 0;-14 0" dur="40s" repeatCount="indefinite"/></g>
<g opacity=".8"><ellipse cx="156" cy="50" rx="22" ry="7"/><ellipse cx="168" cy="45" rx="14" ry="7"/><animateTransform attributeName="transform" type="translate" values="10 0;-18 0;10 0" dur="50s" repeatCount="indefinite"/></g></g>
<path d="M96 120 q4 -4 8 0 q4 -4 8 0 M120 104 q3 -3 6 0 q3 -3 6 0" stroke="#5b6b7a" stroke-width="1.4" fill="none" stroke-linecap="round"/>
<path d="M32 176 Q70 140 110 160 Q150 136 208 164 V258 H32Z" fill="#b9d8c4"/>
<path d="M32 190 Q80 160 128 182 Q170 164 208 184 V258 H32Z" fill="#9fcb9c"/>
<g><rect x="58.5" y="178" width="3" height="12" fill="#8a6a4a"/><circle cx="60" cy="178" r="13" fill="#86b886"/><circle cx="55" cy="174" r="7" fill="#a2cc9a"/><rect x="84.5" y="184" width="3" height="9" fill="#8a6a4a"/><circle cx="86" cy="184" r="10" fill="#86b886"/><circle cx="82" cy="181" r="6" fill="#a2cc9a"/><rect x="166.5" y="176" width="3" height="13" fill="#8a6a4a"/><circle cx="168" cy="176" r="14" fill="#86b886"/><circle cx="163" cy="172" r="8" fill="#a2cc9a"/><rect x="192.5" y="184" width="3" height="9" fill="#8a6a4a"/><circle cx="194" cy="184" r="10" fill="#86b886"/><circle cx="190" cy="181" r="6" fill="#a2cc9a"/></g>
<path d="M32 214 Q90 190 150 206 Q186 198 208 206 V258 H32Z" fill="#82b97a"/>
<path d="M32 236 Q100 214 208 232 V258 H32Z" fill="#6fa66b"/>
<path d="M112 258 Q118 232 130 216 Q136 208 146 204 Q134 214 130 232 Q130 246 140 258Z" fill="#f1dcb4" opacity=".9"/>
<g><rect x="46.5" y="214" width="3" height="20" fill="#8a6a4a"/><circle cx="48" cy="214" r="22" fill="#6aa06a"/><circle cx="40" cy="207" r="12" fill="#82b97a"/><rect x="194.5" y="210" width="3" height="23" fill="#8a6a4a"/><circle cx="196" cy="210" r="26" fill="#6aa06a"/><circle cx="187" cy="202" r="14" fill="#82b97a"/></g>
<g fill="#f6a9a0"><circle cx="76" cy="240" r="2.6"/><circle cx="92" cy="246" r="2.6"/><circle cx="160" cy="242" r="2.6"/><circle cx="176" cy="250" r="2.6"/></g>
<g fill="#fff4b8"><circle cx="64" cy="250" r="2.4"/><circle cx="104" cy="238" r="2.4"/><circle cx="148" cy="252" r="2.4"/></g>
<g fill="#fff" opacity=".9"><circle cx="48" cy="64" r="0"/></g>
</g>
<path d="M120 32 V258 M32 108 H208 M32 184 H208" stroke="#fffaf0" stroke-width="6"/>
<rect x="8" y="258" width="224" height="14" rx="4" fill="#f2dcb8"/>
<g><path d="M52 258 L58 238 H82 L88 258 Z" fill="#e2a384"/><g fill="#7fb07a"><ellipse cx="62" cy="228" rx="9" ry="16" transform="rotate(-24 62 228)"/><ellipse cx="78" cy="226" rx="9" ry="16" transform="rotate(24 78 226)"/><ellipse cx="70" cy="222" rx="8" ry="16"/></g></g>
<g><path d="M158 258 L164 240 H188 L194 258 Z" fill="#e2a384"/><g fill="#8fc486"><ellipse cx="166" cy="232" rx="8" ry="13" transform="rotate(-30 166 232)"/><ellipse cx="184" cy="232" rx="8" ry="13" transform="rotate(30 184 232)"/><ellipse cx="175" cy="226" rx="7" ry="14"/></g>
<path d="M166 246 q-12 20 -4 50 M184 246 q10 22 2 44" stroke="#7fb07a" stroke-width="2.6" fill="none"/><g fill="#8fc486"><ellipse cx="160" cy="268" rx="5" ry="3.4"/><ellipse cx="160" cy="288" rx="5" ry="3.4"/><ellipse cx="188" cy="270" rx="5" ry="3.4"/><ellipse cx="187" cy="286" rx="5" ry="3.4"/></g></g>
<path d="M2 14 Q40 8 66 40 Q92 170 56 385 Q30 372 8 392 Q-6 200 2 14z" fill="url(#czsheer)"><animate attributeName="d" values="M2 14 Q40 8 66 40 Q92 170 56 385 Q30 372 8 392 Q-6 200 2 14z;M2 14 Q40 8 66 40 Q112 170 82 385 Q52 378 22 394 Q2 200 2 14z;M2 14 Q40 8 66 40 Q92 170 56 385 Q30 372 8 392 Q-6 200 2 14z" dur="7s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path><path d="M14 40 Q30 160 18 340 M36 36 Q54 160 40 360" stroke="#fff" stroke-width="3" fill="none" opacity=".7"><animate attributeName="d" values="M14 40 Q30 160 18 340 M36 36 Q54 160 40 360;M14 40 Q34 160 28 340 M36 36 Q66 160 62 360;M14 40 Q30 160 18 340 M36 36 Q54 160 40 360" dur="7s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path>
<path d="M238 14 Q200 8 176 40 Q150 170 186 385 Q212 372 234 392 Q248 200 238 14z" fill="url(#czsheer)"><animate attributeName="d" values="M238 14 Q200 8 176 40 Q150 170 186 385 Q212 372 234 392 Q248 200 238 14z;M238 14 Q200 8 176 40 Q130 170 160 385 Q190 378 220 394 Q240 200 238 14z;M238 14 Q200 8 176 40 Q150 170 186 385 Q212 372 234 392 Q248 200 238 14z" dur="8s" begin="-2s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path><path d="M226 40 Q210 160 222 340 M204 36 Q188 160 202 360" stroke="#fff" stroke-width="3" fill="none" opacity=".7"><animate attributeName="d" values="M226 40 Q210 160 222 340 M204 36 Q188 160 202 360;M226 40 Q206 160 212 340 M204 36 Q174 160 178 360;M226 40 Q210 160 222 340 M204 36 Q188 160 202 360" dur="8s" begin="-2s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path>
<rect x="0" y="8" width="240" height="8" rx="4" fill="#caa070"/></svg>"""

LAMP = """<svg class="decor cz lamp" viewBox="0 0 120 240" aria-hidden="true" style="overflow:visible"><defs>
<radialGradient id="czlg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff2c4" stop-opacity=".75"/><stop offset=".45" stop-color="#ffe3a0" stop-opacity=".28"/><stop offset="1" stop-color="#ffd9a0" stop-opacity="0"/></radialGradient>
<linearGradient id="czls" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f1dcb8"/><stop offset=".4" stop-color="#fff6e2"/><stop offset="1" stop-color="#ecd2a8"/></linearGradient>
<radialGradient id="czlb" cx=".5" cy=".4" r=".6"><stop offset="0" stop-color="#fffdf0"/><stop offset="1" stop-color="#ffd980"/></radialGradient></defs>
<circle cx="60" cy="168" r="112" fill="url(#czlg)"><animate attributeName="opacity" values="1;.82;1" dur="5s" repeatCount="indefinite"/></circle>
<path d="M60 0 V90" stroke="#b98b55" stroke-width="2.4"/><rect x="52" y="88" width="16" height="9" rx="3" fill="#c9954f"/><rect x="55" y="96" width="10" height="9" rx="2" fill="#b98441"/>
<path d="M10 178 Q10 114 60 104 Q110 114 110 178 Z" fill="url(#czls)"/>
<path d="M60 104 Q38 120 34 178 M60 104 Q50 124 48 178 M60 104 Q70 124 72 178 M60 104 Q82 120 86 178" stroke="#d9b987" stroke-width="1" fill="none" opacity=".55"/>
<path d="M22 176 Q22 126 48 112 Q38 150 42 176Z" fill="#fff" opacity=".45"/>
<path d="M10 178 q7.5 8 15 0 q7.5 8 15 0 q7.5 8 15 0 q7.5 8 15 0 q7.5 8 15 0 q7.5 8 15 0 q7.5 8 15 0 q7.5 8 15 0" fill="#f1d9ab" stroke="#d9b987" stroke-width="1"/>
<ellipse cx="60" cy="186" rx="15" ry="9" fill="url(#czlb)"/><ellipse cx="60" cy="186" rx="9" ry="5" fill="#fff"/></svg>"""

ART = """<svg class="decor cz art" viewBox="0 0 220 130" aria-hidden="true">
<g><rect x="4" y="2" width="92" height="76" rx="3" fill="#caa070"/><rect x="10" y="8" width="80" height="64" fill="#cfe3f2"/><path d="M10 50 Q36 34 60 48 T90 44 V72 H10z" fill="#b9d4a0"/><path d="M10 60 Q40 50 90 62 V72 H10z" fill="#8fc486"/><rect x="40" y="38" width="18" height="12" fill="#f1a9a0"/><path d="M38 38 L49 28 L60 38z" fill="#e2a384"/></g>
<g><rect x="108" y="14" width="48" height="60" rx="3" fill="#f2dcb8"/><rect x="113" y="19" width="38" height="50" fill="#fffaf0"/><path d="M132 62 V32" stroke="#7fb07a" stroke-width="2"/><g fill="#8fc486"><ellipse cx="127" cy="38" rx="4" ry="7" transform="rotate(-30 127 38)"/><ellipse cx="137" cy="38" rx="4" ry="7" transform="rotate(30 137 38)"/><ellipse cx="127" cy="50" rx="4" ry="7" transform="rotate(-30 127 50)"/><ellipse cx="137" cy="50" rx="4" ry="7" transform="rotate(30 137 50)"/></g></g>
<g><rect x="166" y="34" width="50" height="40" rx="3" fill="#caa070"/><rect x="171" y="39" width="40" height="30" fill="#fbe0c6"/><circle cx="191" cy="54" r="8" fill="#f1a9a0"/><path d="M171 69 Q191 52 211 69z" fill="#b9d4a0"/></g></svg>"""

COUCH = """<svg class="decor cz couch" viewBox="0 0 420 230" aria-hidden="true"><defs><pattern id="czplaid" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#f6c9c4"/><rect width="14" height="3" fill="#fff" opacity=".55"/><rect width="3" height="14" fill="#fff" opacity=".55"/></pattern></defs>
<rect x="56" y="34" width="308" height="126" rx="52" fill="#f2cfc4"/>
<rect x="16" y="86" width="76" height="110" rx="38" fill="#eab8aa"/><rect x="328" y="86" width="76" height="110" rx="38" fill="#eab8aa"/>
<rect x="64" y="104" width="292" height="78" rx="30" fill="#f9dfd5"/><path d="M210 106 V180" stroke="#eab8aa" stroke-width="3" stroke-linecap="round"/>
<rect x="44" y="190" width="10" height="34" rx="5" fill="#c99a6b"/><rect x="366" y="190" width="10" height="34" rx="5" fill="#c99a6b"/>
<g transform="rotate(-10 120 90)"><rect x="86" y="48" width="70" height="66" rx="22" fill="#b8d3b6"/></g>
<path d="M300 100 Q340 90 372 100 L384 196 Q340 206 306 196Z" fill="url(#czplaid)"/><path d="M306 196 l0 12 M318 198 l0 12 M330 199 l0 12 M342 199 l0 12 M354 198 l0 12 M366 197 l0 12 M378 196 l0 12" stroke="#f6c9c4" stroke-width="3" stroke-linecap="round"/>
<g><ellipse cx="228" cy="104" rx="42" ry="22" fill="#e9944f"/><circle cx="196" cy="98" r="17" fill="#e9944f"/><path d="M184 86 l4 -14 l9 9z M200 82 l8 -12 l4 14z" fill="#e9944f"/><path d="M186 99 q4 3 8 0 M199 99 q4 3 8 0" stroke="#5a3a2a" stroke-width="2" fill="none" stroke-linecap="round"/><path d="M262 108 q30 -4 24 -26" stroke="#e9944f" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M212 90 q-4 12 0 22 M228 86 q-4 14 0 24 M244 90 q-4 12 0 20" stroke="#f6c28f" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/></g></svg>"""

def _leaf(x, y, a, r, col):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*.62:.1f}" ry="{r:.1f}" transform="rotate({a:.0f} {x:.1f} {y:.1f})" fill="{col}"/>'

def _vine(name, w, h, pts, n_per, seed, cls):
    rnd = random.Random(seed)
    greens = ["#6fa56c", "#8fc486", "#a6d18f", "#c4e3a2"]
    stem = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    leaves = ""
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        for k in range(n_per):
            t = k / n_per
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for side in (-1, 1):
                leaves += _leaf(x + side * rnd.uniform(4, 11), y + rnd.uniform(-5, 5), side * rnd.uniform(30, 70) + rnd.uniform(-15, 15), rnd.uniform(8, 13), rnd.choice(greens))
    return (f'<svg class="decor cz {cls}" viewBox="0 0 {w} {h}" aria-hidden="true" style="overflow:visible">'
            f'<path d="{stem}" stroke="#5f8f5c" stroke-width="2.4" fill="none" stroke-linejoin="round"/>{leaves}</svg>')

_r = random.Random(7)
VINE = _vine("vine", 90, 700, [(60 + 10 * math.sin(i * .7) + _r.uniform(-4, 4), 20 + i * 28) for i in range(25)], 2, 11, "vine")
GARLAND = _vine("garland", 800, 90, [(i * 30, 45 + 14 * math.sin(i * .6) + _r.uniform(-4, 4)) for i in range(28)], 2, 5, "garland")

_hl = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="8" transform="rotate({a} {x} {y})"/>' for x, y, a in [(28,130,-30),(24,160,30),(20,190,-30),(24,208,30),(52,140,30),(50,176,-30),(48,210,30),(48,240,-30),(72,140,-30),(76,170,30),(78,200,-30),(44,150,30),(44,200,-30),(46,252,30)])
ARMCHAIR = '''<svg class="decor cz couch chair" viewBox="0 0 300 290" aria-hidden="true">
<defs>
<linearGradient id="chBack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6b9b3"/><stop offset="1" stop-color="#e48f8c"/></linearGradient>
<linearGradient id="chCush" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbd0cb"/><stop offset="1" stop-color="#f1a9a4"/></linearGradient>
<linearGradient id="chSeat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f9c3bd"/><stop offset="1" stop-color="#e99b97"/></linearGradient>
<linearGradient id="chArmL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e48f8c"/><stop offset=".55" stop-color="#f3aaa5"/><stop offset="1" stop-color="#d98582"/></linearGradient>
<linearGradient id="chArmR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#e48f8c"/><stop offset=".55" stop-color="#f3aaa5"/><stop offset="1" stop-color="#d98582"/></linearGradient>
<linearGradient id="chLeg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d9ac5c"/><stop offset="1" stop-color="#a97a34"/></linearGradient>
</defs>
<ellipse cx="150" cy="282" rx="118" ry="9" fill="#8a4f48" opacity=".16"/>
<path d="M72 240 L63 284 M112 250 L107 286 M198 250 L203 286 M236 240 L245 284" stroke="url(#chLeg)" stroke-width="8" stroke-linecap="round"/>
<path d="M44 124 Q44 38 150 36 Q256 38 256 124 L262 216 Q150 236 38 216 Z" fill="url(#chBack)"/>
<path d="M44 124 Q44 38 150 36 Q256 38 256 124" stroke="#fde0dc" stroke-width="3" fill="none" opacity=".7"/>
<path d="M60 132 Q60 60 150 58 Q240 60 240 132 L238 194 H62 Z" fill="#e9978f"/>
<path d="M66 134 Q66 66 150 64 Q234 66 234 134 L232 190 H68 Z" fill="url(#chCush)"/>
<g fill="#e48f8c" opacity=".75"><circle cx="150" cy="104" r="3.5"/><circle cx="116" cy="118" r="3.5"/><circle cx="184" cy="118" r="3.5"/><circle cx="116" cy="150" r="3.5"/><circle cx="184" cy="150" r="3.5"/><circle cx="150" cy="140" r="3.5"/></g>
<path d="M150 104 L116 118 M150 104 L184 118 M116 118 L116 150 M184 118 L184 150 M150 140 L116 150 M150 140 L184 150 M150 104 L150 140" stroke="#e28b88" stroke-width="2" fill="none" opacity=".55"/>
<path d="M56 196 Q150 182 244 196 L252 250 Q150 268 48 250 Z" fill="url(#chSeat)"/>
<path d="M48 250 Q150 268 252 250 L252 238 Q150 256 48 238 Z" fill="#dc8b88"/>
<path d="M56 196 Q150 182 244 196" stroke="#fde8e4" stroke-width="4" fill="none"/>
<path d="M52 224 Q150 210 248 224" stroke="#e48f8c" stroke-width="2" fill="none" opacity=".6"/>
<path d="M20 152 Q14 118 46 116 Q74 116 74 152 L78 240 Q50 252 28 240 Z" fill="url(#chArmL)"/>
<path d="M280 152 Q286 118 254 116 Q226 116 226 152 L222 240 Q250 252 272 240 Z" fill="url(#chArmR)"/>
<path d="M26 128 Q40 116 62 124" stroke="#fde0dc" stroke-width="3" fill="none" opacity=".75" stroke-linecap="round"/>
<path d="M274 128 Q260 116 238 124" stroke="#fde0dc" stroke-width="3" fill="none" opacity=".75" stroke-linecap="round"/>
<path d="M96 72 Q150 52 206 78 Q214 122 196 170 Q150 184 102 166 Q86 122 96 72Z" fill="#fbd9c4"/>
<path d="M96 72 Q150 52 206 78 Q212 98 210 112 Q150 80 92 108 Q90 90 96 72Z" fill="#fff0e4" opacity=".6"/>
<path d="M102 166 Q150 184 196 170 Q200 164 202 156 Q150 172 100 156Z" fill="#eeb89d" opacity=".7"/>
<path d="M110 92 Q150 82 190 94 M106 126 Q150 114 196 128" stroke="#f0bba0" stroke-width="3" fill="none"/>
</svg>'''

HANG = '''<svg class="decor cz hang" viewBox="0 0 100 300" aria-hidden="true" style="overflow:visible"><defs>
<linearGradient id="czhp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d98d6c"/><stop offset=".45" stop-color="#f4c0a2"/><stop offset="1" stop-color="#c97c5c"/></linearGradient></defs>
<path d="M50 0 V54" stroke="#d9c39a" stroke-width="2.4"/><circle cx="50" cy="56" r="4.5" fill="#e6d4ac" stroke="#c9b387"/>
<path d="M50 60 L28 104 M50 60 L72 104 M50 60 L42 106 M50 60 L58 106" stroke="#e6d4ac" stroke-width="1.8" fill="none"/>
<circle cx="39" cy="82" r="2.6" fill="#e6d4ac"/><circle cx="61" cy="82" r="2.6" fill="#e6d4ac"/>
<path d="M36 104 Q14 150 24 214" stroke="#5f8f5c" stroke-width="1.8" fill="none" stroke-linecap="round"/><path d="M46 104 Q40 170 48 262" stroke="#5f8f5c" stroke-width="1.8" fill="none" stroke-linecap="round"/><path d="M56 104 Q66 160 54 236" stroke="#5f8f5c" stroke-width="1.8" fill="none" stroke-linecap="round"/><path d="M64 104 Q92 150 80 222" stroke="#5f8f5c" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<path d="M26 100 H74 L67 136 Q50 144 33 136 Z" fill="url(#czhp)"/><rect x="24" y="96" width="52" height="9" rx="4" fill="#e9a988"/><rect x="24" y="96" width="52" height="3" rx="1.5" fill="#fff" opacity=".35"/>
<path d="M32 116 H68" stroke="#fff6e8" stroke-width="2" stroke-dasharray="3 3" opacity=".8"/>
<path d="M0 0 C-7.7 -5.5 -5.5 -14.2 0 -16.4 C5.5 -14.2 7.7 -5.5 0 0Z" transform="translate(31.3 114.9) rotate(54)" fill="#8fc486"/><path d="M0 0 C-7.3 -5.2 -5.2 -13.6 0 -15.7 C5.2 -13.6 7.3 -5.2 0 0Z" transform="translate(27.5 126.4) rotate(-62)" fill="#a6d18f"/><path d="M0 0 C-7.5 -5.3 -5.3 -13.9 0 -16.0 C5.3 -13.9 7.5 -5.3 0 0Z" transform="translate(24.5 138.3) rotate(59)" fill="#6fa56c"/><path d="M0 0 C-7.4 -5.3 -5.3 -13.8 0 -15.9 C5.3 -13.8 7.4 -5.3 0 0Z" transform="translate(22.5 150.7) rotate(-47)" fill="#8fc486"/><path d="M0 0 C-7.1 -5.1 -5.1 -13.2 0 -15.2 C5.1 -13.2 7.1 -5.1 0 0Z" transform="translate(21.2 163.6) rotate(47)" fill="#a6d18f"/><path d="M0 0 C-6.4 -4.5 -4.5 -11.8 0 -13.6 C4.5 -11.8 6.4 -4.5 0 0Z" transform="translate(20.9 176.9) rotate(-48)" fill="#6fa56c"/><path d="M0 0 C-7.1 -5.1 -5.1 -13.3 0 -15.3 C5.1 -13.3 7.1 -5.1 0 0Z" transform="translate(21.4 190.8) rotate(56)" fill="#8fc486"/><path d="M0 0 C-6.1 -4.3 -4.3 -11.3 0 -13.0 C4.3 -11.3 6.1 -4.3 0 0Z" transform="translate(22.8 205.2) rotate(-49)" fill="#a6d18f"/><path d="M0 0 C-6.3 -4.5 -4.5 -11.7 0 -13.5 C4.5 -11.7 6.3 -4.5 0 0Z" transform="translate(24.0 214.0) rotate(183)" fill="#6fa56c"/><path d="M0 0 C-8.3 -5.9 -5.9 -15.3 0 -17.7 C5.9 -15.3 8.3 -5.9 0 0Z" transform="translate(44.8 119.7) rotate(69)" fill="#a6d18f"/><path d="M0 0 C-8.6 -6.1 -6.1 -15.9 0 -18.4 C6.1 -15.9 8.6 -6.1 0 0Z" transform="translate(44.0 136.1) rotate(-56)" fill="#6fa56c"/><path d="M0 0 C-8.2 -5.8 -5.8 -15.2 0 -17.5 C5.8 -15.2 8.2 -5.8 0 0Z" transform="translate(43.5 153.2) rotate(47)" fill="#8fc486"/><path d="M0 0 C-6.9 -4.9 -4.9 -12.9 0 -14.8 C4.9 -12.9 6.9 -4.9 0 0Z" transform="translate(43.4 171.0) rotate(-53)" fill="#a6d18f"/><path d="M0 0 C-6.9 -4.9 -4.9 -12.8 0 -14.8 C4.9 -12.8 6.9 -4.9 0 0Z" transform="translate(43.8 189.5) rotate(49)" fill="#6fa56c"/><path d="M0 0 C-6.5 -4.6 -4.6 -12.0 0 -13.9 C4.6 -12.0 6.5 -4.6 0 0Z" transform="translate(44.4 208.7) rotate(-66)" fill="#8fc486"/><path d="M0 0 C-6.9 -4.9 -4.9 -12.8 0 -14.8 C4.9 -12.8 6.9 -4.9 0 0Z" transform="translate(45.5 228.7) rotate(60)" fill="#a6d18f"/><path d="M0 0 C-6.5 -4.7 -4.7 -12.1 0 -14.0 C4.7 -12.1 6.5 -4.7 0 0Z" transform="translate(47.0 249.3) rotate(-55)" fill="#6fa56c"/><path d="M0 0 C-6.3 -4.5 -4.5 -11.7 0 -13.5 C4.5 -11.7 6.3 -4.5 0 0Z" transform="translate(48.0 262.0) rotate(171)" fill="#8fc486"/><path d="M0 0 C-7.7 -5.5 -5.5 -14.4 0 -16.6 C5.5 -14.4 7.7 -5.5 0 0Z" transform="translate(58.0 117.3) rotate(47)" fill="#6fa56c"/><path d="M0 0 C-7.8 -5.6 -5.6 -14.5 0 -16.7 C5.6 -14.5 7.8 -5.6 0 0Z" transform="translate(59.5 131.1) rotate(-62)" fill="#8fc486"/><path d="M0 0 C-7.8 -5.6 -5.6 -14.5 0 -16.7 C5.6 -14.5 7.8 -5.6 0 0Z" transform="translate(60.3 145.5) rotate(54)" fill="#a6d18f"/><path d="M0 0 C-7.1 -5.1 -5.1 -13.3 0 -15.3 C5.1 -13.3 7.1 -5.1 0 0Z" transform="translate(60.5 160.4) rotate(-57)" fill="#6fa56c"/><path d="M0 0 C-7.5 -5.3 -5.3 -13.8 0 -16.0 C5.3 -13.8 7.5 -5.3 0 0Z" transform="translate(60.2 175.9) rotate(65)" fill="#8fc486"/><path d="M0 0 C-7.0 -5.0 -5.0 -13.1 0 -15.1 C5.0 -13.1 7.0 -5.0 0 0Z" transform="translate(59.2 191.9) rotate(-52)" fill="#a6d18f"/><path d="M0 0 C-7.2 -5.2 -5.2 -13.4 0 -15.5 C5.2 -13.4 7.2 -5.2 0 0Z" transform="translate(57.7 208.4) rotate(59)" fill="#6fa56c"/><path d="M0 0 C-6.1 -4.4 -4.4 -11.4 0 -13.2 C4.4 -11.4 6.1 -4.4 0 0Z" transform="translate(55.6 225.5) rotate(-64)" fill="#8fc486"/><path d="M0 0 C-6.3 -4.5 -4.5 -11.7 0 -13.5 C4.5 -11.7 6.3 -4.5 0 0Z" transform="translate(54.0 236.0) rotate(190)" fill="#a6d18f"/><path d="M0 0 C-8.0 -5.7 -5.7 -14.9 0 -17.2 C5.7 -14.9 8.0 -5.7 0 0Z" transform="translate(70.0 115.0) rotate(49)" fill="#8fc486"/><path d="M0 0 C-7.4 -5.3 -5.3 -13.8 0 -15.9 C5.3 -13.8 7.4 -5.3 0 0Z" transform="translate(74.9 126.8) rotate(-64)" fill="#a6d18f"/><path d="M0 0 C-7.0 -5.0 -5.0 -13.0 0 -15.0 C5.0 -13.0 7.0 -5.0 0 0Z" transform="translate(78.7 139.3) rotate(58)" fill="#6fa56c"/><path d="M0 0 C-7.8 -5.6 -5.6 -14.5 0 -16.7 C5.6 -14.5 7.8 -5.6 0 0Z" transform="translate(81.4 152.4) rotate(-62)" fill="#8fc486"/><path d="M0 0 C-7.7 -5.5 -5.5 -14.3 0 -16.5 C5.5 -14.3 7.7 -5.5 0 0Z" transform="translate(83.0 166.3) rotate(60)" fill="#a6d18f"/><path d="M0 0 C-7.2 -5.1 -5.1 -13.4 0 -15.4 C5.1 -13.4 7.2 -5.1 0 0Z" transform="translate(83.6 180.8) rotate(-54)" fill="#6fa56c"/><path d="M0 0 C-6.8 -4.9 -4.9 -12.6 0 -14.6 C4.9 -12.6 6.8 -4.9 0 0Z" transform="translate(83.1 196.1) rotate(60)" fill="#8fc486"/><path d="M0 0 C-6.9 -4.9 -4.9 -12.9 0 -14.8 C4.9 -12.9 6.9 -4.9 0 0Z" transform="translate(81.5 212.1) rotate(-57)" fill="#a6d18f"/><path d="M0 0 C-6.3 -4.5 -4.5 -11.7 0 -13.5 C4.5 -11.7 6.3 -4.5 0 0Z" transform="translate(80.0 222.0) rotate(189)" fill="#6fa56c"/>
</svg>'''

PROPS = '''<svg class="decor cz props" viewBox="0 0 380 190" aria-hidden="true" style="overflow:visible">
<g><rect x="12" y="150" width="120" height="32" rx="4" fill="#9fc7b0"/><rect x="18" y="118" width="108" height="32" rx="4" fill="#f1a9a0"/><rect x="8" y="88" width="116" height="30" rx="4" fill="#f4d58d"/><rect x="22" y="62" width="96" height="26" rx="4" fill="#a9c9e8"/>
<path d="M14 166 H126 M24 134 H120 M14 104 H118 M28 75 H112" stroke="#fff" stroke-width="2" opacity=".55"/></g>
<g><path d="M168 182 L174 138 H214 L220 182 Z" fill="#fffaf0"/><g fill="#8fc486"><ellipse cx="178" cy="120" rx="10" ry="26" transform="rotate(-30 178 120)"/><ellipse cx="206" cy="118" rx="10" ry="28" transform="rotate(28 206 118)"/><ellipse cx="192" cy="108" rx="10" ry="32"/></g></g>
<g><path d="M326 182 Q318 150 326 128 H352 Q360 150 352 182 Z" fill="#fffaf0"/><g stroke="#7fb07a" stroke-width="2" fill="none"><path d="M334 130 q-8 -30 -12 -46"/><path d="M340 130 V76"/><path d="M346 130 q8 -30 14 -46"/></g><g fill="#fff"><circle cx="322" cy="82" r="7"/><circle cx="340" cy="74" r="7"/><circle cx="360" cy="82" r="7"/></g><g fill="#f6c25f"><circle cx="322" cy="82" r="3"/><circle cx="340" cy="74" r="3"/><circle cx="360" cy="82" r="3"/></g></g></svg>'''


def _lf(x, y, ang, L, W, c1, c2, sway, delay, stem=None):
    half = lambda k: f"M0 0 C{k*W*.95:.1f} {-L*.22:.1f} {k*W*.8:.1f} {-L*.72:.1f} 0 {-L:.1f}Z"
    veins = "".join(f'<path d="M0 {-L*t:.1f} L{W*.55:.1f} {-L*(t+.14):.1f} M0 {-L*t:.1f} L{-W*.55:.1f} {-L*(t+.14):.1f}"/>' for t in (.25, .42, .59))
    st = f'<path d="M{stem[0]:.1f} {stem[1]:.1f} Q{(stem[0]+x)/2+stem[2]:.1f} {(stem[1]+y)/2:.1f} {x:.1f} {y:.1f}" stroke="#6f9a68" stroke-width="2.6" fill="none"/>' if stem else ""
    return (f'{st}<g style="transform-origin:{x:.1f}px {y:.1f}px;--a:{sway}deg;animation:leafsway {4.2 + delay:.1f}s ease-in-out {-delay*2:.1f}s infinite alternate">'
            f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang})"><path d="{half(1)}" fill="{c1}"/><path d="{half(-1)}" fill="{c2}"/>'
            f'<path d="M0 0 V{-L:.1f}" stroke="#5f8f5c" stroke-width="1.4" opacity=".7"/><g stroke="#5f8f5c" stroke-width=".9" opacity=".4" fill="none">{veins}</g></g></g>')

def _plant(cls, seed, n, spread, pot):
    rnd = random.Random(seed)
    out = ""
    for i in range(n):
        a = -spread + 2 * spread * i / (n - 1) + rnd.uniform(-6, 6)
        L = rnd.uniform(52, 76)
        W = rnd.uniform(16, 24)
        bx = 75 + a * .25
        sl = rnd.uniform(40, 70)
        tip_x = 75 + math.sin(math.radians(a)) * sl
        out += _lf(tip_x, 205 - math.cos(math.radians(a)) * sl, a, L, W, rnd.choice(["#7fb27a", "#8fc486", "#76a972"]), rnd.choice(["#a3d198", "#95c68c"]), rnd.choice([2.5, 3.5, 4.5]), rnd.uniform(0, 2), (75, 206, rnd.uniform(-8, 8)))
    return (f'<svg class="decor cz {cls}" viewBox="0 0 150 300" aria-hidden="true" style="overflow:visible">{out}'
            f'<defs><linearGradient id="czpot{cls}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d48a69"/><stop offset=".4" stop-color="{pot[1]}"/><stop offset="1" stop-color="#c47a5b"/></linearGradient></defs>'
            f'<ellipse cx="75" cy="294" rx="48" ry="6" fill="#000" opacity=".14"/>'
            f'<path d="M32 206 H118 L108 290 Q75 298 42 290 Z" fill="url(#czpot{cls})"/><rect x="28" y="198" width="94" height="16" rx="8" fill="url(#czpot{cls})"/><rect x="28" y="198" width="94" height="5" rx="2.5" fill="#fff" opacity=".35"/>'
            f'<path d="M40 232 H110 M42 256 H108" stroke="#fff6e8" opacity=".55" stroke-width="2" stroke-dasharray="4 4"/></svg>')

PLANT = _plant("plant", 3, 9, 62, ("#e2a384", "#eab79c"))
PLANT2 = _plant("plant plant2", 8, 7, 55, ("#d9b48a", "#e6c7a0"))

COFFEE = '''<svg class="decor cz coffee" viewBox="0 0 220 150" aria-hidden="true" style="overflow:visible">
<ellipse cx="110" cy="146" rx="90" ry="5" fill="#a86a66" opacity=".25"/>
<path d="M34 70 L24 144 M186 70 L196 144" stroke="#b9854f" stroke-width="7" stroke-linecap="round"/>
<path d="M40 112 H180" stroke="#c99a62" stroke-width="5"/>
<rect x="14" y="62" width="192" height="14" rx="7" fill="#e0b27a"/><rect x="14" y="62" width="192" height="5" rx="2.5" fill="#f0cc9a"/>
<g><path d="M96 24 H128 L125 58 Q112 62 99 58 Z" fill="#fffaf0"/><path d="M96 24 H128" stroke="#e9dfcc" stroke-width="2"/><ellipse cx="112" cy="25" rx="16" ry="4" fill="#7a4a2c"/><ellipse cx="108" cy="24" rx="6" ry="1.5" fill="#a56b44" opacity=".7"/>
<path d="M127 32 q16 2 12 14 q-3 8 -13 7" stroke="#fffaf0" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M100 44 h22" stroke="#f1a9a0" stroke-width="3" opacity=".8"/></g>
<g fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round">
<path class="steam s1" d="M104 18 q-8 -8 0 -16 q8 -8 0 -16"/><path class="steam s2" d="M114 18 q8 -8 0 -16 q-8 -8 0 -16"/><path class="steam s3" d="M122 18 q-7 -7 0 -14 q7 -7 0 -14"/></g></svg>'''
CLOCK = '''<svg class="decor cz clock" viewBox="0 0 110 130" aria-hidden="true" style="overflow:visible">
<g><circle cx="30" cy="22" r="13" fill="#d9a84f"/><circle cx="80" cy="22" r="13" fill="#d9a84f"/><path d="M24 20 q6 -8 12 0 M74 20 q6 -8 12 0" stroke="#fff3c4" stroke-width="2" fill="none" opacity=".7"/></g>
<path d="M55 10 Q55 2 62 4" stroke="#b98a3e" stroke-width="3" fill="none"/>
<path d="M30 112 L22 128 M80 112 L88 128" stroke="#b98a3e" stroke-width="5" stroke-linecap="round"/>
<circle cx="55" cy="68" r="46" fill="#e8b86a"/><circle cx="55" cy="68" r="41" fill="#c98d3a"/><circle cx="55" cy="68" r="37" fill="#fbf6e8"/><circle cx="43" cy="52" r="14" fill="#fff" opacity=".5"/>
<g fill="#6b4a2a" font-family="Georgia,serif" font-size="9" text-anchor="middle"><text x="55" y="42">XII</text><text x="55" y="101">VI</text><text x="87" y="71">III</text><text x="23" y="71">IX</text></g>
<g stroke="#a98b5c" stroke-width="1.6"><path d="M71 46 l-2 4 M82 57 l-4 2 M82 79 l-4 -2 M71 90 l-2 -4 M39 90 l2 -4 M28 79 l4 -2 M28 57 l4 2 M39 46 l2 4"/></g>
<g stroke="#4a3520" stroke-linecap="round"><path d="M55 68 V54" stroke-width="3.6"><animateTransform attributeName="transform" type="rotate" from="300 55 68" to="660 55 68" dur="43200s" repeatCount="indefinite" /></path><path d="M55 68 V47" stroke-width="3"><animateTransform attributeName="transform" type="rotate" from="60 55 68" to="420 55 68" dur="3600s" repeatCount="indefinite" /></path><path d="M55 74 V40" stroke="#c0503f" stroke-width="1.2"><animateTransform attributeName="transform" type="rotate" from="0 55 68" to="360 55 68" dur="60s" repeatCount="indefinite" /></path></g><circle cx="55" cy="68" r="3" fill="#b98a3e"/></svg>'''
FILTER = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="czpaint" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2"/></filter></svg>'''

ALL = LAMP + WINDOW + HANG + ART + ARMCHAIR + PLANT + COFFEE
CASE_EXTRA = GARLAND + VINE


def _bookwall():
    rnd = random.Random(11)
    W, H, rows = 700, 420, 6
    rh = H / rows
    pal = ['#e8a9a4', '#f4c8c0', '#f2d9a6', '#cfe0b8', '#9fc9c0', '#a9c4de', '#d9b3c8', '#c99a7e', '#f7e6c4', '#b7d6c4', '#e59b8f', '#8fb7a8', '#d8c3a5']
    o = [f'<svg class="bookwall cz" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="bwg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fcdb4"/><stop offset="1" stop-color="#b6dcc4"/></linearGradient></defs><rect width="{W}" height="{H}" fill="#a9d4bd"/>']
    for r in range(rows):
        top = r * rh
        base = top + rh - 8
        o.append(f'<rect x="0" y="{top:.1f}" width="{W}" height="{rh-8:.1f}" fill="url(#bwg)"/>')
        o.append(f'<rect x="0" y="{base:.1f}" width="{W}" height="8" fill="#e3f3e8"/><rect x="0" y="{base+6:.1f}" width="{W}" height="2" fill="#7fb59c" opacity=".6"/>')
        x = 6
        while x < W - 8:
            roll = rnd.random()
            if roll < .07:
                x += rnd.randint(14, 34)
                continue
            if roll < .13:
                for k in range(rnd.randint(3, 5)):
                    w = rnd.randint(34, 46)
                    h = rnd.randint(6, 9)
                    o.append(f'<rect x="{x}" y="{base-h*(k+1):.1f}" width="{w}" height="{h-1}" rx="1.5" fill="{rnd.choice(pal)}"/>')
                x += 50
                continue
            w = rnd.randint(7, 15)
            h = rnd.randint(int(rh * .55), int(rh * .8))
            c = rnd.choice(pal)
            lean = rnd.random() < .05
            tr = f' transform="rotate({rnd.randint(8, 14)} {x} {base:.1f})"' if lean else ''
            o.append(f'<g{tr}><rect x="{x}" y="{base-h:.1f}" width="{w}" height="{h}" rx="1.4" fill="{c}"/><rect x="{x+1.5}" y="{base-h:.1f}" width="2" height="{h}" fill="#fff" opacity=".28"/><rect x="{x}" y="{base-h+6:.1f}" width="{w}" height="2" fill="#fff" opacity=".5"/><rect x="{x}" y="{base-9:.1f}" width="{w}" height="2" fill="#fff" opacity=".4"/></g>')
            x += w + rnd.choice([0, 0, 1, 1, 2])
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bwlight)" />')
    o.append('</svg>')
    return ''.join(o).replace('<defs>', '<defs><linearGradient id="bwlight" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#fff6d8" stop-opacity=".38"/><stop offset=".55" stop-color="#fff6d8" stop-opacity="0"/></linearGradient>', 1)


BOOKWALL = _bookwall()
ALL = BOOKWALL + ALL
