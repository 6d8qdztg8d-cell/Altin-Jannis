#!/usr/bin/env python3
"""Generate a 2-page A5 flyer as PDF."""
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas as rcanvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

BASE = '/Users/altinramadani/Desktop/Gärtner_Altin&Jannis/'
IMG  = BASE + 'images/'
OUT  = BASE + 'flyer-altin-jannis.pdf'

W, H = A5   # 419.53 × 595.28 pt
MX   = 22   # horizontal margin
CW   = W - 2*MX

# ── Colours ──────────────────────────────────────────────────
BG      = HexColor('#0b1e12')
PANEL   = HexColor('#0f2916')
CARD    = HexColor('#112c1a')
GREEN   = HexColor('#4caf77')
DKGREEN = HexColor('#1a5c35')
WHITE   = HexColor('#ffffff')
GREY    = HexColor('#8db09e')
LGREY   = HexColor('#c5d9cf')
RING    = HexColor('#3a9e66')


# ── Helpers ───────────────────────────────────────────────────
def fill_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def top_accent(c):
    c.setFillColor(GREEN)
    c.rect(0, H - 4, W, 4, fill=1, stroke=0)

def divider(c, y, x0=None, x1=None, color=GREEN, lw=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x0 or MX, y, x1 or (W - MX), y)

def ctext(c, y, text, font='Helvetica', size=9, color=WHITE):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(W / 2, y, text)

def ltext(c, x, y, text, font='Helvetica', size=9, color=WHITE):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)

def panel_rect(c, x, y, w, h, r=8, color=PANEL):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)

def clip_circle(c, path, cx, cy, r):
    """Draw image clipped to circle, top-aligned to show face."""
    c.saveState()
    p = c.beginPath()
    p.circle(cx, cy, r)
    c.clipPath(p, stroke=0, fill=0)
    reader = ImageReader(path)
    iw, ih = reader.getSize()
    scale  = (2 * r) / iw
    sw, sh = 2 * r, ih * scale
    # Anchor image top to circle top so we see the head/face
    iy = cy + r - sh
    c.drawImage(path, cx - r, iy, width=sw, height=sh, mask='auto')
    c.restoreState()

def photo_circle(c, path, cx, cy, r):
    """Ring + clipped portrait."""
    # Outer glow ring
    c.setFillColor(HexColor('#183d27'))
    c.setStrokeColor(HexColor('#183d27'))
    c.setLineWidth(0)
    c.circle(cx, cy, r + 6, fill=1, stroke=0)
    # Green border
    c.setFillColor(BG)
    c.setStrokeColor(RING)
    c.setLineWidth(2.5)
    c.circle(cx, cy, r + 3, fill=1, stroke=1)
    # Photo
    clip_circle(c, path, cx, cy, r)


# ══════════════════════════════════════════════════════════════
# PAGE 1 — VORSTELLUNG
# ══════════════════════════════════════════════════════════════
c = rcanvas.Canvas(OUT, pagesize=A5)
fill_bg(c)
top_accent(c)

# Soft decorative glow top-right
c.setFillColor(HexColor('#0e2a18'))
c.circle(W + 10, H + 10, 120, fill=1, stroke=0)
c.setFillColor(HexColor('#0c2314'))
c.circle(W, H, 70, fill=1, stroke=0)

# ── Header ────────────────────────────────────────────────────
ctext(c, H - 22,  'G A R T E N A R B E I T E N   ·   K A N T O N   Z U G',
      size=7, color=GREEN)
ctext(c, H - 52,  'Altin  &  Jannis', font='Helvetica-Bold', size=28)
ctext(c, H - 68,  'Studentisch geführt  &  professionell', size=8.5, color=GREY)
divider(c, H - 80)

# ── Portraits ─────────────────────────────────────────────────
r    = 83
lcx  = W / 2 - 88     # Jannis
rcx  = W / 2 + 88     # Altin
pcy  = H - 80 - 14 - r  # = H - 177

photo_circle(c, IMG + 'face-jannis.jpg', lcx, pcy, r)
photo_circle(c, IMG + 'face-altin.jpg',  rcx, pcy, r)

# Names
ny = pcy - r - 15
ctext(c, ny,      'Jannis',            font='Helvetica-Bold', size=13,
      color=WHITE)  # placeholder – draw individually below
c.setFillColor(WHITE)
c.setFont('Helvetica-Bold', 13)
c.drawCentredString(lcx, ny, 'Jannis')
c.drawCentredString(rcx, ny, 'Altin')

