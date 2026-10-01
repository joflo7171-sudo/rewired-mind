"""Builds store images from cropped demo screenshots. Usage: python build_launch_images.py <shots_dir> <out_dir>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SH, OUT = sys.argv[1].rstrip("/") + "/", sys.argv[2].rstrip("/") + "/"
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"; R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
PRI = (15, 76, 92); ACC = (43, 179, 163); MINT = (216, 240, 236); WHITE = (255, 255, 255); MUTED = (107, 123, 131); BG = (243, 247, 248)
F = lambda p, s: ImageFont.truetype(p, s)


def wordmark(d, x, y, size, on_dark=True):
    """OperatorGrid wordmark: 3x3 grid icon + 'Operator' + 'Grid'. Returns width."""
    cell = max(3, size // 4); gap = max(1, size // 12)
    for r in range(3):
        for c in range(3):
            col = ACC if (r + c) % 2 == 0 else (MINT if on_dark else PRI)
            d.rectangle((x + c * (cell + gap), y + r * (cell + gap) + (size - 3 * cell - 2 * gap) // 2,
                         x + c * (cell + gap) + cell, y + r * (cell + gap) + cell + (size - 3 * cell - 2 * gap) // 2), fill=col)
    tx = x + 3 * cell + 2 * gap + size // 3
    f = F(B, size)
    d.text((tx, y - size // 10), "Operator", font=f, fill=WHITE if on_dark else PRI)
    w1 = d.textlength("Operator", font=f)
    d.text((tx + w1, y - size // 10), "Grid", font=f, fill=ACC)
    return tx + w1 + d.textlength("Grid", font=f) - x


def wordmark_width(size):
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    cell = max(3, size // 4); gap = max(1, size // 12)
    f = F(B, size)
    return 3 * cell + 2 * gap + size // 3 + tmp.textlength("OperatorGrid", font=f)


def card(im, w):
    r = w / im.width; im = im.resize((round(w), round(im.height * r)), Image.LANCZOS)
    c = Image.new("RGB", (im.width + 20, im.height + 20), WHITE); c.paste(im, (10, 10)); return c


def shadow_paste(bg, im, xy):
    sh = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.rectangle((20, 24, im.width + 20, im.height + 24), fill=(0, 0, 0, 80)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    bg.paste(sh, (xy[0] - 20, xy[1] - 20), sh); bg.paste(im, xy)


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]


dash = Image.open(SH + "dashboard.png").convert("RGB"); quote = Image.open(SH + "quote-builder.png").convert("RGB")

# Cover 1280x720
cv = Image.new("RGB", (1280, 720), PRI); d = ImageDraw.Draw(cv)
d.rectangle((0, 700, 1280, 720), fill=ACC)
wordmark(d, 60, 48, 24)
d.text((60, 108), "CLEANING BUSINESS", font=F(B, 24), fill=MINT); d.text((60, 140), "AI Growth OS", font=F(B, 70), fill=WHITE)
y = 238
for ln in wrap(d, "Run your cleaning business from lead to payment in one connected system.", F(R, 27), 520):
    d.text((60, y), ln, font=F(R, 27), fill=MINT); y += 36
y += 22
for b in ["Quote + profit engine", "CRM, jobs & recurring schedule", "Profit by service & cleaner", "18 AI workflows + forms + marketing kit"]:
    d.ellipse((62, y + 9, 76, y + 23), fill=ACC); d.text((92, y), b, font=F(B, 23), fill=WHITE); y += 42
d.text((60, 648), "Excel + Google Sheets  ·  One-time purchase", font=F(R, 20), fill=MINT)
shadow_paste(cv, card(quote, 560), (690, 310)); shadow_paste(cv, card(dash, 590), (650, 60))
cv.save(OUT + "01-cover-1280x720.png")

# Thumbnail 600x600
th = Image.new("RGB", (600, 600), PRI); d = ImageDraw.Draw(th)
wordmark(d, 40, 30, 18)
d.text((40, 70), "CLEANING BUSINESS", font=F(B, 22), fill=MINT); d.text((40, 98), "AI Growth OS", font=F(B, 54), fill=WHITE)
d.text((40, 166), "Lead → quote → job → payment → profit", font=F(R, 21), fill=MINT)
shadow_paste(th, card(dash, 520), (40, 222)); d = ImageDraw.Draw(th); d.rectangle((0, 585, 600, 600), fill=ACC)
th.save(OUT + "02-thumbnail-600x600.png")

# Gallery 1600x1000: header 0-198, card zone 228-900, footer 930-1000
gal = [("dashboard", "See your whole business on one screen", "Money, pipeline, operations, reputation, and an Action Center that tells you what needs attention today."),
       ("quote-builder", "Know your profit before you send the quote", "Price, labor, supplies, travel, fees, gross margin, break-even and the price needed for your target margin."),
       ("profitability", "Find out which services really make money", "Profit by service, cleaner and customer type. Jobs below your target margin are flagged automatically."),
       ("schedule", "Your week, built automatically", "Every job from your jobs log, in start-time order, with daily hours and revenue."),
       ("leads-crm", "A sales pipeline that follows up for you", "Overdue follow-ups turn red. Booked leads remind you to add the customer."),
       ("monthly", "Twelve months of numbers that matter", "Revenue, labor, gross profit, overhead, estimated operating profit, leads, reviews and more.")]
ZONE_TOP, ZONE_BOTTOM, MAXW = 228, 900, 1480
for i, (n, h, sub) in enumerate(gal, start=3):
    g = Image.new("RGB", (1600, 1000), BG); d = ImageDraw.Draw(g)
    d.rectangle((0, 0, 1600, 190), fill=PRI); d.rectangle((0, 190, 1600, 198), fill=ACC)
    d.text((60, 42), h, font=F(B, 50), fill=WHITE); d.text((60, 114), sub, font=F(R, 25), fill=MINT)
    im = Image.open(SH + n + ".png").convert("RGB")
    maxh = ZONE_BOTTOM - ZONE_TOP - 20
    r = min((MAXW - 20) / im.width, maxh / im.height)
    c = card(im, im.width * r)
    shadow_paste(g, c, ((1600 - c.width) // 2, ZONE_TOP + (ZONE_BOTTOM - ZONE_TOP - c.height) // 2))
    d = ImageDraw.Draw(g)
    d.line((60, 930, 1540, 930), fill=(214, 224, 228), width=2)
    d.text((60, 950), "Fictional demo data shown.", font=F(R, 18), fill=MUTED)
    wm = wordmark_width(22); wordmark(d, int(1540 - wm), 948, 22, on_dark=False)
    g.save(OUT + f"{i:02d}-{n}.png")
print("images built")
