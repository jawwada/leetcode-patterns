"""Typeset the editable CX guide. Run with the bundled Python or ReportLab installed."""
from __future__ import annotations

import ast
import html
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Preformatted, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "dialogflow_cx_applied_ai_field_guide.pdf"
DEPS = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies"
FONT_DIR = DEPS / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
if not FONT_DIR.is_dir():
    FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
for name, filename in [
    ("Guide", "DejaVuSans.ttf"), ("Guide-Bold", "DejaVuSans-Bold.ttf"),
    ("Guide-Italic", "DejaVuSans-Oblique.ttf"),
    ("Guide-BoldItalic", "DejaVuSans-BoldOblique.ttf"),
    ("Code", "DejaVuSansMono.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily("Guide", normal="Guide", bold="Guide-Bold", italic="Guide-Italic", boldItalic="Guide-BoldItalic")

NAVY = colors.HexColor("#12243B")
TEAL = colors.HexColor("#007D83")
INK = colors.HexColor("#233248")
MUTED = colors.HexColor("#526477")
PALE = colors.HexColor("#EDF5F6")
LINE = colors.HexColor("#D5E1E6")
PAGE_W, PAGE_H = 612, 792
MARGIN = 54
WIDTH = PAGE_W - 2 * MARGIN
styles = getSampleStyleSheet()
styles.add(ParagraphStyle("BodyGuide", fontName="Guide", fontSize=10.3, leading=15.1,
                          textColor=INK, spaceAfter=8, allowWidows=0, allowOrphans=0))
styles.add(ParagraphStyle("ChapterGuide", fontName="Guide-Bold", fontSize=23, leading=29,
                          textColor=NAVY, spaceAfter=18, keepWithNext=True))
styles.add(ParagraphStyle("SectionGuide", fontName="Guide-Bold", fontSize=13.1, leading=18,
                          textColor=TEAL, spaceBefore=13, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle("SmallGuide", fontName="Guide", fontSize=8.7, leading=12.3,
                          textColor=MUTED, spaceAfter=7))
styles.add(ParagraphStyle("CellGuide", fontName="Guide", fontSize=8.6, leading=12.1,
                          textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle("CellHeader", parent=styles["CellGuide"], fontName="Guide-Bold", textColor=colors.white))
styles.add(ParagraphStyle("BulletGuide", parent=styles["BodyGuide"], leftIndent=14, firstLineIndent=-10))
styles.add(ParagraphStyle("CodeGuide", fontName="Code", fontSize=8, leading=11.1,
                          textColor=INK, backColor=PALE, borderPadding=9, spaceBefore=5, spaceAfter=10))
styles.add(ParagraphStyle("TOC0", fontName="Guide-Bold", fontSize=11.2, leading=16.5,
                          textColor=NAVY, spaceBefore=9, leftIndent=0, firstLineIndent=0))
styles.add(ParagraphStyle("TOC1", fontName="Guide", fontSize=9, leading=13.5,
                          textColor=INK, leftIndent=15, firstLineIndent=0, spaceBefore=3))
styles.add(ParagraphStyle("AnswerTitle", parent=styles["SectionGuide"], fontSize=15,
                          leading=19, spaceBefore=0, spaceAfter=12))
styles.add(ParagraphStyle("AnswerSection", parent=styles["SectionGuide"], fontSize=11.2,
                          leading=15, spaceBefore=7, spaceAfter=5))

def normalize(text: str) -> str:
    return text.replace("\u2014", " - ").replace("\u2013", "-").replace("\u2011", "-").replace("\u00a0", " ")

def inline(text: str) -> str:
    text = normalize(text)
    saved = []
    def hold(markup: str) -> str:
        saved.append(markup)
        return f"ZXQMARK{len(saved)-1}QXZ"
    text = re.sub(r"`([^`]+)`", lambda m: hold(f'<font name="Code" size="9">{escape(m[1])}</font>'), text)
    def link(m):
        url = html.escape(m[2], quote=True)
        label = escape(m[1])
        return hold(f'<link href="{url}" color="#007D83"><u>{label}</u></link>')
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", link, text)
    text = escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    for i, markup in enumerate(saved):
        text = text.replace(f"ZXQMARK{i}QXZ", markup)
    return text

class Diagram(Flowable):
    def __init__(self, kind: str):
        Flowable.__init__(self)
        self.kind = kind
        self.width = WIDTH
        self.height = 239 if kind in ("drive_arch", "noctal_arch", "market_arch", "foundation") else 189

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#F6F9FB"))
        c.roundRect(0, 0, WIDTH, self.height, 10, fill=1, stroke=0)
        nodes = {}
        def box(key, x, y, w, title, desc, h=48):
            nodes[key] = (x, y, w, h)
            c.setFillColor(colors.white)
            c.setStrokeColor(LINE)
            c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
            c.setFillColor(NAVY)
            c.setFont("Guide-Bold", 9.1)
            c.drawCentredString(x + w/2, y + h - 15, title)
            c.setFillColor(MUTED)
            c.setFont("Guide", 7.5)
            for i, line in enumerate(simpleSplit(desc, "Guide", 7.5, w-14)[:2]):
                c.drawCentredString(x + w/2, y + h - 28 - i*10, line)
        def arrow(a, b, vertical=False, label=""):
            ax, ay, aw, ah = nodes[a]
            bx, by, bw, bh = nodes[b]
            if vertical:
                if by > ay:
                    start, end = (ax+aw/2, ay+ah), (bx+bw/2, by)
                else:
                    start, end = (ax+aw/2, ay), (bx+bw/2, by+bh)
            else:
                start, end = (ax+aw, ay+ah/2), (bx, by+bh/2)
            c.setStrokeColor(TEAL)
            c.setFillColor(TEAL)
            c.setLineWidth(1.15)
            c.line(*start, *end)
            import math
            angle = math.atan2(end[1]-start[1], end[0]-start[0])
            p = c.beginPath(); p.moveTo(*end)
            p.lineTo(end[0]-6*math.cos(angle-.45), end[1]-6*math.sin(angle-.45))
            p.lineTo(end[0]-6*math.cos(angle+.45), end[1]-6*math.sin(angle+.45))
            p.close(); c.drawPath(p, fill=1, stroke=0)
            if label:
                c.setFont("Guide", 7)
                c.drawString((start[0]+end[0])/2+3, (start[1]+end[1])/2+4, label)
        if self.kind == "drive_arch":
            box("lane", 15, 166, 140, "Lane audio/channel", "Speech capture and playback")
            box("cx", 182, 166, 140, "Dialogflow CX", "Pages, forms, routes, prompts")
            box("api", 349, 166, 140, "FastAPI adapter", "Authenticated tag dispatch")
            box("menu", 15, 82, 140, "Menu/configuration", "Store, availability, revision")
            box("cart", 182, 82, 140, "Cart/order service", "Prices, proposals, operations")
            box("pos", 349, 82, 140, "POS integration", "Submit and reconcile order")
            arrow("lane", "cx"); arrow("cx", "api")
            arrow("api", "cart", True); arrow("menu", "cart"); arrow("cart", "pos")
            caption = "CX manages the dialogue; cart/POS services own order truth."
        elif self.kind == "noctal_arch":
            box("ui", 15, 166, 140, "Web / in-app client", "Chat, file controls, progress")
            box("bff", 182, 166, 140, "BFF + identity", "Login and session binding")
            box("cx", 349, 166, 140, "Dialogflow CX", "Conversational task/state")
            box("store", 15, 82, 140, "Media / job stores", "Assets, operations, results")
            box("jobs", 182, 82, 140, "Domain services", "Authorize, queue, workers")
            box("api", 349, 82, 140, "FastAPI fulfillment", "Validate and dispatch tags")
            arrow("ui", "bff"); arrow("bff", "cx"); arrow("cx", "api", True)
            # Right-to-left domain path, drawn without overlapping labels.
            c.setStrokeColor(TEAL); c.setLineWidth(1.15)
            for x1, x2 in [(349, 322), (182, 155)]:
                c.line(x1, 106, x2, 106)
                c.line(x2, 106, x2+5, 109); c.line(x2,106,x2+5,103)
            caption = "File bytes and progress use dedicated channel APIs; jobs outlive chat."
        elif self.kind == "foundation":
            box("ui", 15, 166, 140, "Chat / voice channel", "User interaction and transfer")
            box("cx", 182, 166, 140, "Dialogflow CX", "Conversational task/state")
            box("api", 349, 166, 140, "Webhook/tool gateway", "Authenticated integration")
            box("id", 15, 82, 140, "Identity / binding", "Verified principal and policy")
            box("domain", 182, 82, 140, "Business APIs", "Durable stores, queue, workers")
            box("rag", 349, 82, 140, "Retrieval service", "Authorized evidence and model")
            arrow("ui", "cx"); arrow("cx", "api")
            arrow("api", "id", True); arrow("api", "domain", True); arrow("api", "rag", True)
            caption = "Domain outcomes, handoff integration, and telemetry are application-owned."
        elif self.kind == "market_arch":
            box("ui", 15, 166, 140, "Authenticated client", "Selection and explicit review")
            box("cx", 182, 166, 140, "Dialogflow CX", "Discovery and approval flow")
            box("api", 349, 166, 140, "Domain adapter", "Validate proposal and action")
            box("feed", 15, 82, 140, "Market-data service", "Metadata, quotes, freshness")
            box("ops", 182, 82, 140, "Operation store", "Approval and reconciliation")
            box("exec", 349, 82, 140, "Provider execution", "Kalshi / Polymarket adapters")
            arrow("ui", "cx"); arrow("cx", "api")
            arrow("api", "feed", True); arrow("api", "ops", True); arrow("api", "exec", True)
            caption = "Provider identifiers, signing, constraints, and lifecycle stay explicit."
        elif self.kind == "drive_states":
            box("a", 15, 113, 140, "CollectItem", "Resolve canonical item")
            box("b", 182, 113, 140, "CollectOptions", "Ask for missing fields")
            box("c", 349, 113, 140, "ReviewCart", "Validate and read back")
            box("d", 349, 39, 140, "SubmitOrder", "Commit approved proposal")
            box("e", 182, 39, 140, "OrderStatus", "Accepted / unknown / failed")
            box("f", 15, 39, 140, "Clarify / staff", "Resolve ambiguity or hand off")
            arrow("a", "b"); arrow("b", "c"); arrow("c", "d", True)
            arrow("c", "f", True); arrow("f", "a", True)
            c.setStrokeColor(TEAL)
            c.line(349,63,322,63); c.line(322,63,327,66); c.line(322,63,327,60)
            caption = "Main path shown; corrections return to capture and invalidate approval."
        elif self.kind == "noctal_jobs":
            box("q", 15, 113, 140, "QUEUED", "Durable submission accepted")
            box("r", 182, 113, 140, "RUNNING", "Worker stage and heartbeat")
            box("s", 349, 113, 140, "SUCCEEDED", "Verified result references")
            box("w", 182, 39, 140, "WAITING_FOR_USER", "Resume after needed input")
            box("f", 349, 39, 140, "FAILED / CANCELED", "Terminal state with reason")
            arrow("q", "r"); arrow("r", "s"); arrow("r", "w", True)
            arrow("w", "r", True); arrow("r", "f", True)
            caption = "Application states, not CX pages; retry/recovery preserves job identity."
        else:
            raise ValueError(self.kind)
        c.setFillColor(MUTED)
        c.setFont("Guide", 8)
        c.drawString(15, 16, caption)

class Cover(Flowable):
    def __init__(self):
        Flowable.__init__(self)
        self.width = WIDTH
        self.height = 660
    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.roundRect(0, 0, WIDTH, 660, 14, fill=1, stroke=0)
        c.setFillColor(TEAL); c.rect(30, 582, 58, 7, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#B4E4E3")); c.setFont("Guide-Bold", 11)
        c.drawString(30, 609, "APPLIED AI FIELD GUIDE")
        c.setFillColor(colors.white); c.setFont("Guide-Bold", 35)
        for line, y in [("Dialogflow CX", 523), ("in Practice", 478)]:
            c.drawString(30, y, line)
        c.setFont("Guide", 15)
        for i, line in enumerate(["Conversational concepts, worked designs,", "and the backend systems behind them"]):
            c.drawString(30, 420-i*23, line)
        c.setStrokeColor(colors.HexColor("#3B536D")); c.line(30, 341, WIDTH-30, 341)
        c.setFillColor(colors.HexColor("#D4E4EF")); c.setFont("Guide-Bold", 12)
        for i, line in enumerate(["Drive-through voice ordering", "Noctal media and job workflows", "Kalshi and Polymarket assistants"]):
            c.drawString(30, 309-i*31, line)
        c.setFont("Guide", 10)
        c.drawString(30, 156, "With framework comparisons, diagrams, and FastAPI contracts")
        c.drawString(30, 134, "Includes the 30 previously completed design answers")
        c.setFillColor(colors.HexColor("#A8BECF")); c.setFont("Guide", 9)
        c.drawString(30, 65, "Prepared for Google Forward Deployed AI Engineer study")
        c.drawString(30, 45, "October 12, 2026  |  Editable source included")

class BookDoc(BaseDocTemplate):
    def __init__(self, path):
        BaseDocTemplate.__init__(self, str(path), pagesize=(PAGE_W, PAGE_H),
            title="Dialogflow CX in Practice: Applied AI Field Guide",
            author="Prepared for Ahmed Jawad", subject="CX, voice, Noctal, Kalshi and Polymarket",
            leftMargin=MARGIN, rightMargin=MARGIN, topMargin=53, bottomMargin=49)
        frame = Frame(MARGIN, 49, WIDTH, PAGE_H-102, leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0, id="body")
        self.addPageTemplates(PageTemplate(id="book", frames=frame, onPage=self.decorations))
        self.heading_pages = []

    def beforeDocument(self):
        self.heading_pages = []

    def decorations(self, c, doc):
        if doc.page == 1:
            return
        c.saveState()
        c.setStrokeColor(LINE); c.setLineWidth(.5)
        c.line(MARGIN, PAGE_H-35, PAGE_W-MARGIN, PAGE_H-35)
        c.setFillColor(MUTED); c.setFont("Guide", 8)
        c.drawString(MARGIN, PAGE_H-27, "DIALOGFLOW CX IN PRACTICE")
        c.drawRightString(PAGE_W-MARGIN, PAGE_H-27, "APPLIED AI FIELD GUIDE")
        c.line(MARGIN, 35, PAGE_W-MARGIN, 35)
        c.drawString(MARGIN, 22, "October 2026 | Proposed designs and illustrative data")
        c.drawRightString(PAGE_W-MARGIN, 22, str(doc.page))
        c.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, "bookmark_key"):
            key = flowable.bookmark_key
            title = flowable.bookmark_title
            level = flowable.bookmark_level
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=level, closed=level > 0)
            self.heading_pages.append({"title": title, "page": self.page, "level": level})
            if flowable.toc_level is not None:
                self.notify("TOCEntry", (flowable.toc_level, title, self.page, key))

heading_counter = 0
def heading(title: str, level: int, toc_level=None):
    global heading_counter
    heading_counter += 1
    style = "ChapterGuide" if level == 0 else ("AnswerTitle" if toc_level == 1 else "SectionGuide")
    p = Paragraph(inline(title), styles[style])
    p.bookmark_key = f"heading-{heading_counter}"
    p.bookmark_title = normalize(title)
    p.bookmark_level = level
    p.toc_level = toc_level
    return p

def code_block(code: str, language: str = ""):
    code = normalize(code)
    # Wrap long commentary only; executable lines must remain intact.
    max_width = WIDTH - 20
    max_line = max((pdfmetrics.stringWidth(line, "Code", 8) for line in code.splitlines()), default=0)
    font_size = min(8, 8*max_width/max_line) if max_line else 8
    if font_size < 6.8:
        raise ValueError(f"Code line too long for readable rendering: {max_line}")
    style = ParagraphStyle("CodeAdjusted", parent=styles["CodeGuide"], fontSize=font_size, leading=font_size*1.4)
    if language == "python":
        source_lines = code.splitlines()
        nodes = ast.parse(code).body
        starts = [node.lineno-1 for node in nodes]
        chunks = ["\n".join(source_lines[start:end]) for start,end in zip(starts, starts[1:]+[len(source_lines)])]
    else:
        chunks = [code]
    # Keep JSON envelopes and individual Python definitions intact across pages.
    return [KeepTogether([Preformatted(chunk, style)]) for chunk in chunks if chunk.strip()]

def table(rows):
    count = len(rows[0])
    fractions = {2:[.30,.70], 3:[.20,.41,.39], 4:[.07,.36,.29,.28]}.get(count, [1/count]*count)
    data = []
    for i, row in enumerate(rows):
        if len(row) != count:
            raise ValueError(f"Bad table row: {row}")
        data.append([Paragraph(inline(cell), styles["CellHeader" if i == 0 else "CellGuide"]) for cell in row])
    t = Table(data, colWidths=[WIDTH*x for x in fractions], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PALE]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LINEBELOW", (0,0), (-1,0), .7, TEAL),
        ("LINEBELOW", (0,1), (-1,-1), .3, LINE),
    ]))
    return [Spacer(1,4), t, Spacer(1,11)]

