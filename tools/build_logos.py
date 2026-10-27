"""Generate Himalayas Tech Solution logo files (outlined SVG + PNG)."""
import os, sys, zipfile
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

OUT = sys.argv[1]
FD = "/usr/share/fonts/truetype/google-fonts/"
BOLD = TTFont(FD + "Poppins-Bold.ttf")
MED = TTFont(FD + "Poppins-Medium.ttf")

NAVY, TEAL, TEAL_LT, SLATE, ICE, WHITE = "#0F2A44", "#1F8F86", "#2BB3A8", "#4A5B6C", "#F7F9FB", "#FFFFFF"
NAVY_TILE = "#163A5C"

SCHEMES = {
    "color":    dict(mark=NAVY,  dot=TEAL,    name=NAVY,  sub=SLATE,     tag=TEAL,    rule="#C9D3DD"),
    "reversed": dict(mark=WHITE, dot=TEAL_LT, name=WHITE, sub="#B8C7D6", tag=TEAL_LT, rule="#3A5878"),
    "black":    dict(mark="#000000", dot="#000000", name="#000000", sub="#000000", tag="#000000", rule="#000000"),
    "white":    dict(mark=WHITE, dot=WHITE,   name=WHITE, sub=WHITE,     tag=WHITE,   rule=WHITE),
}

def text_run(font, text, size, track_em, fill, x, baseline, anchor="start"):
    """Outlined text. Returns (svg, width). x is left edge (or centre if anchor='middle')."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    s = size / upm
    track = track_em * size
    glyphs = [cmap[ord(c)] for c in text]
    adv = [font["hmtx"][g][0] * s for g in glyphs]
    width = sum(adv) + track * (len(text) - 1)
    cx = x - width / 2 if anchor == "middle" else x
    parts = []
    for g, a in zip(glyphs, adv):
        pen = SVGPathPen(gs)
        gs[g].draw(pen)
        d = pen.getCommands()
        if d:
            parts.append(f'<path transform="translate({cx:.2f} {baseline:.2f}) scale({s:.5f} {-s:.5f})" d="{d}"/>')
        cx += a + track
    return f'<g fill="{fill}">' + "".join(parts) + "</g>", width

def cap(font, size):
    return font["OS/2"].sCapHeight * size / font["head"].unitsPerEm

def mark(sc, x, y, size, stroke=8, dot_r=6):
    """Summit Arrow mark drawn in a 120-unit box placed at (x,y) with given size."""
    k = size / 120
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.5f})">'
            f'<path d="M14 96 L48 46 L62 64 L82 30 L106 96" fill="none" stroke="{sc["mark"]}" '
            f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="82" cy="{16 if dot_r <= 7 else 14}" r="{dot_r}" fill="{sc["dot"]}"/></g>')

# mark visual bounds inside its 120 box (stroke 8): x 10..110, y 10..100
MB = (10, 10, 110, 100)

def svg_doc(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}">{b}{body}</svg>')

TAG = "ELEVATE YOUR TECH"

def vertical(sc, tagline):
    pad, msize = 40, 200
    k = msize / 120
    W = 520
    cx = W / 2
    body = []
    mx = cx - 60 * k
    my = pad - MB[1] * k
    body.append(mark(sc, mx, my, msize))
    y = pad + (MB[3] - MB[1]) * k + 34
    c1 = cap(BOLD, 44); y += c1
    t, _ = text_run(BOLD, "HIMALAYAS", 44, 0.12, sc["name"], cx, y, "middle"); body.append(t)
    y += 18 + cap(MED, 17)
    t, _ = text_run(MED, "TECH SOLUTION", 17, 0.32, sc["sub"], cx, y, "middle"); body.append(t)
    if tagline:
        y += 26
        body.append(f'<rect x="{cx-24:.2f}" y="{y:.2f}" width="48" height="2" fill="{sc["tag"]}"/>')
        y += 22 + cap(MED, 14)
        t, _ = text_run(MED, TAG, 14, 0.30, sc["tag"], cx, y, "middle"); body.append(t)
    H = y + pad
    return svg_doc(W, H, "".join(body))

def horizontal(sc, tagline):
    pad, msize = 32, 120
    k = msize / 120
    mh = (MB[3] - MB[1]) * k
    c1, c2, c3 = cap(BOLD, 40), cap(MED, 15), cap(MED, 12)
    g12, g23 = 14, 16
    block = c1 + g12 + c2 + ((g23 + c3) if tagline else 0)
    H = max(mh, block + 20) + pad * 2
    mid = H / 2
    body = [mark(sc, pad - MB[0] * k, mid - mh / 2 - MB[1] * k, msize, stroke=9, dot_r=7)]
    x = pad + (MB[2] - MB[0]) * k + 26
    dh = block + 24
    body.append(f'<rect x="{x:.2f}" y="{mid-dh/2:.2f}" width="2.5" height="{dh:.2f}" fill="{sc["rule"]}"/>')
    x += 2.5 + 26
    y = mid - block / 2 + c1
    t, w1 = text_run(BOLD, "HIMALAYAS", 40, 0.10, sc["name"], x, y); body.append(t)
    y += g12 + c2
    t, w2 = text_run(MED, "TECH SOLUTION", 15, 0.36, sc["sub"], x, y); body.append(t)
    wmax = max(w1, w2)
    if tagline:
        y += g23 + c3
        t, w3 = text_run(MED, TAG, 12, 0.30, sc["tag"], x, y); body.append(t)
        wmax = max(wmax, w3)
    W = x + wmax + pad
    return svg_doc(W, H, "".join(body))

def mark_only(sc):
    S = 120
    return svg_doc(S, S, mark(sc, 0, 5, 120)) .replace(f'viewBox="0 0 {S} {S}"', 'viewBox="4 4 112 112"')

def app_icon(dark, rounded=True, msize=700, stroke=10, dot_r=8):
    S = 1024
    bg = NAVY if dark else WHITE
    sc = dict(SCHEMES["reversed"] if dark else SCHEMES["color"])
    shape = (f'<rect width="{S}" height="{S}" rx="{230 if rounded else 0}" fill="{bg}"/>')
    k = msize / 120
    m = mark(sc, S / 2 - 60 * k, S / 2 - 55 * k - 10, msize, stroke=stroke, dot_r=dot_r)
    return svg_doc(S, S, shape + m)

files = {}
for tag in (False, True):
    sfx = "-tagline" if tag else ""
    for name, sc in SCHEMES.items():
        files[f"vertical/HTS-vertical{sfx}-{name}.svg"] = (vertical(sc, tag), 2000)
        files[f"horizontal/HTS-horizontal{sfx}-{name}.svg"] = (horizontal(sc, tag), 3000)
for name, sc in SCHEMES.items():
    files[f"mark/HTS-mark-{name}.svg"] = (mark_only(sc), 1024)
files["app-icon/HTS-app-icon-light.svg"] = (app_icon(False), 1024)
files["app-icon/HTS-app-icon-dark.svg"] = (app_icon(True), 1024)
files["app-icon/HTS-app-icon-light-square.svg"] = (app_icon(False, False), 1024)
files["app-icon/HTS-app-icon-dark-square.svg"] = (app_icon(True, False), 1024)

for rel, (svg, _) in files.items():
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(svg)

# PNG export via headless Chromium (transparent backgrounds)
from playwright.sync_api import sync_playwright
import re
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    def render(svg, png, target_w):
        m = re.search(r'viewBox="([\d.\s-]+)"', svg)
        _, _, vw, vh = map(float, m.group(1).split())
        th = round(target_w * vh / vw)
        s2 = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{target_w}" height="{th}"', svg, count=1)
        if 'width="' not in s2.split(">")[0]:
            s2 = s2.replace("<svg ", f'<svg width="{target_w}" height="{th}" ', 1)
        pg.set_viewport_size({"width": target_w, "height": th})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{s2}</body></html>')
        pg.locator("svg").screenshot(path=png, omit_background=True)
    for rel, (svg, w) in files.items():
        render(svg, os.path.join(OUT, rel[:-4] + ".png"), w)
    # favicon sizes from light icon
    for s in (512, 180, 64, 32):
        light = app_icon(False, True, 860 if s <= 64 else 700, 15 if s <= 64 else 10, 10 if s <= 64 else 8)
        render(light, os.path.join(OUT, f"app-icon/HTS-favicon-{s}.png"), s)
    b.close()

open(os.path.join(OUT, "BRAND-COLORS.txt"), "w").write("""HIMALAYAS TECH SOLUTION — BRAND COLORS
Tagline: ELEVATE YOUR TECH

