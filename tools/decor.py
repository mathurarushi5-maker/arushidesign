"""Flat illustrated decor for the Library room (portfolio style: ink outlines, flat fills)."""
INK = "#16150f"
S = f'stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'


def _leaf(x, y, rot, sc, fill):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})">'
            f'<path d="M0 0 C-30 -30 -26 -95 0 -140 C26 -95 30 -30 0 0Z" fill="{fill}"/>'
            f'<path d="M0 0 C26 -30 30 -95 0 -140 C8 -90 6 -40 0 0Z" fill="#000" opacity=".16"/>'
            f'<path d="M0 -4 V-128" stroke="#fff" stroke-width="{2/sc:.2f}" opacity=".35"/></g>')


WINDOW = '''<svg class="decor window" viewBox="0 0 220 300" aria-hidden="true" style="overflow:visible"><defs>
<linearGradient id="wsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ec4f2"/><stop offset=".6" stop-color="#d5e8f5"/><stop offset="1" stop-color="#fdeccb"/></linearGradient>
<linearGradient id="wfr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf7ec"/><stop offset="1" stop-color="#d9d0bb"/></linearGradient>
<linearGradient id="wcl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8dff3"/><stop offset=".25" stop-color="#f6f4ee"/><stop offset=".5" stop-color="#c9d3ee"/><stop offset=".75" stop-color="#f3f1ea"/><stop offset="1" stop-color="#c3cdea"/></linearGradient>
<linearGradient id="wcr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#d8dff3"/><stop offset=".25" stop-color="#f6f4ee"/><stop offset=".5" stop-color="#c9d3ee"/><stop offset=".75" stop-color="#f3f1ea"/><stop offset="1" stop-color="#c3cdea"/></linearGradient>
<radialGradient id="wsun"><stop offset="0" stop-color="#fff6cf"/><stop offset=".35" stop-color="#fff1b5" stop-opacity=".7"/><stop offset="1" stop-color="#fff1b5" stop-opacity="0"/></radialGradient>
<linearGradient id="wglass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset=".6" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="wtb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e0bd7c"/><stop offset=".5" stop-color="#c49a5a"/><stop offset="1" stop-color="#9a7436"/></linearGradient><clipPath id="wclip"><rect x="48" y="40" width="124" height="200"/></clipPath></defs>
<rect x="48" y="40" width="124" height="200" fill="url(#wsky)"/>
<g clip-path="url(#wclip)"><circle cx="124" cy="112" r="56" fill="url(#wsun)"/><circle cx="124" cy="112" r="15" fill="#fff8de"/>
<g fill="#fff" opacity=".9"><g><ellipse cx="80" cy="76" rx="22" ry="7"/><ellipse cx="94" cy="71" rx="14" ry="8"/><animateTransform attributeName="transform" type="translate" values="-8 0;12 0;-8 0" dur="38s" repeatCount="indefinite"/></g><g opacity=".75"><ellipse cx="146" cy="62" rx="18" ry="6"/><ellipse cx="156" cy="58" rx="11" ry="6"/><animateTransform attributeName="transform" type="translate" values="6 0;-10 0;6 0" dur="46s" repeatCount="indefinite"/></g></g>
<path d="M44 170 Q80 146 116 166 Q146 148 176 164 V244 H44Z" fill="#a9cdb8"/>
<path d="M44 184 Q84 160 126 180 Q154 168 176 178 V244 H44Z" fill="#8fbf86"/>
<g fill="#6f9d6b"><circle cx="62" cy="176" r="9"/><circle cx="72" cy="180" r="7"/><circle cx="150" cy="176" r="10"/><circle cx="162" cy="182" r="7"/></g>
<path d="M44 208 Q90 186 140 206 T176 200 V244 H44Z" fill="#7aae5f"/>
<path d="M44 224 Q100 206 176 222 V244 H44Z" fill="#5f9a4e"/>
<path d="M106 244 Q112 224 124 212 Q130 206 140 204 Q128 214 126 228 Q126 238 134 244Z" fill="#f1dfb8" opacity=".9"/>
<g fill="#2b36c9"><circle cx="62" cy="230" r="3.4"/><circle cx="76" cy="236" r="3.4"/><circle cx="150" cy="232" r="3.4"/><circle cx="164" cy="238" r="3.4"/></g><g fill="#ffe27a"><circle cx="68" cy="238" r="2.6"/><circle cx="158" cy="226" r="2.6"/></g></g>
<rect x="48" y="40" width="124" height="200" fill="url(#wglass)"/>
<path d="M110 40 V240 M48 140 H172" stroke="url(#wfr)" stroke-width="7"/>
<path d="M107 40 V240 M48 137 H172" stroke="#fff" stroke-opacity=".6" stroke-width="1.5"/>
<rect x="44" y="36" width="132" height="208" fill="none" stroke="url(#wfr)" stroke-width="9"/><rect x="48" y="40" width="124" height="200" fill="none" stroke="#000" stroke-opacity=".14" stroke-width="1.6"/>
<path d="M30 244 H190 L184 256 H36Z" fill="url(#wfr)"/><rect x="30" y="256" width="160" height="4" fill="#000" opacity=".08"/>
<rect x="6" y="10" width="208" height="8" rx="4" fill="#8a6a43"/><rect x="6" y="10" width="208" height="3" rx="1.5" fill="#d9b787" opacity=".8"/><circle cx="6" cy="14" r="7" fill="#6b4c2c"/><circle cx="214" cy="14" r="7" fill="#6b4c2c"/>
<path d="M10 18 H62 C62 90 46 120 56 146 C68 180 62 240 66 284 H10Z" fill="url(#wcl)"><animate attributeName="d" values="M10 18 H62 C62 90 46 120 56 146 C68 180 62 240 66 284 H10Z;M10 18 H62 C64 90 50 120 60 146 C74 180 70 240 74 284 H10Z;M10 18 H62 C62 90 46 120 56 146 C68 180 62 240 66 284 H10Z" dur="8s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path>
<path d="M210 18 H158 C158 90 174 120 164 146 C152 180 158 240 154 284 H210Z" fill="url(#wcr)"><animate attributeName="d" values="M210 18 H158 C158 90 174 120 164 146 C152 180 158 240 154 284 H210Z;M210 18 H158 C156 90 170 120 160 146 C146 180 150 240 146 284 H210Z;M210 18 H158 C158 90 174 120 164 146 C152 180 158 240 154 284 H210Z" dur="9s" begin="-3s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></path>
<g stroke="#9fb0e0" stroke-opacity=".45" stroke-width="1.4" fill="none"><path d="M24 22 Q22 150 26 280 M40 22 Q38 150 44 280"/><path d="M196 22 Q198 150 194 280 M180 22 Q182 150 176 280"/></g>
<g><path d="M10 140 Q34.0 152 58 142 L58 149 Q34.0 160 10 148Z" fill="url(#wtb)"/><path d="M10 144 Q34.0 156 58 146" stroke="#fff" stroke-opacity=".35" stroke-width="1" fill="none" stroke-dasharray="2 2"/><path d="M10 148 Q34.0 160 58 149" stroke="#000" stroke-opacity=".2" stroke-width="1" fill="none"/>
<circle cx="56" cy="150" r="3.2" fill="#c49a5a"/><circle cx="56" cy="150" r="1.2" fill="#f2d9a6"/><path d="M56 153 V164" stroke="#b58a4a" stroke-width="2.4" stroke-linecap="round"/><path d="M52.5 164 Q56 160 59.5 164 L60.5 178 H51.5Z" fill="url(#wtb)"/><path d="M53 170 H59" stroke="#8a6a2c" stroke-width="1.2"/><path d="M52.5 178 V184 M54.8 178 V186 M57.2 178 V186 M59.5 178 V184" stroke="#c49a5a" stroke-width="1.1" stroke-linecap="round"/>
<g><animateTransform attributeName="transform" type="rotate" values="-3 56 153;3 56 153;-3 56 153" dur="6s" repeatCount="indefinite"/></g></g><g><path d="M162 140 Q186.0 152 210 142 L210 149 Q186.0 160 162 148Z" fill="url(#wtb)"/><path d="M162 144 Q186.0 156 210 146" stroke="#fff" stroke-opacity=".35" stroke-width="1" fill="none" stroke-dasharray="2 2"/><path d="M162 148 Q186.0 160 210 149" stroke="#000" stroke-opacity=".2" stroke-width="1" fill="none"/>
<circle cx="164" cy="150" r="3.2" fill="#c49a5a"/><circle cx="164" cy="150" r="1.2" fill="#f2d9a6"/><path d="M164 153 V164" stroke="#b58a4a" stroke-width="2.4" stroke-linecap="round"/><path d="M160.5 164 Q164 160 167.5 164 L168.5 178 H159.5Z" fill="url(#wtb)"/><path d="M161 170 H167" stroke="#8a6a2c" stroke-width="1.2"/><path d="M160.5 178 V184 M162.8 178 V186 M165.2 178 V186 M167.5 178 V184" stroke="#c49a5a" stroke-width="1.1" stroke-linecap="round"/>
<g><animateTransform attributeName="transform" type="rotate" values="-3 164 153;3 164 153;-3 164 153" dur="6s" repeatCount="indefinite"/></g></g></svg>'''