# Age / club
dy = ny - 14
c.setFillColor(GREEN)
c.setFont('Helvetica', 8)
c.drawCentredString(lcx, dy, '19 Jahre  ·  SC Cham')
c.drawCentredString(rcx, dy, '20 Jahre  ·  Zug 94')

# Hobbies
hy = dy - 13
c.setFillColor(GREY)
c.setFont('Helvetica', 7.5)
c.drawCentredString(lcx, hy, 'Fussball  ·  Natur  ·  Freiluft')
c.drawCentredString(rcx, hy, 'Fussball  ·  Fahrrad  ·  Gym')

# ── Intro text panel ──────────────────────────────────────────
px = MX
pt = hy - 16       # panel top
ph = 90            # panel height
py = pt - ph       # panel bottom y

panel_rect(c, px, py, CW, ph, r=8, color=PANEL)
# Left green stripe
c.setFillColor(GREEN)
c.rect(px, py, 3, ph, fill=1, stroke=0)

intro = [
    'Wir sind zwei Studenten aus dem Kanton Zug, die mit',
    'echter Leidenschaft Gartenarbeiten übernehmen.',
    'Kein Grossbetrieb, keine anonymen Teams – nur wir',
    'zwei, persönlich und mit vollem Einsatz für Ihren Garten.',
    '',
    'Sauber, zuverlässig, pünktlich – immer mit Herz.',
]
ty = pt - 14
c.setFillColor(LGREY)
c.setFont('Helvetica', 8)
for line in intro:
    c.drawString(px + 12, ty, line)
    ty -= 13

# ── Quote band ────────────────────────────────────────────────
qy = py - 10
qh = 38
panel_rect(c, MX, qy - qh, CW, qh, r=8, color=DKGREEN)
c.setFillColor(GREEN)
c.rect(MX, qy - qh, 3, qh, fill=1, stroke=0)
c.setFillColor(WHITE)
c.setFont('Helvetica-Oblique', 10)
c.drawCentredString(W / 2, qy - 15, '« Ihr Garten. Unsere Leidenschaft. »')
c.setFillColor(GREY)
c.setFont('Helvetica', 7)
c.drawCentredString(W / 2, qy - 28, 'Altin Ramadani  &  Jannis')

# ── Bottom contact strip ──────────────────────────────────────
sh = 56
c.setFillColor(DKGREEN)
c.rect(0, 0, W, sh, fill=1, stroke=0)
c.setFillColor(GREEN)
c.rect(0, sh - 2, W, 2, fill=1, stroke=0)

# Left: phones
ltext(c, MX,          sh - 14, 'TELEFON', font='Helvetica-Bold', size=6.5, color=GREEN)
ltext(c, MX,          sh - 26, 'Altin: +41 76 611 81 50', size=8, color=WHITE)
ltext(c, MX,          sh - 38, 'Jannis: +41 78 978 77 75', size=8, color=WHITE)

# Right: email + location
rx = W / 2 + 12
ltext(c, rx, sh - 14, 'E-MAIL', font='Helvetica-Bold', size=6.5, color=GREEN)
ltext(c, rx, sh - 26, 'tiniolti2006@gmail.com', size=8, color=WHITE)
ltext(c, rx, sh - 38, 'Kanton Zug, Schweiz', size=8, color=GREY)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — LEISTUNGEN & KONTAKT
# ══════════════════════════════════════════════════════════════
c.showPage()
fill_bg(c)
top_accent(c)

# Decorative glow top-left
c.setFillColor(HexColor('#0e2a18'))
c.circle(-10, H + 10, 100, fill=1, stroke=0)

# ── Header ────────────────────────────────────────────────────
ctext(c, H - 22, 'W A S   W I R   A N B I E T E N', size=7, color=GREEN)
ctext(c, H - 48, 'Unsere Leistungen', font='Helvetica-Bold', size=22)
ctext(c, H - 63, 'Von Rasenpflege bis Handwerk – flexibel & zuverlässig.',
      size=8, color=GREY)
divider(c, H - 75)

# ── Services grid (2 columns) ─────────────────────────────────
services = [
    ('grass',          'Rasen mähen',           'Präziser Schnitt, wöchentlich oder nach Bedarf'),
    ('content_cut',    'Hecken schneiden',       'Saubere Konturen, gesunde Pflanzen'),
    ('yard',           'Unkraut entfernen',      'Vollständig inkl. Wurzel – dauerhaft sauber'),
    ('eco',            'Gartenpflege allg.',     'Schneiden, pflegen, düngen – aus einer Hand'),
    ('grid_view',      'Platten verlegen',       'Wege & Terrassen mit fachgerechtem Unterbau'),
    ('cleaning_services', 'Aufräumarbeiten',     'Laub, Schnittgut, Abfall – ordentlich entsorgt'),
    ('construction',   'Handwerkliche Arb.',     'Kleinere Außenarbeiten – nach Absprache'),
]

