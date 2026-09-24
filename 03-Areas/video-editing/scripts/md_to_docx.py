"""Turn a simple Markdown brief into a Word .docx, stock Python only (no python-docx).

Handles what client briefs use: #/##/### headings, "- " bullets, "> " quote lines
(rendered italic, for on-screen/demo directions), **bold** runs, blank-line paragraphs.

    python md_to_docx.py "<in.md>" ["<out.docx>"]
"""
import re, sys, zipfile
from xml.sax.saxutils import escape

CT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""
RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def style(sid, name, size, bold=False, before=0, after=120):
    b = "<w:b/>" if bold else ""
    return (f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/>'
            f'<w:pPr><w:spacing w:before="{before}" w:after="{after}"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>{b}<w:sz w:val="{size}"/></w:rPr></w:style>')


STYLES = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {W}>'
          + style("Normal", "Normal", 22)
          + style("Heading1", "heading 1", 36, True, 240, 160)
          + style("Heading2", "heading 2", 30, True, 320, 120)
          + style("Heading3", "heading 3", 25, True, 240, 80)
          + "</w:styles>")


def runs(text, italic=False):
    out = []
    for i, part in enumerate(re.split(r"\*\*", text)):
        if not part:
            continue
        rpr = ("<w:b/>" if i % 2 else "") + ("<w:i/>" if italic else "")
        out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def para(text, sid="Normal", italic=False, indent=0):
    ind = f'<w:ind w:left="{indent}" w:hanging="{240 if indent else 0}"/>' if indent else ""
    return f'<w:p><w:pPr><w:pStyle w:val="{sid}"/>{ind}</w:pPr>{runs(text, italic)}</w:p>'


def convert(md):
    body = []
    for line in md.splitlines():
        s = line.rstrip()
        if not s:
            continue
        m = re.match(r"(#{1,3}) (.*)", s)
        if m:
            body.append(para(m.group(2), f"Heading{len(m.group(1))}"))
        elif s.startswith("- "):
            body.append(para("•  " + s[2:], indent=480))
        elif s.startswith(">"):
            t = s.lstrip("> ").strip()
            if t:
                body.append(para(t, italic=True, indent=360))
        else:
            body.append(para(s))
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>'
            + "".join(body) + "<w:sectPr/></w:body></w:document>")


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else re.sub(r"\.md$", "", src) + ".docx"
    doc = convert(open(src, encoding="utf-8").read())
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", STYLES)
    print(out)


if __name__ == "__main__":
    main()