CHAIR = f'''<svg class="decor chair" viewBox="0 0 290 250" aria-hidden="true">
<rect x="40" y="14" width="210" height="140" rx="38" fill="#f0cf91" {S}/>
<rect x="12" y="104" width="62" height="96" rx="28" fill="#e9c27c" {S}/><rect x="216" y="104" width="62" height="96" rx="28" fill="#e9c27c" {S}/>
<rect x="56" y="128" width="178" height="66" rx="18" fill="#f6dca4" {S}/>
<rect x="40" y="196" width="14" height="42" rx="4" fill="#6b4423" {S}/><rect x="236" y="196" width="14" height="42" rx="4" fill="#6b4423" {S}/>
<path d="M56 30 H168 L158 78 Q108 92 70 76Z" fill="#ff8f9c" {S}/>
<path d="M82 154 Q128 182 170 152 L184 214 Q130 226 88 212Z" fill="#ff8f9c" {S}/>
<g transform="rotate(-9 100 100)"><rect x="66" y="64" width="84" height="64" rx="14" fill="#2b36c9" {S}/></g>
<g transform="rotate(8 170 110)"><rect x="128" y="76" width="78" height="58" rx="14" fill="#6b4eff" {S}/></g></svg>'''

TABLE = f'''<svg class="decor table" viewBox="0 0 160 300" aria-hidden="true">
<rect x="76" y="164" width="8" height="118" fill="#8a5a2f" {S} stroke-width="3"/>
<ellipse cx="80" cy="288" rx="34" ry="8" fill="#8a5a2f" {S} stroke-width="3"/>
<path d="M8 150 H152 V162 Q80 176 8 162Z" fill="#e9c27c" {S}/><ellipse cx="80" cy="150" rx="72" ry="13" fill="#f3d28f" {S}/>
<path d="M20 138 L68 132 L72 146 L26 152Z" fill="#d2f26f" {S} stroke-width="3"/>
<ellipse cx="84" cy="142" rx="30" ry="6" fill="#fdfbf4" {S} stroke-width="3"/>
<path d="M66 138 q0 -22 18 -22 q18 0 18 22z" fill="#e8a05a" {S} stroke-width="3"/><circle cx="76" cy="124" r="3" fill="#2b36c9"/><circle cx="90" cy="121" r="3" fill="#2b36c9"/>
<path d="M118 92 H140 L137 146 H121Z" fill="#c9c2ff" {S} stroke-width="3"/><path d="M130 100 L134 74" {S} stroke-width="3"/></svg>'''


