"""Sets OperatorGrid metadata on buyer-facing Office files and PDFs and strips generator fingerprints.
Content parts (worksheets, formulas, document text, slides) are copied byte-for-byte.
Usage: python clean_meta.py <folder>   (processes every .xlsx/.docx/.pptx/.pdf below it, in place)"""
import sys, os, re, zipfile, posixpath, datetime as dt
from pypdf import PdfReader, PdfWriter

BRAND = "OperatorGrid"
STAMP = "2026-10-01T00:00:00Z"
DROP = re.compile(r"^(docProps/thumbnail\.\w+|ppt/printerSettings/.*|xl/printerSettings/.*|word/printerSettings/.*)$")
APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           f'<Company>{BRAND}</Company></Properties>')


def title_for(path):
    n = os.path.splitext(os.path.basename(path))[0]
    n = re.sub(r"^\d+-", "", n).replace("-", " ")
    return n.title() if not n.isupper() else n.title()


def core_xml(title):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{title}</dc:title><dc:creator>{BRAND}</dc:creator><cp:lastModifiedBy>{BRAND}</cp:lastModifiedBy>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{STAMP}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{STAMP}</dcterms:modified></cp:coreProperties>')


def clean_office(path):
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    names = {i.filename for i, _ in items}
    dropped = {n for n in names if DROP.match(n)}
    out = []
    for info, data in items:
        n = info.filename
        if n in dropped:
            continue
        if n == "docProps/core.xml":
            data = core_xml(title_for(path)).encode()
        elif n == "docProps/app.xml":
            data = APP_XML.encode()
        elif n.endswith(".rels") and dropped:
            base = posixpath.dirname(posixpath.dirname(n))
            txt = data.decode("utf-8")

            def keep(m):
                tgt = re.search(r'Target="([^"]+)"', m.group(0)).group(1)
                full = posixpath.normpath(tgt.lstrip("/") if tgt.startswith("/") else posixpath.join(base, tgt))
                return "" if full in dropped else m.group(0)
            data = re.sub(r"<Relationship [^>]*/>", keep, txt).encode("utf-8")
        elif n == "[Content_Types].xml" and dropped:
            txt = data.decode("utf-8")
            for d in dropped:
                txt = re.sub(r'<Override PartName="/' + re.escape(d) + r'"[^>]*/>', "", txt)
            data = txt.encode("utf-8")
        out.append((n, data))
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in out:
            zi = zipfile.ZipInfo(n, date_time=(2026, 10, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    os.replace(tmp, path)
    return sorted(dropped)


def clean_pdf(path):
    r = PdfReader(path)
    title = (r.metadata or {}).get("/Title") or title_for(path)
    subject = (r.metadata or {}).get("/Subject") or ""
    w = PdfWriter()
    for page in r.pages:
        w.add_page(page)
    meta = {"/Title": str(title), "/Author": BRAND, "/Creator": BRAND, "/Producer": BRAND}
    if subject:
        meta["/Subject"] = str(subject)
    w.add_metadata(meta)
    with open(path, "wb") as f:
        w.write(f)


if __name__ == "__main__":
    root = sys.argv[1]
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            ext = f.lower().rsplit(".", 1)[-1]
            if ext in ("xlsx", "docx", "pptx"):
                d = clean_office(p)
                print("office", f, "dropped:", d)
            elif ext == "pdf":
                clean_pdf(p)
                print("pdf", f)
