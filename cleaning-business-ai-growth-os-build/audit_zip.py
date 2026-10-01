"""Audits the buyer ZIP. Usage: python audit_zip.py <zip> [reference_zip_for_structure]"""
import sys, re, zipfile, io
from pypdf import PdfReader

ZIP = sys.argv[1]
REF = sys.argv[2] if len(sys.argv) > 2 else None
problems, notes = [], []

TERMS = re.compile(r"rewired|zavoniq|legacy\s*(&|&amp;|and)\s*liberation|badgeworks|claude|cowork(?!er)|anthropic|chatgpt|gemini|copilot|"
                   r"python-docx|python-pptx|openpyxl|steve canny|reportlab|libreoffice|pypdf|joflo|jonathan|gmail\.com|"
                   r"/home/|/tmp/|/root/|scratchpad|file:/|[a-z]:\\\\|market-research|qa-report|pricing-validation|graphify|"
                   r"session_|build_workbook|demo_data|\.py\b|operatorgrid@|support@getoperatorgrid", re.I)
OK_URL = re.compile(r"^https?://(schemas\.openxmlformats\.org|schemas\.microsoft\.com|purl\.org|www\.w3\.org)/|^www\.example\.com$")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL = re.compile(r"https?://[^\s\"'<>)]+|www\.[a-z0-9.-]+\.[a-z]{2,}", re.I)
PHONE = re.compile(r"\(?\b\d{3}\)?[ .-]?\d{3}[ .-]\d{4}\b")
BAD_PARTS = re.compile(r"(externalLink|connections\.xml|queryTable|vbaProject|activeX|embeddings/|oleObject|customUI|printerSettings|thumbnail)", re.I)

counts = {"office": 0, "pdf": 0, "txt": 0, "office_parts": 0, "pdf_pages": 0}


def scan_text(src, text, visible=True):
    for m in TERMS.finditer(text):
        problems.append(f"{src}: forbidden term '{m.group(0)}' (…{text[max(0, m.start()-40):m.end()+40]!r}…)")
    for e in EMAIL.findall(text):
        if not e.lower().endswith("@example.com"):
            problems.append(f"{src}: non-placeholder email {e}")
    for u in URL.findall(text):
        if not OK_URL.match(u):
            problems.append(f"{src}: unexpected URL {u}")
    if visible:
        for ph in PHONE.findall(text):
            digits = re.sub(r"\D", "", ph)
            if not digits.startswith("555"):
                problems.append(f"{src}: phone-like number not in fictional 555 range: {ph}")


z = zipfile.ZipFile(ZIP)
if z.comment:
    problems.append(f"zip comment present: {z.comment!r}")
names = [i.filename for i in z.infolist()]
for n in names:
    if re.search(r"(__MACOSX|\.DS_Store|Thumbs\.db|desktop\.ini|/~\$|\.tmp$|\.bak$|\.md$|\.py$)", n):
        problems.append(f"unwanted file in zip: {n}")
if REF:
    ref = {re.sub(r"^[^/]+/", "", n) for n in zipfile.ZipFile(REF).namelist()}
    new = {re.sub(r"^[^/]+/", "", n) for n in names}
    if ref != new:
        problems.append(f"structure differs from reference: added {sorted(new-ref)} removed {sorted(ref-new)}")
    else:
        notes.append(f"structure identical to reference ({len(new)} entries)")