PLANT = ('<svg class="decor plant" viewBox="0 0 150 300" aria-hidden="true">'
         + _leaf(75, 205, -62, .7, "#3b7d3f") + _leaf(75, 205, 60, .72, "#3b7d3f")
         + _leaf(75, 205, -36, 1.0, "#4f9a4f") + _leaf(75, 205, 34, .98, "#4f9a4f")
         + _leaf(75, 205, -8, 1.15, "#5fae58") + _leaf(75, 205, 14, .9, "#3b7d3f")
         + f'<path d="M30 212 H120 L110 288 H40Z" fill="#fdfbf4" {S}/><rect x="26" y="200" width="98" height="16" rx="5" fill="#d2f26f" {S}/></svg>')

CATCHER = '''<svg class="decor frame" viewBox="0 0 120 190" aria-hidden="true" style="overflow:visible"><defs>
<linearGradient id="mcg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8cdb4"/><stop offset=".4" stop-color="#f7f1e2"/><stop offset="1" stop-color="#cdbf9f"/></linearGradient>
<linearGradient id="mwd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c79a63"/><stop offset=".5" stop-color="#a97943"/><stop offset="1" stop-color="#7a5128"/></linearGradient></defs>
<path d="M60 0 L14 22 M60 0 L106 22" stroke="#d9c9a6" stroke-width="2.2" fill="none" stroke-linecap="round"/><circle cx="60" cy="0" r="3" fill="#8a6a43"/>
<g><rect x="8" y="20" width="104" height="7" rx="3.5" fill="url(#mwd)"/><rect x="8" y="20" width="104" height="2.4" rx="1.2" fill="#e8c999" opacity=".7"/><ellipse cx="9" cy="23.5" rx="2.2" ry="3.5" fill="#6b4423"/><ellipse cx="111" cy="23.5" rx="2.2" ry="3.5" fill="#6b4423"/>
<path d="M20 27 V34 M30 27 V34 M40 27 V34 M50 27 V34 M60 27 V34 M70 27 V34 M80 27 V34 M90 27 V34 M100 27 V34" stroke="#efe6d0" stroke-width="2.4" stroke-linecap="round"/>
<g transform="translate(0 -4)"><path d="M51 33 Q60 30 69 33 Q71 40 69 47 Q60 50 51 47 Q49 40 51 33Z" fill="url(#mcg)"/><path d="M53 38 H67 M53 42 H67" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M41 45 Q50 42 59 45 Q61 52 59 59 Q50 62 41 59 Q39 52 41 45Z" fill="url(#mcg)"/><path d="M43 50 H57 M43 54 H57" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M61 45 Q70 42 79 45 Q81 52 79 59 Q70 62 61 59 Q59 52 61 45Z" fill="url(#mcg)"/><path d="M63 50 H77 M63 54 H77" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M31 57 Q40 54 49 57 Q51 64 49 71 Q40 74 31 71 Q29 64 31 57Z" fill="url(#mcg)"/><path d="M33 62 H47 M33 66 H47" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M51 57 Q60 54 69 57 Q71 64 69 71 Q60 74 51 71 Q49 64 51 57Z" fill="url(#mcg)"/><path d="M53 62 H67 M53 66 H67" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M71 57 Q80 54 89 57 Q91 64 89 71 Q80 74 71 71 Q69 64 71 57Z" fill="url(#mcg)"/><path d="M73 62 H87 M73 66 H87" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M41 69 Q50 66 59 69 Q61 76 59 83 Q50 86 41 83 Q39 76 41 69Z" fill="url(#mcg)"/><path d="M43 74 H57 M43 78 H57" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M61 69 Q70 66 79 69 Q81 76 79 83 Q70 86 61 83 Q59 76 61 69Z" fill="url(#mcg)"/><path d="M63 74 H77 M63 78 H77" stroke="#b8a88a" stroke-width=".8" opacity=".7"/><path d="M51 81 Q60 78 69 81 Q71 88 69 95 Q60 98 51 95 Q49 88 51 81Z" fill="url(#mcg)"/><path d="M53 86 H67 M53 90 H67" stroke="#b8a88a" stroke-width=".8" opacity=".7"/></g>
<g transform="translate(0 0)"><path d="M26 82 Q25 104.0 26 126" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M26 120 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M31 100 Q32 125.0 31 150" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M31 144 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M36 100 Q35 128.0 36 156" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M36 150 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M41 100 Q42 135.0 41 170" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M41 164 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M46 100 Q45 137.0 46 174" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M46 168 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M51 100 Q52 138.0 51 176" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M51 170 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M56 100 Q55 139.0 56 178" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M56 172 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M61 100 Q62 138.0 61 176" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M61 170 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M66 100 Q65 137.0 66 174" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M66 168 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M71 100 Q72 135.0 71 170" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M71 164 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M76 100 Q75 132.0 76 164" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M76 158 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M81 100 Q82 129.0 81 158" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M81 152 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M86 100 Q85 122.0 86 144" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M86 138 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/><path d="M91 82 Q92 102.0 91 122" stroke="url(#mcg)" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M91 116 l0 6" stroke="#fffaf0" stroke-width="1" opacity=".5"/></g>
<animateTransform attributeName="transform" type="rotate" values="-1.2 60 20;1.2 60 20;-1.2 60 20" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></g>
<ellipse cx="60" cy="150" rx="46" ry="3" fill="#000" opacity="0"/></svg>'''


