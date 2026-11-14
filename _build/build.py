"""Generates every SVG in ../assets for the GitHub profile README.

Run:  python _build/build.py
All artwork is hand-built SVG with CSS animations (GitHub renders these inside <img>).
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "'Inter','Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

BG = "#06080C"
PANEL = "#0B0F16"
LINE = "#1A212C"
TEXT = "#EEF2F7"
SOFT = "#C3CCD8"
MUTED = "#8B98AA"
DIM = "#4E5968"
CYAN = "#5EEAD4"
VIOLET = "#A78BFA"
GREEN = "#34D399"
RED = "#F87171"
AMBER = "#FBBF24"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, style="", title=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>
text{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
{style}
</style>
{body}
</svg>
"""


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"  wrote assets/{name} ({len(content)//1024 or 1} KB)")


def common_defs(uid):
    return f"""
<pattern id="grid{uid}" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M40 0H0V40" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1"/>
</pattern>
<radialGradient id="glowV{uid}" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(160 40) rotate(35) scale(620 360)">
  <stop stop-color="{VIOLET}" stop-opacity="0.22"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowC{uid}" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(980 420) rotate(-20) scale(560 320)">
  <stop stop-color="{CYAN}" stop-opacity="0.16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
</radialGradient>"""


def pill(x, y, label, color=SOFT, stroke=LINE, h=34, fs=14, mono=False, fill="#FFFFFF", fill_op=0.025, char_w=None):
    cw = char_w or (fs * (0.62 if mono else 0.56))
    w = int(len(label) * cw + 32)
    cls = ' class="mono"' if mono else ""
    return w, (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" fill-opacity="{fill_op}" stroke="{stroke}"/>'
               f'<text{cls} x="{x + w/2}" y="{y + h/2 + fs*0.36:.1f}" font-size="{fs}" fill="{color}" text-anchor="middle" letter-spacing="0.2">{esc(label)}</text>')


