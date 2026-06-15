#!/usr/bin/env python3
"""ReportPDF: Professional PDF report builder using fpdf2's native API.

Pure Python. Zero system dependencies. Cross-platform (macOS, Ubuntu, etc.).
Renders directly — no HTML/CSS intermediary, no lossy conversion.
"""

import os
import platform
import re
from pathlib import Path

from fpdf import FPDF


# ---------------------------------------------------------------------------
# Inline markdown parser
# ---------------------------------------------------------------------------

_INLINE_RE = re.compile(
    r"(\*\*\*(.+?)\*\*\*)"
    r"|(\*\*(.+?)\*\*)"
    r"|(?<!\w)(\*(.+?)\*)(?!\w)"
    r"|(`([^`]+?)`)"
    r"|(\[([^\]]+?)\]\(([^)]+?)\))"
)


def _parse_inline(text):
    """Split text into (content, style) segments.

    Styles: "normal", "bold", "italic", "bold_italic", "code", ("link", url)
    """
    segments = []
    pos = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            segments.append((text[pos : m.start()], "normal"))
        if m.group(2):
            segments.append((m.group(2), "bold_italic"))
        elif m.group(4):
            segments.append((m.group(4), "bold"))
        elif m.group(6):
            segments.append((m.group(6), "italic"))
        elif m.group(8):
            segments.append((m.group(8), "code"))
        elif m.group(10):
            segments.append((m.group(10), ("link", m.group(11))))
        pos = m.end()
    if pos < len(text):
        segments.append((text[pos:], "normal"))
    return segments or [(text, "normal")]


# ---------------------------------------------------------------------------
# System font discovery
# ---------------------------------------------------------------------------


def _find_system_fonts():
    system = platform.system()
    if system == "Darwin":
        base = "/System/Library/Fonts/Supplemental"
        fonts = {
            "sans": f"{base}/Arial.ttf",
            "sans_bold": f"{base}/Arial Bold.ttf",
            "sans_italic": f"{base}/Arial Italic.ttf",
            "sans_bi": f"{base}/Arial Bold Italic.ttf",
            "mono": f"{base}/Courier New.ttf",
            "mono_bold": f"{base}/Courier New Bold.ttf",
        }
    elif system == "Linux":
        base = "/usr/share/fonts/truetype/dejavu"
        fonts = {
            "sans": f"{base}/DejaVuSans.ttf",
            "sans_bold": f"{base}/DejaVuSans-Bold.ttf",
            "sans_italic": f"{base}/DejaVuSans-Oblique.ttf",
            "sans_bi": f"{base}/DejaVuSans-BoldOblique.ttf",
            "mono": f"{base}/DejaVuSansMono.ttf",
            "mono_bold": f"{base}/DejaVuSansMono-Bold.ttf",
        }
    else:
        return None
    if all(os.path.exists(f) for f in fonts.values()):
        return fonts
    return None


# ---------------------------------------------------------------------------
# ReportPDF
# ---------------------------------------------------------------------------


