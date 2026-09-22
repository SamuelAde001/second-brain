/**
 * TEMPLATE: Subtitle -> Formatted Transcript .docx builder
 *
 * HOW TO USE THIS FILE:
 * This is a STYLING TEMPLATE, not a content template. Copy this file to a working
 * location (e.g. /home/claude/build.js), then replace the `children.push(...)` calls
 * in the "Document build" section below with the ACTUAL reconstructed transcript
 * content for the current video: real section titles, real lines (one sentence or
 * tight thought per line), and real bullet/numbered list items pulled from the
 * speaker's lists. Do not invent content — this only supplies the formatting helpers
 * (sectionTitle / line / bullet / numbered) and page setup.
 *
 * Requires: `docx` npm package (preinstalled in this environment — just require it,
 * do not run `npm install` first; only install if the require() call fails).
 *
 * RUN:
 *   node build.js
 *
 * VERIFY (always do this before sharing):
 *   python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf output.docx
 *   pdftoppm -jpeg -r 100 output.pdf page
 *   # then view page-01.jpg, a middle page with a list, and the last page
 */

const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  AlignmentType, BorderStyle, LevelFormat, convertInchesToTwip
} = require("docx");

// ---- CUSTOMIZE: document title shown centered at the top ----
const DOC_TITLE = "REPLACE WITH VIDEO TITLE — FULL TRANSCRIPT";
// ---- CUSTOMIZE: output filename ----
const OUTPUT_PATH = "/home/claude/Formatted_Transcript.docx";

// Helper builders -------------------------------------------------------
// All helpers force ALL CAPS via .toUpperCase() so you can pass content in
// natural case and not worry about it — the skill's Step 5 requirement is
// automatically enforced here.

function sectionTitle(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    border: {
      bottom: { color: "1F4E79", space: 4, style: BorderStyle.SINGLE, size: 12 },
    },
    children: [
      new TextRun({ text: text.toUpperCase(), bold: true, color: "1F4E79", size: 30 }),
    ],
  });
}

// One paragraph per sentence / tight thought — this is what makes the
// document "skimmable" per Step 6. Do not combine many sentences into one
// line() call; call line() once per sentence or very tight 2-sentence group.
function line(text) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text: text.toUpperCase(), size: 24 })],
  });
}

// Use for flat/unordered lists (Step 4 rule).
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullet-list", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text: text.toUpperCase(), size: 24 })],
  });
}

// Use for sequential/named/ordinal lists, named examples walked through in
// order, or step-by-step processes (Step 4 rule).
function numbered(text) {
  return new Paragraph({
    numbering: { reference: "number-list", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text: text.toUpperCase(), size: 24 })],
  });
}

// Document build ----------------------------------------------------------
// REPLACE everything below this line with the real transcript content.
// Pattern to follow for every narrative beat in the video:
//   children.push(sectionTitle("Section N: Descriptive Title"));
//   children.push(line("First reconstructed full sentence the speaker said."));
//   children.push(line("Next sentence..."));
//   children.push(line("Sentence introducing a list, ending in a colon:"));
//   children.push(bullet("First listed item"));   // or numbered(...)
//   children.push(bullet("Second listed item"));
//   children.push(line("Sentence continuing after the list."));
// ...repeat for every section until the transcript is fully covered end-to-end.

const children = [];

children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({ text: DOC_TITLE, bold: true, size: 36, color: "1F4E79" })],
  })
);

// == EXAMPLE (delete and replace with real content) ==
children.push(sectionTitle("Section 1: Example Section Title"));
children.push(line("Replace this with the first real reconstructed sentence."));
children.push(line("Sentence that introduces a list of items:"));
children.push(bullet("Example Item One"));
children.push(bullet("Example Item Two"));
// == END EXAMPLE ==

// Build the doc -----------------------------------------------------------

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [
          {
            level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.2) } } },
          },
        ],
      },
      {
        reference: "number-list",
        levels: [
          {
            level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.2) } } },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 }, // US Letter
          margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 },
        },
      },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  require("fs").writeFileSync(OUTPUT_PATH, buf);
  console.log("done:", OUTPUT_PATH);
});
