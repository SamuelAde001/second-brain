/**
 * engine -> Google Sheets bridge.
 *
 * Bound to "My Claude Budget". Deployed as a web app so Claude Code can read and
 * write the budget from the terminal, from the phone, or from a cloud routine.
 *
 * This script is GENERIC ON PURPOSE. It is a set of primitives (read, write,
 * append, format, ensureSheet...) not a set of budget-specific functions, so the
 * budget can be redesigned as often as needed without ever re-pasting this file.
 *
 * Paste once. Deploy once. Never touch again.
 */

var TOKEN = '__SHEETS_TOKEN__';  // substituted at paste time from .env — never committed

function doPost(e) {
  try {
    var req = JSON.parse(e.postData.contents);
    if (req.token !== TOKEN) return out({ ok: false, error: 'bad token' });

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var ops = req.ops || [{ action: req.action, args: req.args || req }];
    var results = [];

    for (var i = 0; i < ops.length; i++) {
      results.push(run(ss, ops[i].action, ops[i].args || {}));
    }
    SpreadsheetApp.flush();
    return out({ ok: true, results: results });
  } catch (err) {
    return out({ ok: false, error: String(err), stack: err.stack || null });
  }
}

function doGet() {
  return out({ ok: true, note: 'engine sheets bridge is alive. POST to use it.' });
}