COUCH = """<svg class="decor couch" viewBox="0 0 420 230" aria-hidden="true">
<defs>
<linearGradient id="cb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e7dcc6"/><stop offset="1" stop-color="#cdbfa5"/></linearGradient>
<linearGradient id="cs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0e6d2"/><stop offset="1" stop-color="#d6c8ac"/></linearGradient>
<linearGradient id="ca" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfc1a6"/><stop offset=".5" stop-color="#e6dac3"/><stop offset="1" stop-color="#c4b698"/></linearGradient>
<linearGradient id="cn" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3d4fd0"/><stop offset="1" stop-color="#1f2a8f"/></linearGradient>
<linearGradient id="cc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffc2b1"/><stop offset="1" stop-color="#e98f7c"/></linearGradient>
<pattern id="cwv" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 3 H6 M3 0 V6" stroke="#fff" stroke-opacity=".10" stroke-width=".8"/></pattern>
<radialGradient id="cpf" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient>
<radialGradient id="csh"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
<ellipse cx="210" cy="222" rx="200" ry="14" fill="url(#csh)"/>
<rect x="46" y="196" width="10" height="26" rx="3" fill="#6b4423"/><rect x="364" y="196" width="10" height="26" rx="3" fill="#6b4423"/>
<rect x="40" y="38" width="340" height="110" rx="26" fill="url(#cb)"/>
<path d="M150 44 V140 M270 44 V140" stroke="#000" stroke-opacity=".1" stroke-width="3"/>
<rect x="4" y="86" width="62" height="112" rx="28" fill="url(#ca)"/><rect x="354" y="86" width="62" height="112" rx="28" fill="url(#ca)"/>
<rect x="56" y="118" width="308" height="80" rx="20" fill="url(#cs)"/>
<path d="M210 126 V194" stroke="#000" stroke-opacity=".12" stroke-width="3"/>
<rect x="56" y="186" width="308" height="14" rx="6" fill="#bfb090"/>

</svg>"""

