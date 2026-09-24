"""Build Samuel's editing transcript (.docx) from a JSON spec, stock Python only.

    python transcript_docx.py spec.json out.docx

The format follows the video-edit-pass skill, Phase 2: ALL CAPS, flowing paragraphs,
one timecode per chapter header, body text in one colour, red notes for A-roll <-> screen
switches and anything to stop and look at, a purple box around prompts read out on screen.
Each chapter is colour-coded to match its Resolve chapter marker and clip colour:
a filled heading bar plus a matching stripe down the left edge of every paragraph in it.

Spec:
{"title": "...", "subtitle": "...", "fps": 23.976, "end": 13755,
 "chapters": [{"title": "...", "start": 0, "hex": "F2C200", "ink": "000000",
               "blocks": [["p", "text"], ["note", "text"], ["box", "text"],
                          ["bullet", "text"], ["num", "text"]]}]}
"start"/"end" are timeline frames; the chapter's out point is the next chapter's in point.
"""
import json, sys, zipfile
from xml.sax.saxutils import escape

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
CT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>"""
RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>"""
STYLES = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {W}>'
          '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
          '<w:sz w:val="23"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="140" w:line="288" w:lineRule="auto"/>'
          '</w:pPr></w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
          '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
          '<w:pPr><w:keepNext/><w:outlineLvl w:val="0"/></w:pPr></w:style>'
          '</w:styles>')


def numbering():
    def absn(i, fmt, txt):
        return (f'<w:abstractNum w:abstractNumId="{i}"><w:lvl w:ilvl="0"><w:start w:val="1"/>'
                f'<w:numFmt w:val="{fmt}"/><w:lvlText w:val="{txt}"/><w:lvlJc w:val="left"/>'
                '<w:pPr><w:ind w:left="720" w:hanging="300"/></w:pPr></w:lvl></w:abstractNum>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering {W}>'
            + absn(0, "bullet", "•") + absn(1, "decimal", "%1.")
            + '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
            + '<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num></w:numbering>')


def tc(frames, fps):
    base = round(fps)
    s, f = divmod(int(frames), base)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"


def clock(frames, fps):
    m, s = divmod(frames / fps, 60)
    return f"{int(m)}:{s:05.2f}"


def run(text, color=None, bold=False, size=None, caps=True):
    rpr = ""
    if bold: rpr += "<w:b/>"
    if color: rpr += f'<w:color w:val="{color}"/>'
    if size: rpr += f'<w:sz w:val="{size}"/>'
    t = text.upper() if caps else text
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>'


def stripe(hexc):
    return f'<w:pBdr><w:left w:val="single" w:sz="36" w:space="10" w:color="{hexc}"/></w:pBdr>'


def para(inner, ppr=""):
    return f"<w:p><w:pPr>{ppr}</w:pPr>{inner}</w:p>"


def build(spec):
    fps = spec.get("fps", 23.976)
    body = [para(run(spec["title"], bold=True, size=36), '<w:jc w:val="center"/><w:spacing w:after="80"/>')]
    if spec.get("subtitle"):
        body.append(para(run(spec["subtitle"], color="595959", size=20), '<w:jc w:val="center"/><w:spacing w:after="240"/>'))
    chs = spec["chapters"]
    # colour key
    body.append(para(run("CHAPTERS (COLOURS MATCH THE RESOLVE MARKERS AND CLIP COLOURS)", bold=True, size=20),
                     '<w:spacing w:before="120" w:after="80"/>'))
    for i, ch in enumerate(chs):
        out = chs[i + 1]["start"] if i + 1 < len(chs) else spec["end"]
        key = f'  {i + 1}. {ch["title"]}   {clock(ch["start"], fps)} – {clock(out, fps)}'
        body.append(para(run(key, size=20), stripe(ch["hex"]) + '<w:spacing w:after="40"/><w:ind w:left="200"/>'))
    for i, ch in enumerate(chs):
        out = chs[i + 1]["start"] if i + 1 < len(chs) else spec["end"]
        hexc, ink = ch["hex"], ch.get("ink", "FFFFFF")
        head = (f'<w:pStyle w:val="Heading1"/><w:shd w:val="clear" w:color="auto" w:fill="{hexc}"/>'
                '<w:spacing w:before="360" w:after="60"/><w:ind w:left="120" w:right="120"/>')
        body.append(para(run(f'{i + 1}. {ch["title"]}', color=ink, bold=True, size=28), head))
        body.append(para(run(f'{tc(ch["start"], fps)} – {tc(out, fps)}   ({clock(ch["start"], fps)} – {clock(out, fps)})',
                             color=ink, size=19), f'<w:shd w:val="clear" w:color="auto" w:fill="{hexc}"/>'
                                                   '<w:spacing w:after="200"/><w:ind w:left="120" w:right="120"/>'))
        for kind, text in ch["blocks"]:
            if kind == "p":
                body.append(para(run(text), stripe(hexc)))
            elif kind == "note":
                body.append(para(run("NOTE: ", color="C00000", bold=True) + run(text, color="C00000", bold=True, size=20),
                                 stripe(hexc) + '<w:spacing w:after="140"/>'))
            elif kind == "box":
                bd = "".join(f'<w:{s} w:val="single" w:sz="12" w:space="6" w:color="7030A0"/>' for s in ("top", "left", "bottom", "right"))
                body.append(para(run("PROMPT READ OUT ON SCREEN", color="7030A0", bold=True, size=18) + "<w:r><w:br/></w:r>" + run(text),
                                 f'<w:pBdr>{bd}</w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="F3ECFA"/>'
                                 '<w:ind w:left="360" w:right="360"/><w:spacing w:before="120" w:after="200"/>'))
            elif kind in ("bullet", "num"):
                nid = 1 if kind == "bullet" else 2
                body.append(para(run(text), f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{nid}"/></w:numPr>'
                                            '<w:spacing w:after="60"/>'))
    sect = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
            '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="0" w:footer="0" w:gutter="0"/></w:sectPr>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>'
            + "".join(body) + sect + "</w:body></w:document>")


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", build(spec))
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/numbering.xml", numbering())
    print(out)


if __name__ == "__main__":
    main()