def parse_markdown(text: str, chapter_title=None, question=False):
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if line.startswith("# "):
            title = chapter_title or line[2:]
            out.append(heading(title, 1 if question else 0, 1 if question else 0))
            i += 1; continue
        if line.startswith("## "):
            next_line = next((x.strip() for x in lines[i+1:] if x.strip()), "")
            if next_line.startswith("|"):
                out.append(CondPageBreak(200))
            if question:
                out.append(Paragraph(inline(line[3:]), styles["AnswerSection"]))
            else:
                out.append(heading(line[3:], 1))
            i += 1; continue
        if line.startswith("```"):
            language = line[3:]; i += 1; code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            if language == "mermaid":
                out.extend([Diagram("foundation"), Spacer(1,12)])
            else:
                out.extend(code_block("\n".join(code), language))
            continue
        if line.startswith(":::diagram "):
            out.extend([Diagram(line.split()[1]), Spacer(1,12)])
            i += 1; continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", x.replace(" ", "")) for x in row):
                    rows.append(row)
                i += 1
            out.extend(table(rows)); continue
        if re.match(r"^\d+\. ", line) or line.startswith("- "):
            out.append(Paragraph(inline(line), styles["BulletGuide"]))
            i += 1; continue
        para = [line]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|```|\||:::|\d+\. |\- )", lines[i].strip()):
            para.append(lines[i].strip()); i += 1
        out.append(Paragraph(inline(" ".join(para)), styles["BodyGuide"]))
    return out

guide_files = sorted((ROOT / "guide").glob("*.md"))
questions = sorted((ROOT / "questions").glob("*.md"))
assert [int(p.name[:3]) for p in questions] == list(range(1,31)), "Retained bank must be Q001-Q030"
sources = guide_files + [ROOT / "FOUNDATIONS.md"] + questions
all_text = "\n\n".join(p.read_text() for p in sources)
(ROOT / "BOOK.md").write_text("# Dialogflow CX in Practice\n\n" + all_text + "\n")

# Check executable syntax and JSON examples without pretending this is deployment testing.
syntax_checks = []
for p in guide_files:
    for language, code in re.findall(r"```(python|json)\n(.*?)\n```", p.read_text(), re.S):
        if language == "python":
            ast.parse(code)
        else:
            json.loads(code)
        syntax_checks.append({"file":p.name, "language":language})

story = [Cover(), PageBreak(), heading("Contents", 0)]
toc = TableOfContents()
toc.levelStyles = [styles["TOC0"], styles["TOC1"]]
toc.dotsMinLevel = 0
story.extend([toc, PageBreak()])
for p in guide_files:
    story.extend(parse_markdown(p.read_text()))
    story.append(PageBreak())
story.extend(parse_markdown((ROOT / "FOUNDATIONS.md").read_text(), chapter_title="Appendix A. Previously written foundations"))
story.extend([PageBreak(), heading("Appendix B. The 30 existing design answers", 0, 0),
    Paragraph("These answers were completed before the scope was narrowed to the detailed CX guide. They are retained without adding further design-question examples.", styles["BodyGuide"]), PageBreak()])
for p in questions:
    story.extend(parse_markdown(p.read_text(), question=True))
    story.append(PageBreak())

story.append(heading("Sources and further reading", 0, 0))
story.append(Paragraph("Primary documentation links used throughout the guide. Reviewed October 12, 2026. Proposed architectures and synthetic conversations are original teaching material.", styles["BodyGuide"]))
links = dict()
for label, url in re.findall(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", all_text):
    links.setdefault(url, label)
for number, (url, label) in enumerate(links.items(), 1):
    label_markup = f"<b>{number}. {escape(label)}</b>"
    url_markup = escape(url).replace("/", "/<wbr/>").replace("-", "-<wbr/>")
    # ReportLab supports splitLongWords and does not require HTML wbr tags.
    url_markup = url_markup.replace("<wbr/>", "")
    story.append(Paragraph(label_markup + f'<br/><link href="{html.escape(url,quote=True)}" color="#007D83">{url_markup}</link>', styles["SmallGuide"]))

doc = BookDoc(PDF)
doc.multiBuild(story)
reader = PdfReader(PDF)
text = "\n".join(page.extract_text() or "" for page in reader.pages)
for term in ["Noctal", "Kalshi", "Polymarket", "CollectOptions", "ApproveNextStep", "MCP", "FastAPI"]:
    assert term in text, f"Missing PDF content: {term}"
for n in range(1,31):
    assert f"Q{n:03d}." in text, f"Missing answer {n}"
assert len(reader.outline) > 0, "Missing bookmarks"
assert "100 answers" not in text, "Stale scope claim"
report = {
    "pdf": str(PDF), "page_count":len(reader.pages),
    "word_count":len(re.findall(r"\b[\w-]+\b", all_text)),
    "retained_answer_count":len(questions), "guide_chapters":len(guide_files),
    "documentation_links":len(links), "syntax_checks":syntax_checks,
    "headings":doc.heading_pages,
    "verification":"Text coverage and syntax checked; visual review recorded separately.",
}
(OUT / "build_report.json").write_text(json.dumps(report, indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ("headings", "syntax_checks")}, indent=2))