col_w  = CW / 2 - 5
row_h  = 44
sy     = H - 75 - 10  # top of first service row

for i, (_, title, desc) in enumerate(services):
    col = i % 2
    row = i // 2
    cx  = MX + col * (col_w + 10)
    ry  = sy - row * row_h

    panel_rect(c, cx, ry - row_h + 6, col_w, row_h - 6, r=7, color=CARD)

    # Green dot accent
    c.setFillColor(GREEN)
    c.circle(cx + 8, ry - 9, 3, fill=1, stroke=0)

    # Title
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawString(cx + 17, ry - 12, title)

    # Desc
    c.setFillColor(GREY)
    c.setFont('Helvetica', 7)
    c.drawString(cx + 17, ry - 23, desc)

# ── Divider + Why us ─────────────────────────────────────────
n_rows  = (len(services) + 1) // 2   # = 4 rows
why_top = sy - n_rows * row_h - 8

divider(c, why_top)

ctext(c, why_top - 14, 'W A R U M   A L T I N   &   J A N N I S ?',
      size=7, color=GREEN)
ctext(c, why_top - 32, 'Drei gute Gründe', font='Helvetica-Bold', size=14)

reasons = [
    ('Persönlich',    'Direkt mit uns –\nkein Call-Center.'),
    ('Zuverlässig',   'Pünktlich & sauber.\nAbmachungen gelten.'),
    ('Faire Preise',  'Transparent und\nerschwinglich.'),
]

rcard_w = CW / 3 - 6
rcard_h = 58
rcards_y = why_top - 32 - 14  # top of reason cards

for i, (rtitle, rdesc) in enumerate(reasons):
    rx = MX + i * (rcard_w + 9)
    panel_rect(c, rx, rcards_y - rcard_h, rcard_w, rcard_h, r=8, color=CARD)
    # Green top bar
    c.setFillColor(GREEN)
    c.roundRect(rx, rcards_y - 4, rcard_w, 4, 2, fill=1, stroke=0)
    # Title
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawCentredString(rx + rcard_w / 2, rcards_y - 17, rtitle)
    # Desc lines
    c.setFillColor(GREY)
    c.setFont('Helvetica', 7)
    for j, line in enumerate(rdesc.split('\n')):
        c.drawCentredString(rx + rcard_w / 2, rcards_y - 29 - j * 11, line)

# ── CTA block ────────────────────────────────────────────────
cta_y  = rcards_y - rcard_h - 12
cta_h  = 44

panel_rect(c, MX, cta_y - cta_h, CW, cta_h, r=8, color=DKGREEN)
c.setFillColor(GREEN)
c.rect(MX, cta_y - cta_h, 3, cta_h, fill=1, stroke=0)

c.setFillColor(WHITE)
c.setFont('Helvetica-Bold', 11)
c.drawCentredString(W / 2, cta_y - 18, 'Jetzt Anfrage stellen →')
c.setFillColor(GREY)
c.setFont('Helvetica', 8)
c.drawCentredString(W / 2, cta_y - 32, 'Schnell, unkompliziert & kostenlos  ·  Kanton Zug')

# ── Bottom contact strip ──────────────────────────────────────
c.setFillColor(DKGREEN)
c.rect(0, 0, W, sh, fill=1, stroke=0)
c.setFillColor(GREEN)
c.rect(0, sh - 2, W, 2, fill=1, stroke=0)

ltext(c, MX,          sh - 14, 'TELEFON', font='Helvetica-Bold', size=6.5, color=GREEN)
ltext(c, MX,          sh - 26, 'Altin: +41 76 611 81 50',   size=8, color=WHITE)
ltext(c, MX,          sh - 38, 'Jannis: +41 78 978 77 75',  size=8, color=WHITE)

rx = W / 2 + 12
ltext(c, rx, sh - 14, 'E-MAIL', font='Helvetica-Bold', size=6.5, color=GREEN)
ltext(c, rx, sh - 26, 'tiniolti2006@gmail.com',         size=8, color=WHITE)
ltext(c, rx, sh - 38, 'Kanton Zug, Schweiz',            size=8, color=GREY)

# ── Save ─────────────────────────────────────────────────────
c.save()
print('Flyer gespeichert:', OUT)
