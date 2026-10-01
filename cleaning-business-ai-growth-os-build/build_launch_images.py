"""Builds store images from cropped demo screenshots in SHOTS dir. Usage: python build_launch_images.py <shots_dir> <out_dir>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SH, OUT = sys.argv[1].rstrip("/") + "/", sys.argv[2].rstrip("/") + "/"
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"; R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
PRI = (15, 76, 92); ACC = (43, 179, 163); MINT = (216, 240, 236); WHITE = (255, 255, 255)
F = lambda p, s: ImageFont.truetype(p, s)


def card(im, w):
    r = w / im.width; im = im.resize((w, int(im.height * r)), Image.LANCZOS)
    c = Image.new("RGB", (im.width + 20, im.height + 20), WHITE); c.paste(im, (10, 10)); return c


def shadow_paste(bg, im, xy):
    sh = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.rectangle((20, 24, im.width + 20, im.height + 24), fill=(0, 0, 0, 90)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    bg.paste(sh, (xy[0] - 20, xy[1] - 20), sh); bg.paste(im, xy)


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]


dash = Image.open(SH + "dashboard.png").convert("RGB"); quote = Image.open(SH + "quote-builder.png").convert("RGB")
cv = Image.new("RGB", (1280, 720), PRI); d = ImageDraw.Draw(cv)
d.rectangle((0, 700, 1280, 720), fill=ACC)
d.text((60, 70), "CLEANING BUSINESS", font=F(B, 26), fill=MINT); d.text((60, 105), "AI Growth OS", font=F(B, 72), fill=WHITE)
y = 205
for ln in wrap(d, "Run your cleaning business from lead to payment in one connected system.", F(R, 28), 520):
    d.text((60, y), ln, font=F(R, 28), fill=MINT); y += 38
y += 25
for b in ["Quote + profit engine", "CRM, jobs & recurring schedule", "Profit by service & cleaner", "18 AI workflows + forms + marketing kit"]:
    d.ellipse((62, y + 9, 76, y + 23), fill=ACC); d.text((92, y), b, font=F(B, 24), fill=WHITE); y += 44
d.text((60, 640), "Excel + Google Sheets  ·  One-time purchase", font=F(R, 20), fill=MINT)
shadow_paste(cv, card(quote, 560), (690, 300)); shadow_paste(cv, card(dash, 600), (640, 60))
cv.save(OUT + "01-cover-1280x720.png")
th = Image.new("RGB", (600, 600), PRI); d = ImageDraw.Draw(th)
d.text((40, 40), "CLEANING BUSINESS", font=F(B, 24), fill=MINT); d.text((40, 72), "AI Growth OS", font=F(B, 56), fill=WHITE)
d.text((40, 145), "Lead → quote → job → payment → profit", font=F(R, 22), fill=MINT)
shadow_paste(th, card(dash, 520), (40, 205)); d = ImageDraw.Draw(th); d.rectangle((0, 585, 600, 600), fill=ACC)
th.save(OUT + "02-thumbnail-600x600.png")
gal = [("dashboard", "See your whole business on one screen", "Money, pipeline, operations, reputation, and an Action Center that tells you what needs attention today."),
       ("quote-builder", "Know your profit before you send the quote", "Price, labor, supplies, travel, fees, gross margin, break-even and the price needed for your target margin."),
       ("profitability", "Find out which services really make money", "Profit by service, cleaner and customer type. Jobs below your target margin are flagged automatically."),
       ("schedule", "Your week, built automatically", "Every job from your jobs log, sorted by start time, with daily hours and revenue."),
       ("leads-crm", "An 8-stage sales pipeline that follows up for you", "Overdue follow-ups turn red. Booked leads remind you to add the customer."),
       ("monthly", "Twelve months of numbers that matter", "Revenue, labor, gross profit, overhead, estimated operating profit, leads, reviews and more.")]
for i, (n, h, sub) in enumerate(gal, start=3):
    g = Image.new("RGB", (1600, 1000), (243, 247, 248)); d = ImageDraw.Draw(g)
    d.rectangle((0, 0, 1600, 190), fill=PRI); d.rectangle((0, 190, 1600, 198), fill=ACC)
    d.text((60, 40), h, font=F(B, 50), fill=WHITE); d.text((60, 112), sub, font=F(R, 26), fill=MINT)
    im = Image.open(SH + n + ".png").convert("RGB")
    r = min(1480 / im.width, 740 / im.height); im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    c = card(im, im.width); shadow_paste(g, c, ((1600 - c.width) // 2, 230 + (740 - c.height) // 2))
    ImageDraw.Draw(g).text((60, 968), "Fictional demo data shown.", font=F(R, 18), fill=(107, 123, 131))
    g.save(OUT + f"{i:02d}-{n}.png")
print("images built")