for info in z.infolist():
    n = info.filename
    if n.endswith("/"):
        continue
    data = z.read(n)
    low = n.lower()
    if low.endswith((".xlsx", ".docx", ".pptx")):
        counts["office"] += 1
        oz = zipfile.ZipFile(io.BytesIO(data))
        for part in oz.namelist():
            counts["office_parts"] += 1
            if BAD_PARTS.search(part):
                problems.append(f"{n}: disallowed part {part}")
            raw = oz.read(part)
            if part.endswith((".xml", ".rels")):
                txt = raw.decode("utf-8", "replace")
                visible = bool(re.search(r"(sharedStrings|worksheets/sheet|word/(document|header|footer)|ppt/slides/slide)", part))
                scan_text(f"{n}::{part}", txt, visible)
                if part.endswith(".rels") and 'TargetMode="External"' in txt:
                    problems.append(f"{n}::{part}: external relationship {re.findall(r'Target=.[^ ]+ TargetMode=.External.', txt)}")
                if "attachedTemplate" in txt:
                    problems.append(f"{n}::{part}: attachedTemplate reference")
                if part.startswith("xl/worksheets/") and re.search(r"<f>[^<]*(\[\d+\]|\.xls|https?:|file:)", txt):
                    problems.append(f"{n}::{part}: formula references an external workbook/URL")
                if part == "docProps/core.xml":
                    cr = re.search(r"<dc:creator>([^<]*)", txt); lm = re.search(r"<cp:lastModifiedBy>([^<]*)", txt)
                    if not cr or cr.group(1) != "OperatorGrid" or not lm or lm.group(1) != "OperatorGrid":
                        problems.append(f"{n}: core.xml creator/lastModifiedBy not OperatorGrid")
                    if "<dc:description>" in txt and re.search(r"<dc:description>[^<]+", txt):
                        problems.append(f"{n}: core.xml description present")
                if part == "docProps/app.xml" and "<Application>" in txt:
                    problems.append(f"{n}: app.xml Application fingerprint")
                if part == "xl/workbook.xml":
                    for dn in re.findall(r"<definedName[^>]*>([^<]*)", txt):
                        if re.search(r"\[\d+\]|\.xls|https?:|file:", dn):
                            problems.append(f"{n}: external defined name {dn}")
            else:
                if re.search(rb"python|openpyxl|reportlab|libreoffice|claude", raw, re.I):
                    problems.append(f"{n}::{part}: binary part contains tool fingerprint")
    elif low.endswith(".pdf"):
        counts["pdf"] += 1
        r = PdfReader(io.BytesIO(data))
        md = r.metadata or {}
        for k in ("/Author", "/Creator", "/Producer"):
            if md.get(k) != "OperatorGrid":
                problems.append(f"{n}: PDF {k} = {md.get(k)!r}")
        for k, v in md.items():
            scan_text(f"{n}::meta{k}", str(v), False)
        root = r.trailer["/Root"]
        if "/Metadata" in root:
            problems.append(f"{n}: XMP metadata stream present")
        if "/Names" in root and ("/JavaScript" in root["/Names"] or "/EmbeddedFiles" in root["/Names"]):
            problems.append(f"{n}: JavaScript or embedded files")
        if "/OpenAction" in root:
            problems.append(f"{n}: OpenAction present")
        for i, page in enumerate(r.pages):
            counts["pdf_pages"] += 1
            scan_text(f"{n}::p{i+1}", page.extract_text() or "")
            for a in page.get("/Annots") or []:
                a = a.get_object(); act = a.get("/A")
                if act:
                    act = act.get_object()
                    if act.get("/S") in ("/URI", "/Launch", "/JavaScript", "/GoToR"):
                        problems.append(f"{n}::p{i+1}: link action {act.get('/S')} {act.get('/URI')}")
        if re.search(rb"ReportLab|LibreOffice|pypdf|python", data, re.I):
            problems.append(f"{n}: raw PDF bytes contain generator string")
    elif low.endswith(".txt"):
        counts["txt"] += 1
        scan_text(n, data.decode("utf-8"))
    else:
        problems.append(f"unexpected file type: {n}")

print("FILES:", counts)
for x in notes:
    print("NOTE:", x)
if problems:
    print(f"PROBLEMS ({len(problems)}):")
    for p in problems:
        print(" -", p)
else:
    print("RESULT: CLEAN — 0 problems")