function out(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function sheetOf(ss, name) {
  var sh = ss.getSheetByName(name);
  if (!sh) throw new Error('no such tab: ' + name);
  return sh;
}

function run(ss, action, a) {
  var sh, rng;

  switch (action) {

    // ---------- discovery ----------

    case 'ping':
      return {
        name: ss.getName(),
        id: ss.getId(),
        url: ss.getUrl(),
        tabs: ss.getSheets().map(function (s) {
          return { name: s.getName(), rows: s.getLastRow(), cols: s.getLastColumn(), index: s.getIndex() };
        })
      };

    // ---------- reading ----------

    case 'read':
      sh = sheetOf(ss, a.tab);
      rng = a.range ? sh.getRange(a.range) : sh.getDataRange();
      return { tab: a.tab, range: rng.getA1Notation(), values: rng.getDisplayValues() };

    case 'readRaw':
      sh = sheetOf(ss, a.tab);
      rng = a.range ? sh.getRange(a.range) : sh.getDataRange();
      return { tab: a.tab, range: rng.getA1Notation(), values: rng.getValues() };

    case 'readFormulas':
      sh = sheetOf(ss, a.tab);
      rng = a.range ? sh.getRange(a.range) : sh.getDataRange();
      return { tab: a.tab, range: rng.getA1Notation(), formulas: rng.getFormulas() };

    case 'find':
      // find the first row in `column` whose display value equals `value`
      sh = sheetOf(ss, a.tab);
      var col = sh.getRange(a.column + '1:' + a.column + sh.getLastRow()).getDisplayValues();
      for (var r = 0; r < col.length; r++) {
        if (String(col[r][0]).trim() === String(a.value).trim()) return { row: r + 1 };
      }
      return { row: null };

    // ---------- writing ----------

    case 'write':
      // args: tab, cell (top-left A1), values [[...]]
      sh = sheetOf(ss, a.tab);
      var v = a.values;
      sh.getRange(a.cell).offset(0, 0, v.length, v[0].length).setValues(v);
      return { wrote: v.length + 'x' + v[0].length + ' at ' + a.cell };

    case 'append':
      // args: tab, values [[...]]  - appends after the last row with content
      sh = sheetOf(ss, a.tab);
      var start = (a.after ? a.after : sh.getLastRow()) + 1;
      sh.getRange(start, a.startCol || 1, a.values.length, a.values[0].length).setValues(a.values);
      return { appendedAtRow: start, rows: a.values.length };

    case 'setFormulas':
      sh = sheetOf(ss, a.tab);
      sh.getRange(a.cell).offset(0, 0, a.formulas.length, a.formulas[0].length).setFormulas(a.formulas);
      return { wroteFormulas: a.cell };

    case 'clear':
      sh = sheetOf(ss, a.tab);
      rng = a.range ? sh.getRange(a.range) : sh.getDataRange();
      if (a.contentsOnly) { rng.clearContent(); } else { rng.clear(); }
      return { cleared: rng.getA1Notation() };

    // ---------- structure ----------

    case 'ensureSheet':
      sh = ss.getSheetByName(a.tab);
      var created = false;
      if (!sh) { sh = ss.insertSheet(a.tab); created = true; }
      if (a.index != null) { ss.setActiveSheet(sh); ss.moveActiveSheet(a.index); }
      if (a.tabColor) sh.setTabColor(a.tabColor);
      return { tab: a.tab, created: created };

    case 'deleteSheet':
      ss.deleteSheet(sheetOf(ss, a.tab));
      return { deleted: a.tab };

    case 'renameSheet':
      sheetOf(ss, a.tab).setName(a.to);
      return { renamed: a.tab + ' -> ' + a.to };

    case 'insertRows':
      sh = sheetOf(ss, a.tab);
      sh.insertRowsBefore(a.before, a.count || 1);
      return { inserted: a.count || 1, before: a.before };

    case 'deleteRows':
      sh = sheetOf(ss, a.tab);
      sh.deleteRows(a.row, a.count || 1);
      return { deletedRows: a.count || 1, from: a.row };

    case 'insertColumns':
      sh = sheetOf(ss, a.tab);
      sh.insertColumnsBefore(a.before, a.count || 1);
      return { insertedCols: a.count || 1, before: a.before };

    case 'setColumnWidth':
      sh = sheetOf(ss, a.tab);
      sh.setColumnWidth(a.column, a.width);
      return { column: a.column, width: a.width };

    case 'setRowHeight':
      sh = sheetOf(ss, a.tab);
      sh.setRowHeight(a.row, a.height);
      return { row: a.row, height: a.height };

    case 'freeze':
      sh = sheetOf(ss, a.tab);
      if (a.rows != null) sh.setFrozenRows(a.rows);
      if (a.columns != null) sh.setFrozenColumns(a.columns);
      return { frozeRows: a.rows, frozeCols: a.columns };

    // ---------- formatting ----------

    case 'format':
      sh = sheetOf(ss, a.tab);
      rng = sh.getRange(a.range);
      if (a.background) rng.setBackground(a.background);
      if (a.fontColor) rng.setFontColor(a.fontColor);
      if (a.fontSize) rng.setFontSize(a.fontSize);
      if (a.fontFamily) rng.setFontFamily(a.fontFamily);
      if (a.bold != null) rng.setFontWeight(a.bold ? 'bold' : 'normal');
      if (a.italic != null) rng.setFontStyle(a.italic ? 'italic' : 'normal');
      if (a.numberFormat) rng.setNumberFormat(a.numberFormat);
      if (a.horizontalAlignment) rng.setHorizontalAlignment(a.horizontalAlignment);
      if (a.verticalAlignment) rng.setVerticalAlignment(a.verticalAlignment);
      if (a.wrap != null) rng.setWrap(a.wrap);
      if (a.merge) rng.merge();
      if (a.unmerge) rng.breakApart();
      if (a.border) {
        // border: [top, left, bottom, right, vertical, horizontal, color, style]
        var b = a.border;
        rng.setBorder(b[0], b[1], b[2], b[3], b[4], b[5],
          b[6] || '#000000',
          SpreadsheetApp.BorderStyle[b[7] || 'SOLID']);
      }
      return { formatted: a.range };

    case 'note':
      sh = sheetOf(ss, a.tab);
      sh.getRange(a.range).setNote(a.text || '');
      return { noted: a.range };

    case 'validation':
      // args: tab, range, list [..]
      sh = sheetOf(ss, a.tab);
      var rule = SpreadsheetApp.newDataValidation()
        .requireValueInList(a.list, true)
        .setAllowInvalid(a.allowInvalid !== false)
        .build();
      sh.getRange(a.range).setDataValidation(rule);
      return { validated: a.range };

    case 'clearValidation':
      sheetOf(ss, a.tab).getRange(a.range).clearDataValidations();
      return { clearedValidation: a.range };

    default:
      throw new Error('unknown action: ' + action);
  }
}
