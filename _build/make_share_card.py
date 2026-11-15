"""Creates assets/images/share-card.jpg - the 1200x630 picture shown when a POI link is shared.

Run:  python _build/make_share_card.py      (needs Pillow:  pip install pillow)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SITE = Path(__file__).resolve().parent.parent
IMG = SITE / "assets" / "images"
FONT = SITE / "assets" / "fonts" / "Sora-Variable.ttf"

W, H = 1200, 630
NAVY = (10, 15, 46)
CREAM = (244, 241, 225)
SOFT = (195, 201, 228)
YELLOW = (242, 197, 15)
CYAN = (34, 195, 230)
BRAND = (14, 42, 114)


def font(size, weight):
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


card = Image.new("RGB", (W, H), NAVY)

# illustration on the right, fading into the navy
art = Image.open(IMG / "background_chamber.jpg").convert("RGB")
scale = H / art.height
art = art.resize((round(art.width * scale), H), Image.LANCZOS)
panel_w = 470
art = art.crop((art.width - panel_w - 40, 0, art.width - 40, H))
fade = Image.new("L", (panel_w, H), 255)
fd = ImageDraw.Draw(fade)
for x in range(200):
    fd.line([(x, 0), (x, H)], fill=round(255 * (x / 200) ** 1.6))
card.paste(art, (W - panel_w, 0), fade)

d = ImageDraw.Draw(card)

# logo mark + name
logo = Image.open(IMG / "logo_no_words.jpg").convert("RGB").resize((76, 76), Image.LANCZOS)
mask = Image.new("L", (76, 76), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, 75, 75], radius=20, fill=255)
d.rounded_rectangle([60, 56, 60 + 83, 56 + 83], radius=24, fill=YELLOW)
card.paste(logo, (64, 60), mask)
d.text((166, 64), "POI", font=font(40, 800), fill=CREAM)
d.text((168, 112), "POWER OF INTEREST", font=font(17, 600), fill=SOFT)

# headline with a yellow highlighter swipe under "WORDS."
big = font(90, 800)
x0, y1, y2 = 60, 222, 320
w_your = d.textlength("YOUR ", font=big)
w_words = d.textlength("WORDS.", font=big)
swipe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(swipe).rounded_rectangle([x0 + w_your - 6, y1 + 64, x0 + w_your + w_words + 6, y1 + 97], radius=8, fill=(242, 197, 15, 150))
card.paste(swipe, (0, 0), swipe)
d = ImageDraw.Draw(card)
d.text((x0, y1), "YOUR WORDS.", font=big, fill=CREAM)
d.text((x0, y2), "YOUR WAY.", font=big, fill=CREAM)

# supporting line + address
d.text((x0, 462), "Free debate workshops for students —", font=font(28, 500), fill=SOFT)
d.text((x0, 500), "online worldwide & in person in Oxford", font=font(28, 500), fill=SOFT)
d.text((x0, 556), "poi.org.uk", font=font(26, 700), fill=YELLOW)

# tri-colour stripe (matches the site footer)
d.rectangle([0, H - 10, W // 3, H], fill=YELLOW)
d.rectangle([W // 3, H - 10, 2 * W // 3, H], fill=CYAN)
d.rectangle([2 * W // 3, H - 10, W, H], fill=BRAND)

out = IMG / "share-card.jpg"
card.save(out, quality=88, optimize=True, progressive=True)
print("wrote", out)