# --------------------------------------------------------------------------- HERO
def hero():
    W, H = 1200, 500
    rnd = random.Random(108)
    n = 28
    price = 100.0
    candles = []
    for i in range(n):
        drift = 0.55 if i > 6 else -0.25
        o = price
        c = o + rnd.gauss(drift, 2.1)
        hi = max(o, c) + abs(rnd.gauss(0, 1.3))
        lo = min(o, c) - abs(rnd.gauss(0, 1.3))
        candles.append((o, hi, lo, c))
        price = c
    pmin = min(c[2] for c in candles) - 2
    pmax = max(c[1] for c in candles) + 2
    cx0, cx1, cy0, cy1 = 742, 1112, 150, 362

    def py(p):
        return cy1 - (p - pmin) / (pmax - pmin) * (cy1 - cy0)

    step = (cx1 - cx0) / (n - 1)
    parts = []
    for i, (o, hi, lo, c) in enumerate(candles):
        x = cx0 + i * step
        col = GREEN if c >= o else RED
        top, bot = py(max(o, c)), py(min(o, c))
        parts.append(
            f'<g class="cd" style="animation-delay:{0.25 + i*0.045:.3f}s">'
            f'<line x1="{x:.1f}" y1="{py(hi):.1f}" x2="{x:.1f}" y2="{py(lo):.1f}" stroke="{col}" stroke-opacity="0.75" stroke-width="1.4"/>'
            f'<rect x="{x-4.5:.1f}" y="{top:.1f}" width="9" height="{max(bot-top, 1.6):.1f}" rx="1.5" fill="{col}"/></g>')
    closes = [c[3] for c in candles]
    ma = []
    for i in range(n):
        win = closes[max(0, i - 4): i + 1]
        ma.append(sum(win) / len(win))
    pts = [(cx0 + i * step, py(v)) for i, v in enumerate(ma)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx = (x0 + x1) / 2
        d += f" C{mx:.1f} {y0:.1f} {mx:.1f} {y1:.1f} {x1:.1f} {y1:.1f}"
    area = d + f" L{cx1:.1f} {cy1 + 14} L{cx0:.1f} {cy1 + 14} Z"
    last = closes[-1]
    ly = py(last)
    gain = (last - closes[0]) / closes[0] * 100

    ticker_items = ["PYTHON", "C++", "SQL", "TYPESCRIPT", "REACT", "FASTAPI", "PYTORCH", "SCIKIT-LEARN",
                    "DOCKER", "AWS", "AZURE", "POSTGRES", "JAVA", "R", "STREAMLIT", "NODE.JS"]
    seg = "".join(f'<tspan fill="{SOFT}">{t}</tspan><tspan fill="{GREEN}"> ▲ </tspan><tspan fill="{DIM}">·  </tspan>' for t in ticker_items)
    seg_w = 1480

    pills_svg = []
    px = 64
    for label in ["Quant & trading systems", "Machine learning", "Full-stack + AI agents"]:
        w, s = pill(px, 352, label, fs=14.5)
        pills_svg.append(s)
        px += w + 12

    style = f"""
.fade{{opacity:0;animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}}
.d1{{animation-delay:.05s}}.d2{{animation-delay:.18s}}.d3{{animation-delay:.32s}}.d4{{animation-delay:.46s}}.d5{{animation-delay:.6s}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.cd{{opacity:0;animation:cd .5s ease-out forwards}}
@keyframes cd{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.ma{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.2s 1.1s cubic-bezier(.6,.1,.2,1) forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.area{{opacity:0;animation:fadein 1.2s 2.4s forwards}}
.tag{{opacity:0;animation:fadein .6s 2.9s forwards}}
@keyframes fadein{{to{{opacity:1}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
@keyframes pulse{{0%{{opacity:.7;transform:scale(1)}}100%{{opacity:0;transform:scale(3.2)}}}}
.tick{{animation:tick 38s linear infinite}}
@keyframes tick{{to{{transform:translateX(-{seg_w}px)}}}}
.blink{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
"""
    body = f"""
<defs>{common_defs('h')}
<linearGradient id="nameG" x1="60" y1="120" x2="640" y2="240" gradientUnits="userSpaceOnUse">
  <stop stop-color="#FFFFFF"/><stop offset=".55" stop-color="#DCE3EC"/><stop offset="1" stop-color="{CYAN}"/>
</linearGradient>
<linearGradient id="areaG" x1="0" y1="{cy0}" x2="0" y2="{cy1+14}" gradientUnits="userSpaceOnUse">
  <stop stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
  <stop stop-color="{VIOLET}" stop-opacity="0"/><stop offset=".3" stop-color="{VIOLET}" stop-opacity=".7"/><stop offset=".7" stop-color="{CYAN}" stop-opacity=".7"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
</linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="tickClip"><rect x="0" y="{H-58}" width="{W}" height="58"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#gridh)"/>
<rect width="{W}" height="{H}" fill="url(#glowVh)"/>
<rect width="{W}" height="{H}" fill="url(#glowCh)"/>
<rect x="0" y="0" width="{W}" height="1.5" fill="url(#edge)"/>

<g class="fade d1">
  <circle class="pulse" cx="71" cy="86" r="5" fill="{GREEN}"/>
  <circle cx="71" cy="86" r="5" fill="{GREEN}"/>
  <text class="mono" x="88" y="91" font-size="13" fill="{MUTED}" letter-spacing="2.6">OPEN TO SWE · QUANT · DATA INTERNSHIPS</text>
</g>
<text class="fade d2" x="56" y="222" font-size="128" font-weight="800" letter-spacing="-6" fill="url(#nameG)">Eli K.</text>
<text class="fade d3" x="62" y="274" font-size="25" font-weight="500" fill="{SOFT}" letter-spacing="-0.3">Software &amp; analytics that bring clarity to complex markets.</text>
<text class="fade d4" x="63" y="312" font-size="16.5" fill="{MUTED}">Computer Science <tspan fill="{DIM}">·</tspan> University of Calgary <tspan fill="{DIM}">·</tspan> Software engineer &amp; digital strategist</text>
<g class="fade d5">{''.join(pills_svg)}</g>

<g class="fade d3">
  <rect x="712" y="70" width="430" height="338" rx="20" fill="#FFFFFF" fill-opacity="0.022" stroke="{LINE}"/>
  <text class="mono" x="740" y="106" font-size="12.5" fill="{MUTED}" letter-spacing="1.6">EYU108 / USD  <tspan fill="{DIM}">·  1D</tspan></text>
  <text class="mono tag" x="1114" y="106" font-size="13" fill="{GREEN}" text-anchor="end" font-weight="700">▲ {gain:.2f}%</text>
  <line x1="740" y1="122" x2="1114" y2="122" stroke="{LINE}"/>
  {''.join(f'<line x1="740" y1="{y}" x2="1114" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.035" stroke-dasharray="2 6"/>' for y in range(170, 380, 52))}
</g>
<path class="area" d="{area}" fill="url(#areaG)"/>
{''.join(parts)}
<path class="ma" d="{d}" pathLength="1" stroke="{CYAN}" stroke-width="2.6" stroke-linecap="round"/>
<g class="tag">
  <line x1="740" y1="{ly:.1f}" x2="1114" y2="{ly:.1f}" stroke="{GREEN}" stroke-opacity=".5" stroke-dasharray="3 5"/>
  <circle class="pulse" cx="{cx1:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="{CYAN}"/>
  <circle cx="{cx1:.1f}" cy="{pts[-1][1]:.1f}" r="4" fill="{CYAN}"/>
  <text class="mono" x="742" y="392" font-size="11.5" fill="{DIM}" letter-spacing="1.2">MA(5) <tspan fill="{CYAN}">━</tspan>   VOL <tspan fill="{SOFT}">HIGH</tspan>   SIGNAL <tspan fill="{GREEN}">LONG</tspan><tspan class="blink" fill="{CYAN}"> ▍</tspan></text>
</g>

<g clip-path="url(#tickClip)">
  <rect x="0" y="{H-58}" width="{W}" height="58" fill="#FFFFFF" fill-opacity="0.025"/>
  <line x1="0" y1="{H-58}" x2="{W}" y2="{H-58}" stroke="{LINE}"/>
  <g class="tick">
    <text class="mono" x="0" y="{H-23}" font-size="13.5" letter-spacing="2.2" textLength="{seg_w}" lengthAdjust="spacing">{seg}</text>
    <text class="mono" x="{seg_w}" y="{H-23}" font-size="13.5" letter-spacing="2.2" textLength="{seg_w}" lengthAdjust="spacing">{seg}</text>
  </g>
</g>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="27.5" stroke="#FFFFFF" stroke-opacity="0.07"/>
"""
    write("hero.svg", svg(W, H, body, style, "Eli K. — Software & analytics that bring clarity to complex markets"))


# --------------------------------------------------------------------------- SECTION HEADERS
def headers():
    items = [("01", "now", "Now building", "what's on the workbench"),
             ("02", "work", "Selected work", "live demos + source"),
             ("03", "stack", "Toolkit", "what I build with"),
             ("04", "focus", "Where I focus", "domains + impact"),
             ("05", "contact", "Let's build something", "say hi")]
    for num, slug, title, sub in items:
        for theme, fg, mu, ln in (("dark", TEXT, MUTED, "#2A3340"), ("light", "#0B1220", "#5B6677", "#D5DCE5")):
            W, H = 1200, 84
            tw = len(title) * 17.2 + 96
            style = f""".grow{{transform-origin:left;transform:scaleX(0);animation:grow 1.4s .2s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes grow{{to{{transform:scaleX(1)}}}}"""
            body = f"""<defs><linearGradient id="hl" x1="{tw}" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="{CYAN}" stop-opacity=".9"/><stop offset=".35" stop-color="{VIOLET}" stop-opacity=".45"/><stop offset="1" stop-color="{ln}" stop-opacity="0"/></linearGradient></defs>
<text class="mono" x="2" y="52" font-size="15" font-weight="700" fill="{CYAN if theme == 'dark' else '#0D9488'}" letter-spacing="1">{num}</text>
<text x="40" y="54" font-size="30" font-weight="750" fill="{fg}" letter-spacing="-0.8">{esc(title)}</text>
<rect class="grow" x="{tw:.0f}" y="44" width="{W - tw - 170:.0f}" height="1.5" fill="url(#hl)"/>
<text class="mono" x="{W - 2}" y="50" font-size="12.5" fill="{mu}" text-anchor="end" letter-spacing="1.6">{esc(sub.upper())}</text>"""
            write(f"h-{slug}-{theme}.svg", svg(W, H, body, style, title))


# --------------------------------------------------------------------------- NOW (terminal)
def now():
    W, H = 1200, 372
    lines = [
        ("cmd", "whoami --short"),
        ("out", f'<tspan fill="{SOFT}">CS @ University of Calgary</tspan><tspan fill="{DIM}">  ·  </tspan><tspan fill="{SOFT}">software + data + markets</tspan>'),
        ("cmd", "ls ~/building"),
        ("row", ("ai-receptionist", "voice + SMS agent that answers calls and books appointments for small businesses")),
        ("row", ("prediction-bot", "15-minute BTC prediction-market trading system, hybrid signals + risk limits")),
        ("row", ("nq-indicator", "TradingView indicator & strategy for NQ futures, validated with a Python backtester")),
        ("cmd", "echo $GOAL"),
        ("out", f'<tspan fill="{CYAN}">ship things people actually use</tspan>'),
    ]
    y = 104
    rows = []
    for i, (kind, val) in enumerate(lines):
        delay = 0.3 + i * 0.32
        g = f'<g class="ln" style="animation-delay:{delay:.2f}s">'
        if kind == "cmd":
            rows.append(f'{g}<text class="mono" x="44" y="{y}" font-size="16"><tspan fill="{GREEN}">➜</tspan><tspan fill="{VIOLET}">  ~</tspan><tspan fill="{TEXT}">  {esc(val)}</tspan></text></g>')
            y += 30
        elif kind == "out":
            rows.append(f'{g}<text class="mono" x="70" y="{y}" font-size="16">{val}</text></g>')
            y += 40
        else:
            name, desc = val
            rows.append(f'{g}<text class="mono" x="70" y="{y}" font-size="16"><tspan fill="{CYAN}">▸ {esc(name)}</tspan></text>'
                        f'<text x="300" y="{y}" font-size="16" fill="{MUTED}">{esc(desc)}</text></g>')
            y += 30 if i < 5 else 40
    cursor_delay = 0.3 + len(lines) * 0.32
    style = f""".ln{{opacity:0;animation:ln .45s ease-out forwards}}
@keyframes ln{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
.cur{{opacity:0;animation:on 0s {cursor_delay:.2f}s forwards, blink 1s {cursor_delay:.2f}s steps(1) infinite}}
@keyframes on{{to{{opacity:1}}}}
@keyframes blink{{50%{{opacity:0}}}}"""
    body = f"""<defs>{common_defs('n')}<clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<rect width="{W}" height="{H}" fill="url(#gridn)" opacity=".6"/>
<rect width="{W}" height="52" fill="#FFFFFF" fill-opacity="0.03"/>
<line x1="0" y1="52" x2="{W}" y2="52" stroke="{LINE}"/>
<circle cx="32" cy="26" r="6.5" fill="#FF5F57"/><circle cx="54" cy="26" r="6.5" fill="#FEBC2E"/><circle cx="76" cy="26" r="6.5" fill="#28C840"/>
<text class="mono" x="{W/2}" y="31" font-size="13" fill="{MUTED}" text-anchor="middle" letter-spacing="1">eli@calgary — ~/now — zsh</text>
{''.join(rows)}
<rect class="cur" x="{70 + 30 * 9.65 + 8:.0f}" y="{y - 40 - 15}" width="10" height="19" fill="{CYAN}"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="21.5" stroke="#FFFFFF" stroke-opacity="0.08"/>"""
    write("now.svg", svg(W, H, body, style, "Now building: AI receptionist, prediction-market trading bot, NQ futures indicator"))


# --------------------------------------------------------------------------- PROJECT CARDS
def card(slug, num, kicker, title, desc_lines, tags, visual, badge, accent, style_extra=""):
    W, H = 600, 360
    tag_svg, tx = [], 32
    for t in tags:
        w, s = pill(tx, 306, t, color=SOFT, h=28, fs=12, mono=True, char_w=7.6)
        tag_svg.append(s)
        tx += w + 8
    bw, bs = pill(W - 32 - (len(badge) * 7.4 + 32), 24, badge, color=accent, stroke=accent, h=28, fs=11.5, mono=True,
                  fill=accent, fill_op=0.08, char_w=7.4)
    desc = "".join(f'<text x="32" y="{248 + i*22}" font-size="15" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(desc_lines))
    style = f""".rise{{opacity:0;animation:rise .8s .1s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes fadein{{to{{opacity:1}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
@keyframes pulse{{0%{{opacity:.7;transform:scale(1)}}100%{{opacity:0;transform:scale(3)}}}}
{style_extra}"""
    body = f"""<defs>{common_defs('c'+slug)}
<radialGradient id="spot" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(470 40) scale(380 240)">
<stop stop-color="{accent}" stop-opacity=".16"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<clipPath id="cc"><rect width="{W}" height="{H}" rx="22"/></clipPath></defs>
<g clip-path="url(#cc)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<rect width="{W}" height="{H}" fill="url(#spot)"/>
<rect width="{W}" height="180" fill="url(#gridc{slug})" opacity=".8"/>
<line x1="0" y1="180" x2="{W}" y2="180" stroke="{LINE}"/>
{visual}
<text class="mono" x="32" y="40" font-size="12" fill="{accent}" letter-spacing="2">{num} · {esc(kicker)}</text>
{bs}
<g class="rise">
<text x="32" y="220" font-size="25" font-weight="750" fill="{TEXT}" letter-spacing="-0.6">{esc(title)}</text>
{desc}
{''.join(tag_svg)}
</g>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="21.5" stroke="#FFFFFF" stroke-opacity="0.08"/>"""
    write(f"card-{slug}.svg", svg(W, H, body, style, title))


def cards():
    # 1. Backtester: strategy vs benchmark equity curves with trade markers
    rnd = random.Random(7)
    s, b = 120.0, 120.0
    sp, bp = [], []
    for i in range(40):
        s -= rnd.gauss(0.9, 1.6) * (1 if i > 3 else -0.3)
        b -= rnd.gauss(0.35, 1.9)
        sp.append((40 + i * 13.3, s))
        bp.append((40 + i * 13.3, b))

    def path(p):
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
    marks = ""
    for k, i in enumerate([6, 14, 22, 31]):
        x, y = sp[i]
        up = k % 2 == 0
        tri = f"{x-6:.1f},{y+16:.1f} {x+6:.1f},{y+16:.1f} {x:.1f},{y+6:.1f}" if up else f"{x-6:.1f},{y-16:.1f} {x+6:.1f},{y-16:.1f} {x:.1f},{y-6:.1f}"
        marks += f'<polygon class="mk" style="animation-delay:{1.0 + k*0.35:.2f}s" points="{tri}" fill="{GREEN if up else RED}"/>'
    ex, ey = sp[-1]
    v1 = f"""<path d="{path(bp)}" stroke="{DIM}" stroke-width="2" stroke-dasharray="4 5" class="bfade"/>
<path class="eq" d="{path(sp)}" pathLength="1" stroke="{CYAN}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>
{marks}
<circle class="pulse" cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{CYAN}"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{CYAN}"/>
<text class="mono" x="32" y="166" font-size="11" fill="{DIM}" letter-spacing="1">STRATEGY <tspan fill="{CYAN}">━</tspan>  BUY &amp; HOLD <tspan fill="{MUTED}">┅</tspan>   SHARPE <tspan fill="{GREEN}">1.84</tspan></text>"""
    card("backtester", "01", "QUANT", "Trading Strategy Backtester",
         ["Momentum (SMA crossover) and mean-reversion (RSI)", "strategies with risk metrics, in an interactive app."],
         ["Python", "Streamlit", "Pandas", "Plotly"], v1, "LIVE DEMO ↗", CYAN,
         """.eq{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.4s .3s cubic-bezier(.6,.1,.2,1) forwards}
.mk{opacity:0;animation:fadein .4s forwards}.bfade{opacity:0;animation:fadein 1s .2s forwards}""")

    # 2. Risk analyzer: return distribution with VaR tail
    bars = ""
    nb = 31
    for i in range(nb):
        z = (i - nb * 0.55) / 5.2
        h = 112 * math.exp(-z * z / 2) + 6
        x = 44 + i * 16.8
        tail = i < 6
        bars += (f'<rect class="bar" style="animation-delay:{0.1 + i*0.03:.2f}s" x="{x:.1f}" y="{150 - h:.1f}" width="11.5" height="{h:.1f}" rx="2" '
                 f'fill="{RED if tail else VIOLET}" fill-opacity="{0.95 if tail else 0.55 + 0.4*math.exp(-z*z/2):.2f}"/>')
    vx = 44 + 6 * 16.8 - 2.6
    v2 = f"""{bars}
<g class="var"><line x1="{vx:.1f}" y1="34" x2="{vx:.1f}" y2="152" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4 4"/>
<text class="mono" x="{vx + 8:.1f}" y="70" font-size="11" fill="{RED}" letter-spacing="1">VaR 95%</text>
<text class="mono" x="{vx + 8:.1f}" y="86" font-size="11" fill="{MUTED}" letter-spacing="1">CVaR −3.1%</text></g>
<line x1="32" y1="152" x2="568" y2="152" stroke="{LINE}"/>
<text class="mono" x="32" y="170" font-size="11" fill="{DIM}" letter-spacing="1">DAILY RETURNS  ·  β <tspan fill="{SOFT}">0.87</tspan>  ·  σ <tspan fill="{SOFT}">14.2%</tspan></text>"""
    card("risk", "02", "RISK", "Market Risk &amp; Portfolio Analyzer".replace("&amp;", "&"),
         ["VaR / CVaR, rolling beta, factor regression and", "volatility modelling for any portfolio."],
         ["Python", "Streamlit", "Risk", "Factor models"], v2, "LIVE DEMO ↗", VIOLET,
         """.bar{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .7s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes grow{to{transform:scaleY(1)}}.var{opacity:0;animation:fadein .6s 1.3s forwards}""")

    # 3. Facial recognition: landmark mesh + scanning bar + bounding box
    cx, cy = 330, 108
    dots = ""
    pts = []
    for a in range(0, 360, 15):
        r = math.radians(a)
        pts.append((cx + 44 * math.sin(r), cy - 56 * math.cos(r)))
    pts += [(cx - 19, cy - 12), (cx + 19, cy - 12), (cx - 26, cy - 15), (cx - 12, cy - 15), (cx + 12, cy - 15), (cx + 26, cy - 15),
            (cx, cy + 3), (cx - 7, cy + 12), (cx + 7, cy + 12), (cx - 17, cy + 27), (cx, cy + 31), (cx + 17, cy + 27), (cx, cy - 34)]
    mesh = ""
    for i, (x, y) in enumerate(pts):
        dots += f'<circle class="dt" style="animation-delay:{0.2 + i*0.03:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{GREEN}"/>'
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[j]
            if math.hypot(x1 - x2, y1 - y2) < 26:
                mesh += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GREEN}" stroke-opacity=".28" stroke-width="1"/>'
    bx0, by0, bx1, by1 = cx - 66, cy - 70, cx + 66, cy + 64
    L = 16
    corners = (f"M{bx0} {by0+L}V{by0}H{bx0+L} M{bx1-L} {by0}H{bx1}V{by0+L} M{bx1} {by1-L}V{by1}H{bx1-L} M{bx0+L} {by1}H{bx0}V{by1-L}")
    v3 = f"""<g class="meshf">{mesh}</g>{dots}
<path d="{corners}" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round" class="box"/>
<rect class="scan" x="{bx0}" y="{by0}" width="{bx1-bx0}" height="3" fill="{GREEN}" fill-opacity=".85"/>
<g class="lbl"><rect x="{bx1 + 16}" y="{cy - 8}" width="118" height="26" rx="6" fill="{GREEN}" fill-opacity=".12" stroke="{GREEN}" stroke-opacity=".5"/>
<text class="mono" x="{bx1 + 26}" y="{cy + 9}" font-size="11.5" fill="{GREEN}" letter-spacing="1">MATCH 0.97</text>
<text class="mono" x="{bx1 + 18}" y="{cy + 38}" font-size="11" fill="{MUTED}" letter-spacing="1">ID: SUBJECT_04</text>
<text class="mono" x="{bx1 + 18}" y="{cy + 56}" font-size="11" fill="{DIM}" letter-spacing="1">30 FPS · 68 PTS</text>
<line x1="{bx1}" y1="{cy + 5}" x2="{bx1 + 16}" y2="{cy + 5}" stroke="{GREEN}" stroke-opacity=".5"/></g>"""
    card("face", "03", "COMPUTER VISION", "Facial Recognition System",
         ["Detects and identifies faces in video with OpenCV", "and face_recognition, trained on custom data."],
         ["Python", "OpenCV", "face_recognition"], v3, "SOURCE ↗", GREEN,
         f""".dt{{opacity:0;animation:fadein .3s forwards}}.meshf{{opacity:0;animation:fadein 1s 1s forwards}}
.box{{opacity:0;animation:fadein .4s 1.3s forwards}}.lbl{{opacity:0;animation:fadein .5s 1.8s forwards}}
.scan{{animation:scan 2.6s ease-in-out infinite alternate}}
@keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY({by1-by0-3}px)}}}}""")

    # 4. Self checkout: barcode + laser + receipt
    rnd = random.Random(11)
    bars = ""
    x = 70
    while x < 290:
        w = rnd.choice([2, 2, 3, 4, 6])
        bars += f'<rect x="{x}" y="72" width="{w}" height="78" fill="{TEXT}" fill-opacity=".9"/>'
        x += w + rnd.choice([2, 3, 4])
    receipt = ""
    items = [("ESPRESSO BEANS", "18.99"), ("OAT MILK 1L", "4.49"), ("SOURDOUGH", "6.25"), ("TOTAL", "29.73")]
    for i, (it, pr) in enumerate(items):
        yy = 84 + i * 20
        col = AMBER if it == "TOTAL" else SOFT
        receipt += (f'<g class="rc" style="animation-delay:{0.8 + i*0.4:.1f}s"><text class="mono" x="352" y="{yy}" font-size="11.5" fill="{col}" letter-spacing=".5">{it}</text>'
                    f'<text class="mono" x="548" y="{yy}" font-size="11.5" fill="{col}" text-anchor="end">${pr}</text></g>')
    v4 = f"""<rect x="56" y="62" width="248" height="98" rx="10" fill="#FFFFFF" fill-opacity=".03" stroke="{LINE}"/>
{bars}
<rect class="laser" x="62" y="110" width="236" height="2.5" fill="{RED}"/>
<rect class="laser" x="62" y="106" width="236" height="10" fill="{RED}" fill-opacity=".18"/>
<rect x="336" y="62" width="228" height="98" rx="8" fill="#FFFFFF" fill-opacity=".03" stroke="{LINE}" stroke-dasharray="3 4"/>
<line x1="352" y1="134" x2="548" y2="134" stroke="{DIM}" stroke-dasharray="2 3" class="rc" style="animation-delay:1.9s"/>
{receipt}
<text class="mono" x="56" y="172" font-size="11" fill="{DIM}" letter-spacing="1">SESSION <tspan fill="{GREEN}">ACTIVE</tspan>  ·  PAY <tspan fill="{SOFT}">CASH / CARD</tspan></text>"""
    card("checkout", "04", "SOFTWARE ENGINEERING", "Self-Checkout System",
         ["Retail self-checkout in Java: sessions, payments,", "predictive resource management and a GUI."],
         ["Java", "OOP", "GUI", "Hardware I/O"], v4, "SOURCE ↗", AMBER,
         """.laser{animation:laser 1.8s ease-in-out infinite alternate}
@keyframes laser{from{transform:translateY(-34px)}to{transform:translateY(34px)}}
.rc{opacity:0;animation:fadein .4s forwards}""")


# --------------------------------------------------------------------------- FOCUS
def focus():
    W, H = 1200, 330
    cols = [
        (CYAN, "ENERGY & FINANCE", "Markets, modelled.",
         ["Forecasting pipelines explained with SHAP", "Backtests with costs + walk-forward splits", "VaR / CVaR and factor risk tooling"],
         "chart"),
        (VIOLET, "SOFTWARE ENGINEERING", "Built to ship.",
         ["Full-stack apps: React + FastAPI / Node", "APIs and real-time dashboards", "Dockerised cloud deployments"],
         "code"),
        (GREEN, "RESEARCH & AI", "Curious by default.",
         ["Modelling & quantitative research", "Green computing", "AI for education equity"],
         "spark"),
    ]
    body_cols = ""
    for i, (acc, kick, head, bullets, icon) in enumerate(cols):
        x = i * 404
        w = 388
        if icon == "chart":
            ic = f'<path d="M{x+34} {82} l12 -10 l10 6 l16 -18" stroke="{acc}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="{x+72}" cy="60" r="3" fill="{acc}"/>'
        elif icon == "code":
            ic = f'<path d="M{x+44} 58 l-10 12 l10 12 M{x+66} 58 l10 12 l-10 12 M{x+60} 54 l-10 32" stroke="{acc}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        else:
            ic = f'<path d="M{x+55} 52 l4 12 l12 4 l-12 4 l-4 12 l-4 -12 l-12 -4 l12 -4 z" stroke="{acc}" stroke-width="2.2" stroke-linejoin="round"/>'
        bl = "".join(
            f'<circle cx="{x+40}" cy="{196 + j*36 - 5}" r="3" fill="{acc}"/><text x="{x+54}" y="{196 + j*36}" font-size="15.5" fill="{SOFT}">{esc(b)}</text>'
            for j, b in enumerate(bullets))
        body_cols += f"""<g class="col" style="animation-delay:{0.1 + i*0.15:.2f}s">
<rect x="{x+.5}" y=".5" width="{w-1}" height="{H-1}" rx="20" fill="{PANEL}" stroke="#FFFFFF" stroke-opacity=".08"/>
<rect x="{x+24}" y="44" width="52" height="52" rx="14" fill="{acc}" fill-opacity=".1" stroke="{acc}" stroke-opacity=".35"/>
{ic}
<text class="mono" x="{x+28}" y="128" font-size="11.5" fill="{acc}" letter-spacing="2">{esc(kick)}</text>
<text x="{x+28}" y="158" font-size="23" font-weight="750" fill="{TEXT}" letter-spacing="-0.5">{esc(head)}</text>
{bl}
</g>"""
    style = """.col{opacity:0;animation:rise .8s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"""
    write("focus.svg", svg(W, H, body_cols, style, "Focus: energy & finance, software engineering, research & AI"))


# --------------------------------------------------------------------------- BUTTONS
def buttons():
    specs = [
        ("linkedin", "LinkedIn", "#0A66C2",
         '<rect x="22" y="17" width="22" height="22" rx="5" fill="#0A66C2"/><text x="33" y="34" font-size="13" font-weight="800" fill="#fff" text-anchor="middle">in</text>'),
    ]
    for slug, label, acc, icon in specs:
        W, H = 196, 56
        body = f"""<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="{PANEL}" stroke="{acc}" stroke-opacity=".55" stroke-width="1.5"/>
{icon}
<text x="58" y="34" font-size="16" font-weight="650" fill="{TEXT}">{label}</text>
<text x="{W-22}" y="34" font-size="15" fill="{acc}" text-anchor="end">↗</text>"""
        write(f"btn-{slug}.svg", svg(W, H, body, "", label))


# --------------------------------------------------------------------------- FOOTER
def footer():
    W, H = 1200, 150
    rnd = random.Random(21)
    y = 80
    pts = []
    for i in range(61):
        y += rnd.gauss(-0.35, 4)
        y = max(40, min(118, y))
        pts.append((i * 20, y))
    d = "M" + " L".join(f"{x} {yy:.1f}" for x, yy in pts)
    ex, ey = pts[-1]
    style = """.ln{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 3s cubic-bezier(.6,.1,.2,1) forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.txt{opacity:0;animation:fadein 1s 1.2s forwards}@keyframes fadein{to{opacity:1}}"""
    body = f"""<defs><linearGradient id="fl" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="{VIOLET}" stop-opacity="0"/><stop offset=".25" stop-color="{VIOLET}" stop-opacity=".8"/><stop offset="1" stop-color="{CYAN}"/></linearGradient></defs>
<path class="ln" d="{d}" pathLength="1" stroke="url(#fl)" stroke-width="2.2" stroke-linejoin="round"/>
<circle cx="{ex-2}" cy="{ey:.1f}" r="5" fill="{CYAN}" class="txt"/>
<text class="mono txt" x="{W/2}" y="142" font-size="12.5" fill="{MUTED}" text-anchor="middle" letter-spacing="3">THANKS FOR STOPPING BY  ·  ALWAYS SHIPPING</text>"""
    write("footer.svg", svg(W, H, body, style, "Thanks for stopping by"))


if __name__ == "__main__":
    hero(); headers(); now(); cards(); focus(); buttons(); footer()
    print("done")