class ReportPDF(FPDF):
    """Build professional PDF reports with fpdf2's native drawing API."""

    # ── Design tokens ──────────────────────────────────────────────────────
    BLUE = (37, 99, 235)
    NAVY = (30, 58, 95)
    DARK = (26, 26, 26)
    MUTED = (100, 116, 139)
    LIGHT = (248, 250, 252)
    CODE_BG = (30, 41, 59)
    CODE_FG = (226, 232, 240)
    PINK = (190, 24, 93)
    BORDER = (226, 232, 240)
    CALLOUT_BG = (239, 246, 255)
    WHITE = (255, 255, 255)

    BODY_PT = 10.5
    H1_PT = 24
    H2_PT = 17
    H3_PT = 13
    H4_PT = 11.5
    SMALL_PT = 9
    CODE_PT = 9
    LH = 5.5  # default line-height (mm)

    # ── Setup ──────────────────────────────────────────────────────────────

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(22, 22, 22)
        self.alias_nb_pages()
        self._sans = "Helvetica"
        self._mono = "Courier"
        self._unicode = False
        self._try_load_fonts()

    def _try_load_fonts(self):
        fonts = _find_system_fonts()
        if not fonts:
            return
        try:
            self.add_font("_s", "", fonts["sans"])
            self.add_font("_s", "B", fonts["sans_bold"])
            self.add_font("_s", "I", fonts["sans_italic"])
            self.add_font("_s", "BI", fonts["sans_bi"])
            self.add_font("_m", "", fonts["mono"])
            self.add_font("_m", "B", fonts["mono_bold"])
            self._sans = "_s"
            self._mono = "_m"
            self._unicode = True
        except Exception:
            pass

    def _s(self, text):
        """Sanitize text for the active font encoding."""
        if self._unicode:
            return text
        reps = {
            "—": "--",
            "–": "-",
            "‘": "'",
            "’": "'",
            "“": '"',
            "”": '"',
            "…": "...",
            "→": "->",
            "←": "<-",
            "•": "-",
            "✓": "[x]",
            "☐": "[ ]",
            "☑": "[x]",
            " ": " ",
            "□": "[ ]",
        }
        for k, v in reps.items():
            text = text.replace(k, v)
        return text.encode("latin-1", "replace").decode("latin-1")

    # ── Page chrome ────────────────────────────────────────────────────────

    def footer(self):
        self.set_y(-15)
        self.set_font(self._sans, "", 8)
        self.set_text_color(*self.MUTED)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")
        self.set_text_color(*self.DARK)

    # ── Block elements ─────────────────────────────────────────────────────

    def add_title(self, text, date=None):
        """Title block with accent underline. Adds a new page."""
        self.add_page()
        self.ln(12)
        self.set_font(self._sans, "B", self.H1_PT)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, self.H1_PT * 0.55, self._s(text))
        if date:
            self.ln(2)
            self.set_font(self._sans, "", self.SMALL_PT)
            self.set_text_color(*self.MUTED)
            self.cell(0, 5, date)
            self.ln(5)
        y = self.get_y() + 4
        self.set_draw_color(*self.BLUE)
        self.set_line_width(1)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.set_y(y + 8)
        self.set_text_color(*self.DARK)

    def add_heading(self, text, level=2):
        if level <= 1:
            self.ln(10)
            self.set_font(self._sans, "B", self.H1_PT - 2)
            self.set_text_color(*self.DARK)
            self.multi_cell(0, (self.H1_PT - 2) * 0.55, self._s(text))
            y = self.get_y() + 3
            self.set_draw_color(*self.BLUE)
            self.set_line_width(0.8)
            self.line(self.l_margin, y, self.w - self.r_margin, y)
            self.set_y(y + 6)
        elif level == 2:
            self.ln(6)
            self.set_font(self._sans, "B", self.H2_PT)
            self.set_text_color(*self.NAVY)
            self.multi_cell(0, self.H2_PT * 0.55, self._s(text))
            y = self.get_y() + 2
            self.set_draw_color(*self.BORDER)
            self.set_line_width(0.3)
            self.line(self.l_margin, y, self.w - self.r_margin, y)
            self.set_y(y + 4)
        elif level == 3:
            self.ln(5)
            self.set_font(self._sans, "B", self.H3_PT)
            self.set_text_color(*self.BLUE)
            self.multi_cell(0, self.H3_PT * 0.5, self._s(text))
            self.ln(2)
        else:
            self.ln(4)
            self.set_font(self._sans, "B", self.H4_PT)
            self.set_text_color(*self.MUTED)
            self.multi_cell(0, self.H4_PT * 0.5, self._s(text))
            self.ln(1)
        self.set_text_color(*self.DARK)

    def add_paragraph(self, text):
        self.set_font(self._sans, "", self.BODY_PT)
        self._write_rich(text)
        self.ln(self.LH)

    def add_bullets(self, items):
        saved = self.l_margin
        indent = saved + 7
        for item in items:
            self.set_x(saved + 1)
            # Bullet marker
            self.set_font(self._sans, "B", 7)
            self.set_text_color(*self.BLUE)
            bullet = "•" if self._unicode else "-"
            self.cell(5, self.LH, self._s(bullet), new_x="RIGHT", new_y="TOP")
            self.set_text_color(*self.DARK)
            self.set_font(self._sans, "", self.BODY_PT)
            # Item text — temporarily shift left margin so write() wraps correctly
            self.l_margin = indent
            self.set_x(indent)
            self._write_rich(item)
            self.ln(self.LH * 0.85)
        self.l_margin = saved
        self.ln(1)

    def add_numbered(self, items):
        saved = self.l_margin
        indent = saved + 8
        for i, item in enumerate(items, 1):
            self.set_x(saved)
            self.set_font(self._sans, "B", self.BODY_PT)
            self.set_text_color(*self.BLUE)
            self.cell(7, self.LH, f"{i}.", new_x="RIGHT", new_y="TOP")
            self.set_text_color(*self.DARK)
            self.set_font(self._sans, "", self.BODY_PT)
            self.l_margin = indent
            self.set_x(indent)
            self._write_rich(item)
            self.ln(self.LH * 0.85)
        self.l_margin = saved
        self.ln(1)

    def _calc_cell_height(self, text, col_width, line_h):
        """Calculate the height needed for wrapped text in a cell."""
        usable = col_width - 3  # 1.5mm padding each side
        if not text or usable <= 0:
            return line_h
        words = text.split(" ")
        lines = 1
        current_line = ""
        for word in words:
            test = f"{current_line} {word}".strip()
            if self.get_string_width(test) > usable:
                if current_line:
                    lines += 1
                    current_line = word
                else:
                    current_line = word
            else:
                current_line = test
        return max(lines * line_h, line_h)

    def add_table(self, headers, rows):
        if not headers:
            return
        ncols = len(headers)
        W = self.w - self.l_margin - self.r_margin
        line_h = 5  # single line height within cells

        # Column widths: ensure each column fits its widest word, then
        # distribute remaining space proportionally to content length.
        self.set_font(self._sans, "", self.SMALL_PT)
        padding = 3  # 1.5mm each side
        min_widths = []
        content_lens = []
        for ci in range(ncols):
            widest_word_w = self.get_string_width(headers[ci])
            col_max_len = len(headers[ci])
            for row in rows:
                val = str(row[ci]) if ci < len(row) else ""
                col_max_len = max(col_max_len, len(val))
                for word in val.split(" "):
                    widest_word_w = max(widest_word_w, self.get_string_width(word))
            min_widths.append(widest_word_w + padding + 1)
            content_lens.append(max(col_max_len, 3))

        total_min = sum(min_widths)
        if total_min >= W:
            scale = W / total_min
            widths = [mw * scale for mw in min_widths]
        else:
            remaining = W - total_min
            total_lens = sum(content_lens)
            widths = [
                mw + remaining * (cl / total_lens)
                for mw, cl in zip(min_widths, content_lens)
            ]

        def _render_header():
            self.set_font(self._sans, "B", self.SMALL_PT)
            self.set_fill_color(*self.NAVY)
            self.set_text_color(*self.WHITE)
            self.set_draw_color(*self.NAVY)
            x0 = self.get_x()
            y0 = self.get_y()
            row_h = line_h + 2
            for ci, h in enumerate(headers):
                x = x0 + sum(widths[:ci])
                self.rect(x, y0, widths[ci], row_h, "DF")
                self.set_xy(x + 1.5, y0 + 1)
                self.cell(widths[ci] - 3, line_h, self._s(h),
                          new_x="RIGHT", new_y="TOP")
            self.set_xy(x0, y0 + row_h)
            self.set_text_color(*self.DARK)

        _render_header()

        # Data rows
        self.set_font(self._sans, "", self.SMALL_PT)
        self.set_draw_color(*self.BORDER)
        for ri, row in enumerate(rows):
            # Calculate row height based on tallest cell
            cells = []
            for ci in range(ncols):
                val = self._s(str(row[ci])) if ci < len(row) else ""
                cells.append(val)
            self.set_font(self._sans, "", self.SMALL_PT)
            row_h = line_h + 2  # minimum row height
            for ci, val in enumerate(cells):
                ch = self._calc_cell_height(val, widths[ci], line_h) + 2
                row_h = max(row_h, ch)

            # Page break with repeated header
            if self.get_y() + row_h > self.h - self.b_margin:
                self.add_page()
                _render_header()
                self.set_font(self._sans, "", self.SMALL_PT)
                self.set_draw_color(*self.BORDER)

            x0 = self.get_x()
            y0 = self.get_y()
            fill_color = self.LIGHT if ri % 2 else self.WHITE
            self.set_fill_color(*fill_color)
            self.set_text_color(*self.DARK)

            for ci, val in enumerate(cells):
                x = x0 + sum(widths[:ci])
                # Draw cell background and border
                self.set_fill_color(*fill_color)
                self.set_draw_color(*self.BORDER)
                self.rect(x, y0, widths[ci], row_h, "DF")
                # Write wrapped text
                self.set_xy(x + 1.5, y0 + 1)
                saved_margin = self.l_margin
                self.l_margin = x + 1.5
                self.multi_cell(widths[ci] - 3, line_h, val)
                self.l_margin = saved_margin

            self.set_xy(x0, y0 + row_h)
        self.ln(4)
        self.set_text_color(*self.DARK)

    def add_code(self, text):
        self.ln(2)
        self.set_font(self._mono, "", self.CODE_PT)
        lh = 4.2
        w = self.w - self.l_margin - self.r_margin
        for line in text.split("\n"):
            if self.get_y() + lh > self.h - self.b_margin:
                self.add_page()
            self.set_fill_color(*self.CODE_BG)
            self.set_text_color(*self.CODE_FG)
            self.set_x(self.l_margin)
            self.cell(w, lh, "  " + self._s(line), fill=True)
            self.ln(lh)
        self.ln(3)
        self.set_text_color(*self.DARK)

    def add_callout(self, text):
        self.ln(2)
        self.set_font(self._sans, "I", self.BODY_PT)
        self.set_fill_color(*self.CALLOUT_BG)
        self.set_text_color(51, 65, 85)
        x0 = self.l_margin
        y0 = self.get_y()
        w = self.w - self.l_margin - self.r_margin
        indent = 8
        self.set_x(x0 + indent)
        self.multi_cell(w - indent - 2, self.LH, self._s(text), fill=True)
        y1 = self.get_y()
        # Left accent bar
        self.set_fill_color(*self.BLUE)
        self.rect(x0, y0, 3, y1 - y0, "F")
        self.ln(3)
        self.set_text_color(*self.DARK)

    def add_separator(self):
        self.ln(3)
        y = self.get_y()
        self.set_draw_color(*self.BORDER)
        self.set_line_width(0.3)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(5)

    # ── Inline rich text ───────────────────────────────────────────────────

    def _write_rich(self, text):
        """Write text with inline **bold**, *italic*, `code`, [link](url)."""
        lh = self.LH
        for seg, style in _parse_inline(text):
            seg = self._s(seg)
            if style == "bold":
                self.set_font(self._sans, "B", self.BODY_PT)
            elif style == "italic":
                self.set_font(self._sans, "I", self.BODY_PT)
            elif style == "bold_italic":
                self.set_font(self._sans, "BI", self.BODY_PT)
            elif style == "code":
                self.set_font(self._mono, "", self.BODY_PT - 1)
                self.set_text_color(*self.PINK)
            elif isinstance(style, tuple):
                self.set_font(self._sans, "U", self.BODY_PT)
                self.set_text_color(*self.BLUE)
                self.write(lh, seg, style[1])
                self.set_font(self._sans, "", self.BODY_PT)
                self.set_text_color(*self.DARK)
                continue
            else:
                self.set_font(self._sans, "", self.BODY_PT)
                self.set_text_color(*self.DARK)
            self.write(lh, seg)
            # Reset after each segment
            self.set_font(self._sans, "", self.BODY_PT)
            self.set_text_color(*self.DARK)

    # ── Output ─────────────────────────────────────────────────────────────

    def save(self, path):
        self.output(str(path))
        return Path(path)


