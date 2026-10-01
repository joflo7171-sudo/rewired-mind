"""Small reportlab renderer for the product guides. Blocks: (kind, payload)."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, ListFlowable, ListItem, Preformatted, NextPageTemplate)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DVM", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

PRIMARY = colors.HexColor("#0F4C5C")
ACCENT = colors.HexColor("#2BB3A3")
MUTED = colors.HexColor("#6B7B83")
LIGHT = colors.HexColor("#F3F7F8")
AMBERBG = colors.HexColor("#FDF1DC")
TEXT = colors.HexColor("#1E2A30")

S = {
    "body": ParagraphStyle("body", fontName="DV", fontSize=9.6, leading=14, textColor=TEXT, spaceAfter=6),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=19, leading=24, textColor=PRIMARY, spaceBefore=4, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=13, leading=17, textColor=PRIMARY, spaceBefore=12, spaceAfter=5, keepWithNext=1),
    "h3": ParagraphStyle("h3", fontName="DVB", fontSize=10.5, leading=14, textColor=ACCENT, spaceBefore=8, spaceAfter=3, keepWithNext=1),
    "small": ParagraphStyle("small", fontName="DV", fontSize=8, leading=11, textColor=MUTED),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.4, leading=11, textColor=TEXT),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=8.4, leading=11, textColor=colors.white),
    "mono": ParagraphStyle("mono", fontName="DVM", fontSize=8.2, leading=11.2, textColor=TEXT),
    "note": ParagraphStyle("note", fontName="DV", fontSize=9, leading=13, textColor=TEXT),
    "cover_t": ParagraphStyle("ct", fontName="DVB", fontSize=30, leading=36, textColor=colors.white),
    "cover_s": ParagraphStyle("cs", fontName="DV", fontSize=13, leading=18, textColor=colors.HexColor("#D8F0EC")),
}


def P(t, st="body"):
    return Paragraph(t, S[st])


def render(path, title, subtitle, blocks, product="Cleaning Business AI Growth OS", brand="OperatorGrid"):
    def cover(c, doc):
        c.saveState()
        c.setFillColor(PRIMARY); c.rect(0, 0, LETTER[0], LETTER[1], stroke=0, fill=1)
        c.setFillColor(ACCENT); c.rect(0, LETTER[1] * 0.38, LETTER[0], 6, stroke=0, fill=1)
        c.setFont("DV", 9); c.setFillColor(colors.HexColor("#D8F0EC"))
        c.drawString(0.8 * inch, 0.7 * inch, f"© {brand}  ·  {product}  ·  Template content — customize before use")
        c.restoreState()

    def page(c, doc):
        c.saveState()
        c.setStrokeColor(ACCENT); c.setLineWidth(2); c.line(0.75 * inch, LETTER[1] - 0.55 * inch, LETTER[0] - 0.75 * inch, LETTER[1] - 0.55 * inch)
        c.setFont("DVB", 8); c.setFillColor(PRIMARY)
        c.drawString(0.75 * inch, LETTER[1] - 0.45 * inch, brand.upper() + "  ·  " + product.upper())
        c.setFont("DV", 8); c.setFillColor(MUTED)
        c.drawRightString(LETTER[0] - 0.75 * inch, LETTER[1] - 0.45 * inch, title)
        c.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
        c.drawString(0.75 * inch, 0.5 * inch, "Estimates and templates only — not legal, tax, accounting, insurance or safety advice.")
        c.restoreState()

    doc = BaseDocTemplate(path, pagesize=LETTER, title=title, author=brand, creator=brand, subject=subtitle,
                          leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.8 * inch, bottomMargin=0.8 * inch)
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    cfr = Frame(0.8 * inch, LETTER[1] * 0.42, LETTER[0] - 1.6 * inch, LETTER[1] * 0.45, id="c")
    doc.addPageTemplates([PageTemplate("cover", [cfr], onPage=cover), PageTemplate("page", [fr], onPage=page)])
    story = [Spacer(1, 40), P(brand.upper(), "cover_s"), Spacer(1, 4), P(product.upper(), "cover_s"), Spacer(1, 10), P(title, "cover_t"), Spacer(1, 14), P(subtitle, "cover_s"),
             NextPageTemplate("page"), PageBreak()]
    for kind, val in blocks:
        if kind in ("h1", "h2", "h3", "small"):
            story.append(P(val, kind))
        elif kind == "p":
            story.append(P(val))
        elif kind == "bul":
            story.append(ListFlowable([ListItem(P(x), leftIndent=12, value="•") for x in val], bulletType="bullet",
                                      start="•", leftIndent=12, bulletFontName="DV", bulletColor=ACCENT))
            story.append(Spacer(1, 4))
        elif kind == "num":
            story.append(ListFlowable([ListItem(P(x), leftIndent=16) for x in val], bulletType="1", leftIndent=16,
                                      bulletFontName="DVB", bulletColor=PRIMARY, bulletFontSize=9))
            story.append(Spacer(1, 4))
        elif kind == "table":
            rows, widths = val if isinstance(val, tuple) else (val, None)
            data = [[P(str(c), "cellb") for c in rows[0]]] + [[P(str(c), "cell") for c in r] for r in rows[1:]]
            tw = doc.width
            cw = [tw * w for w in widths] if widths else None
            t = Table(data, colWidths=cw, repeatRows=1)
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                                   ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DEE2")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
            story.append(t); story.append(Spacer(1, 8))
        elif kind == "note":
            t = Table([[P(val, "note")]], colWidths=[doc.width])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AMBERBG), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#E08E2B"))]))
            story.append(t); story.append(Spacer(1, 8))
        elif kind == "tip":
            t = Table([[P(val, "note")]], colWidths=[doc.width])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E2F4EA")), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT)]))
            story.append(t); story.append(Spacer(1, 8))
        elif kind == "prompt":
            pre = Preformatted(val, S["mono"], maxLineLength=96)
            t = Table([[pre]], colWidths=[doc.width])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.6, ACCENT),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
            story.append(t); story.append(Spacer(1, 8))
        elif kind == "keep":
            story.append(KeepTogether([P(v[1], v[0]) for v in val]))
        elif kind == "space":
            story.append(Spacer(1, val))
        elif kind == "break":
            story.append(PageBreak())
    doc.build(story)
