# Google Sheets bridge

Lets Claude Code read and write **My Claude Budget** directly, so budgeting and
logging happen in conversation and the sheet updates itself.

Sheet: https://docs.google.com/spreadsheets/d/1BrM8jAJC8Wuqm6WWZnu9jocdeNfxr4rYngapAXTXWMI/edit

## Why a web app and not the Sheets API

The Google Drive connector Claude has can *read* a spreadsheet but cannot write a
single cell. The Sheets API proper needs a Google Cloud project, an OAuth consent
screen and a credentials file. An Apps Script bound to the sheet needs none of
that: it lives inside the sheet Samuel already owns, and it is one paste and one
deploy, once, forever.

## Setup — done once, ~4 minutes

1. Open the sheet.
2. **Extensions → Apps Script.**
3. Delete whatever is in `Code.gs` and paste. Save (Ctrl+S).

   Get the script onto the clipboard with the real token already substituted in —
   the committed `Code.gs` carries a `__SHEETS_TOKEN__` placeholder so the secret
   never enters git history:

   ```powershell
   python tools/sheets/sheets.py script | Set-Clipboard
   ```

4. **Deploy → New deployment.** Gear icon → **Web app**.
   - Description: `engine bridge`
   - Execute as: **Me (repzysam@gmail.com)**
   - Who has access: **Anyone**
5. **Deploy.** Google asks to authorise — Review permissions → pick the account →
   "Google hasn't verified this app" → **Advanced → Go to (project name)** →
   **Allow**. That warning is normal: the unverified app is the script Samuel just
   wrote himself.
6. Copy the **Web app URL** (ends in `/exec`) and give it to Claude Code.

Claude then writes `.env` at the repo root:

```
SHEETS_WEBAPP_URL=https://script.google.com/macros/s/AKfy.../exec
SHEETS_TOKEN=<the shared secret Claude generates - real value lives only in .env>
SHEETS_ID=1BrM8jAJC8Wuqm6WWZnu9jocdeNfxr4rYngapAXTXWMI
```

`.env` is gitignored. It never gets committed.

Verify:

```bash
python tools/sheets/sheets.py ping
```

## If the script ever changes

Editing `Code.gs` in the Apps Script editor is not enough — **Deploy → Manage
deployments → edit (pencil) → Version: New version → Deploy.** The `/exec` URL
stays the same. But the script is deliberately generic, so this should never be
needed: the budget gets redesigned through `ops`, not through new script code.

## Security, plainly

"Who has access: Anyone" means anyone who has the URL can POST to it. The `TOKEN`
in the script is what actually stops them — requests without it are rejected. So:
the web app URL and the token are a password. Do not paste them into a chat, an
issue, or a screenshot. If either leaks, change `TOKEN` in the script, redeploy a
new version, and update `.env`.

The script can only touch this one spreadsheet. It has no access to the rest of
Drive, Gmail, or anything else.

## Using it

`ops` is the real interface — a JSON list of operations run in order, in one
request:

```bash
python tools/sheets/sheets.py ops payload.json
```

```json
{"ops": [
  {"action": "ensureSheet", "args": {"tab": "Details"}},
  {"action": "write", "args": {"tab": "Details", "cell": "A1",
    "values": [["Category", "Item", "Amount"]]}},
  {"action": "format", "args": {"tab": "Details", "range": "A1:C1",
    "bold": true, "background": "#1f2937", "fontColor": "#ffffff"}}
]}
```

Actions: `ping` `read` `readRaw` `readFormulas` `find` `write` `append`
`setFormulas` `clear` `ensureSheet` `deleteSheet` `renameSheet` `insertRows`
`deleteRows` `insertColumns` `setColumnWidth` `setRowHeight` `freeze` `format`
`note` `validation` `clearValidation`.

## Cloud and phone — making the bridge work from everywhere

A cloud session (a scheduled routine, or claude.ai/code on the phone) clones the
repo. `.env` is gitignored, so it is not in the clone. That is blocker one.
Blocker two is quieter: cloud environments only allow outbound traffic to an
allowlist, and the **Trusted** default list does not contain Google Apps Script.
The `/exec` URL also 302s to `script.googleusercontent.com`, so both hosts have
to be allowed or the POST dies at the redirect.

Fix both once, in the browser, on the environment the routines run in. There is
no settings page for cloud environments and no direct URL — the editor is behind
the cloud icon:

- **From a routine (do it this way — it also shows you which environment that
  routine actually uses):** claude.ai/code/routines → click the routine → pencil
  icon (**Edit routine**) → below the **Instructions** box click the cloud icon
  showing the environment name → hover that environment → gear icon →
  **Update cloud environment**.
- **From a session:** claude.ai/code → cloud icon in the row above the message
  box → hover the environment → gear icon.

In that dialog:

**1. Network access -> Custom**, with *"also include default list of common
package managers"* ticked. Allowed domains:

```
script.google.com
*.googleusercontent.com
```

**2. Environment variables** — the same three values as `.env`. Print them
without them passing through a chat window:

```powershell
python tools/sheets/sheets.py env > "$env:TEMP\sheets-env.txt"; notepad "$env:TEMP\sheets-env.txt"
```

Paste, save the environment, then delete that file.

Routines use the same environments as interactive cloud sessions, so this fixes
the scheduled brief, midday and reckoning at the same time. Sessions already
running keep the values they started with — start a new one to test.

Then, from a cloud session:

```bash
python tools/sheets/sheets.py doctor
```

`doctor` names the broken link rather than making you guess: no credentials,
blocked network, wrong token, or OK.

### Env vars are not a secrets store

Cloud environment variables are visible to anyone who uses that environment. On
a personal account that is only Samuel. Do not put these values in a shared or
organisation environment. If the token ever leaks: change `TOKEN` in the Apps
Script, **Deploy -> Manage deployments -> New version**, update `.env`, update
the cloud environment.

## The queue — the sheet catches up by itself

The environment config above is the fix. The queue is what makes the promise
hold anyway on the day something breaks: a bad deploy, an expired environment,
a phone session in an environment nobody configured.

Any check-in that mirrors money sends its batch with a label:

```bash
python tools/sheets/sheets.py ops payload.json --queue "reckoning 2026-08-27"
```

If the bridge is reachable, it writes and that is the end of it. If it is not,
the batch is parked in `context/sheet-queue.jsonl` — committed like everything
else in `context/`, so it travels with the repo — and the next session anywhere
that *can* reach the bridge replays it:

```bash
python tools/sheets/sheets.py pending   # what is in the ledger but not the sheet
python tools/sheets/sheets.py flush     # send it
```

Flushed batches move to `context/sheet-queue.done.jsonl`. Nothing is deleted.

The ledger is still written first and is still the source of truth (money.md
Rule 6). The queue never excuses a missing ledger row — it only stops the mirror
falling silently behind.