PRIMARY
  Summit Navy     HEX #0F2A44   RGB 15, 42, 68     CMYK 78, 38, 0, 73
  Glacier Teal    HEX #1F8F86   RGB 31, 143, 134   CMYK 78, 0, 6, 44

SUPPORTING
  Bright Teal     HEX #2BB3A8   RGB 43, 179, 168   CMYK 76, 0, 6, 30   (accent on dark backgrounds)
  Ridge Slate     HEX #4A5B6C   RGB 74, 91, 108    CMYK 31, 16, 0, 58  (secondary text)
  Mist            HEX #C9D3DD   RGB 201, 211, 221  CMYK 9, 5, 0, 13    (dividers, borders)
  Ice             HEX #F7F9FB   RGB 247, 249, 251  CMYK 2, 1, 0, 2     (light background)
  White           HEX #FFFFFF

CMYK values are approximate conversions; ask your printer for a proof.

TYPOGRAPHY
  Poppins Bold — wordmark, headlines (tracked +12%)
  Poppins Medium — "TECH SOLUTION", tagline, subheads (tracked +30%)
  Poppins Regular — body text
  Free from Google Fonts: fonts.google.com/specimen/Poppins

FILES
  vertical/    stacked logo (primary), with and without tagline
  horizontal/  side-by-side logo for headers, signatures, letterhead
  mark/        Summit Arrow symbol only
  app-icon/    app icons (rounded + square for stores) and favicons
  -color     use on white / light backgrounds
  -reversed  use on Summit Navy or dark photos
  -black / -white  one-color uses (stamps, engraving, single-ink print)
  SVG files are vector (text outlined, no font needed); PNG files are transparent.
""")

zp = OUT.rstrip("/") + ".zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, fs in os.walk(OUT):
        for f in sorted(fs):
            full = os.path.join(root, f)
            z.write(full, os.path.join("HimalayasTech-Logo", os.path.relpath(full, OUT)))
print(zp, len(files), "svgs")