LAMP = """<svg class="decor lamp" viewBox="0 0 120 470" aria-hidden="true" style="overflow:visible">
<defs><linearGradient id="lb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f4f1ea"/><stop offset=".6" stop-color="#cfc8ba"/><stop offset="1" stop-color="#8d867a"/></linearGradient>
<linearGradient id="lg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6a2b"/><stop offset=".45" stop-color="#e8cd84"/><stop offset="1" stop-color="#8a6a2b"/></linearGradient>
<radialGradient id="lglow"><stop offset="0" stop-color="#fff2b8" stop-opacity=".35"/><stop offset="1" stop-color="#fff2b8" stop-opacity="0"/></radialGradient>
<radialGradient id="lsh"><stop offset="0" stop-color="#000" stop-opacity=".4"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="lglobe" cx=".35" cy=".3"><stop offset="0" stop-color="#fffdf2"/><stop offset="1" stop-color="#f3e3b0"/></radialGradient></defs>
<circle cx="60" cy="70" r="130" fill="url(#lglow)"/>
<ellipse cx="60" cy="462" rx="46" ry="9" fill="url(#lsh)"/>
<path d="M30 456 Q30 438 60 438 Q90 438 90 456Z" fill="url(#lb)"/><ellipse cx="60" cy="456" rx="30" ry="5" fill="#8d867a"/>
<rect x="57" y="120" width="6" height="320" fill="url(#lg)"/>
<circle cx="60" cy="70" r="44" fill="url(#lglobe)"/><ellipse cx="46" cy="54" rx="12" ry="8" fill="#fff" opacity=".55"/>
<rect x="46" y="108" width="28" height="12" rx="3" fill="url(#lg)"/></svg>"""

ALL = LAMP + WINDOW + COUCH + CATCHER
