"""Genera los iconos PWA (símbolo de infinitud de Arduino sobre fondo teal)."""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "icons")
os.makedirs(OUT, exist_ok=True)

TEAL = (0, 151, 157, 255)          # #00979D (verde Arduino)
WHITE = (255, 255, 255, 255)


def draw_infinity(d, cx, cy, R, sw):
    """Dos bucles circulares enlazados con + y -, como el logo de Arduino."""
    off = R * 0.95
    for x, sign in ((cx - off, "-"), (cx + off, "+")):
        bbox = [x - R, cy - R, x + R, cy + R]
        d.ellipse(bbox, outline=WHITE, width=sw)
        bar = R * 0.55
        if sign == "+":
            d.rounded_rectangle([x - bar, cy - sw / 2, x + bar, cy + sw / 2], radius=sw / 2, fill=WHITE)
            d.rounded_rectangle([x - sw / 2, cy - bar, x + sw / 2, cy + bar], radius=sw / 2, fill=WHITE)
        else:
            d.rounded_rectangle([x - bar, cy - sw / 2, x + bar, cy + sw / 2], radius=sw / 2, fill=WHITE)


def make_icon(size, maskable=False, rounded=True):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = 0 if maskable else size * 0.08
    bg_box = [pad, pad, size - pad, size - pad]
    radius = 0 if maskable else (size - 2 * pad) * 0.22
    d.rounded_rectangle(bg_box, radius=radius, fill=TEAL)
    # el icono maskable deja un 20% de margen seguro alrededor del motivo
    scale = 0.60 if maskable else 0.78
    R = size * scale / 2 * 0.42
    sw = max(2, int(R * 0.42))
    cy = size / 2
    total_w = size * scale
    cx = size / 2 - (R * 0.95 + R) + total_w / 2
    draw_infinity(d, cx, cy, R, sw)
    return img


for s in (192, 512):
    make_icon(s).save(os.path.join(OUT, f"icon-{s}.png"))
make_icon(512, maskable=True).save(os.path.join(OUT, "icon-maskable-512.png"))
make_icon(180).save(os.path.join(OUT, "apple-touch-icon.png"))
print("iconos generados en", os.path.abspath(OUT))