# ---------------------------------------------------------------------------
# Markdown → structured blocks
# ---------------------------------------------------------------------------


def parse_markdown(md_text):
    """Parse markdown into a list of typed block dicts."""
    blocks = []
    lines = md_text.split("\n")
    i, n = 0, len(lines)

    # Skip YAML front-matter
    if i < n and lines[i].strip() == "---":
        i += 1
        while i < n and lines[i].strip() != "---":
            i += 1
        if i < n:
            i += 1

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Heading
        hm = re.match(r"^(#{1,4})\s+(.+)$", line)
        if hm:
            blocks.append(
                {"type": "heading", "level": len(hm.group(1)), "text": hm.group(2).strip()}
            )
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^[-*_]{3,}\s*$", stripped):
            blocks.append({"type": "separator"})
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            blocks.append({"type": "code", "text": "\n".join(code_lines), "lang": lang})
            continue

        # Table (must have | at start and end, at least 3 pipes)
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 3:
            tlines = []
            while (
                i < n
                and lines[i].strip().startswith("|")
                and lines[i].strip().endswith("|")
            ):
                tlines.append(lines[i])
                i += 1
            if len(tlines) >= 2:
                headers = [c.strip() for c in tlines[0].split("|")[1:-1]]
                start = 2 if re.match(r"^[\s|:\-]+$", tlines[1]) else 1
                rows = []
                for tl in tlines[start:]:
                    rows.append([c.strip() for c in tl.split("|")[1:-1]])
                blocks.append({"type": "table", "headers": headers, "rows": rows})
            continue

        # Blockquote
        if stripped.startswith(">"):
            qlines = []
            while i < n and lines[i].strip().startswith(">"):
                qlines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append({"type": "callout", "text": " ".join(qlines)})
            continue

        # Bullet list (including task-list items)
        if re.match(r"^[\s]*[-*+]\s", line):
            items = []
            while i < n and re.match(r"^[\s]*[-*+]\s", lines[i]):
                txt = re.sub(r"^[\s]*[-*+]\s", "", lines[i]).strip()
                cm = re.match(r"^\[([ xX])\]\s*(.*)", txt)
                if cm:
                    mark = "[x]" if cm.group(1).lower() == "x" else "[ ]"
                    txt = f"{mark} {cm.group(2)}"
                items.append(txt)
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue

        # Numbered list
        if re.match(r"^[\s]*\d+[.)]\s", line):
            items = []
            while i < n and re.match(r"^[\s]*\d+[.)]\s", lines[i]):
                items.append(re.sub(r"^[\s]*\d+[.)]\s", "", lines[i]).strip())
                i += 1
            blocks.append({"type": "numbered", "items": items})
            continue

        # Paragraph — collect consecutive non-special lines
        plines = []
        while i < n:
            ln = lines[i]
            s = ln.strip()
            if not s:
                break
            if s.startswith("#"):
                break
            if re.match(r"^[-*_]{3,}\s*$", s):
                break
            if s.startswith("```"):
                break
            if s.startswith("|") and s.endswith("|") and s.count("|") >= 3:
                break
            if re.match(r"^[\s]*[-*+]\s", ln):
                break
            if re.match(r"^[\s]*\d+[.)]\s", ln):
                break
            if s.startswith(">"):
                break
            plines.append(s)
            i += 1
        if plines:
            blocks.append({"type": "paragraph", "text": " ".join(plines)})

    return blocks


# ---------------------------------------------------------------------------
# High-level render function
# ---------------------------------------------------------------------------


def render_report(md_text, output_path):
    """Parse markdown and render a styled PDF.

    Returns the output Path.
    """
    blocks = parse_markdown(md_text)
    pdf = ReportPDF()

    title_done = False
    for block in blocks:
        t = block["type"]
        if t == "heading":
            if not title_done and block["level"] == 1:
                pdf.add_title(block["text"])
                title_done = True
            else:
                pdf.add_heading(block["text"], block["level"])
        elif t == "paragraph":
            pdf.add_paragraph(block["text"])
        elif t == "bullets":
            pdf.add_bullets(block["items"])
        elif t == "numbered":
            pdf.add_numbered(block["items"])
        elif t == "table":
            pdf.add_table(block["headers"], block["rows"])
        elif t == "code":
            pdf.add_code(block["text"])
        elif t == "callout":
            pdf.add_callout(block["text"])
        elif t == "separator":
            pdf.add_separator()

    return pdf.save(output_path)
