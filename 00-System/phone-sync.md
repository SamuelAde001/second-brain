---
type: sop
area: system
status: active
updated: 2026-10-24
source: manual
tags: [phone, sync, obsidian, git]
---

# Phone sync: the Brain in Obsidian on Android

How the Brain gets onto Samuel's phone and back. Decided 2026-09-20 ([[00-System/decisions-2026-09-20-to-22|decision]]: GitHub is the spine, the Obsidian Git plugin on Android, token in the plugin only). Steps written 2026-10-18; **not installed until Samuel does steps 1-9**. Part of [[00-System/portability|portability]].

## How it works

- The phone holds a full git copy of `SamuelAde001/second-brain` and pulls and pushes `main` through the **Git** community plugin (Vinzent03's *Obsidian Git*).
- The phone uses its **own Obsidian settings folder, `.obsidian-mobile/`**, which is never committed. So the phone's layout, plugins and the GitHub token never reach the PC, and the PC's `.obsidian/` never fights the phone's.
- PC sessions pick up phone commits at start (the SessionStart hook fast-forwards `main`). Cloud sessions merge `origin/main` before every push. Nothing here needs an AI.

## The PC side (since 2026-10-24)

- Windows task **"Brain - git sync"** runs `00-System/scripts/pc_git_sync.py` every 10 minutes while Samuel is logged in (hidden, no window). It pulls phone and cloud commits into the PC's `main` (fast-forward, or a normal merge, never rebase or force) and pushes PC commits to GitHub. So whatever an agent commits reaches the phone within about 10 minutes, and phone notes land on the PC without a session.
- It never commits. Uncommitted edits (an agent mid-job, Samuel typing in Obsidian on the PC) reach the phone once the next session commits them (AGENTS.md §12).
- A pull that conflicts is aborted and left for the next session to show Samuel. Log: `%LOCALAPPDATA%\Brain\git-sync.log` (only runs that did something or failed).
- Needs the PC on. With the PC off, the phone still has its last copy and still pushes; the PC catches up when it's back.

## One-time setup on the phone (Samuel, ~15 minutes, on Wi-Fi)

1. **Make a GitHub token.** github.com → Settings → Developer settings → Personal access tokens → *Fine-grained tokens* → Generate. Repository access: **only `second-brain`**. Permissions: **Contents: Read and write** (Metadata read-only comes with it). Expiry: 1 year. Copy it once. It goes only into the plugin (step 5), never into a note, a chat or the repo (AGENTS.md §6).
2. **New empty vault.** Obsidian → Create new vault → name `Second brain` → store on the device (not in a cloud folder).
3. **Own settings folder.** Settings → Files and links → *Override config folder* → `.obsidian-mobile`. Restart Obsidian.
4. **Install the plugin.** Settings → Community plugins → turn on → Browse → **Git** (by Vinzent03) → Install → Enable.
5. **Log in.** Settings → Git → *Authentication*: Username `SamuelAde001`, Password/Personal access token = the token. *Commit author*: name `Samuel`, email `repzysam@gmail.com`.
6. **Clone.** Command palette (swipe down or the `>` button) → *Git: Clone an existing remote repo* → URL `https://github.com/SamuelAde001/second-brain.git` → directory: leave empty (vault root) → depth: leave empty (full copy; the Brain is small) → wait, then restart Obsidian when it asks.
7. **Plugin settings** (Settings → Git):
   - *Pull on startup*: on.
   - *Auto commit-and-sync interval*: `10` minutes. *Auto commit-and-sync after stopping file edits*: on.
   - *Sync method*: **Merge** (never rebase, AGENTS.md rule 4).
   - *Commit message on auto commit-and-sync*: `Samuel (Obsidian phone): {{date}}`.
   - *Push on commit-and-sync*: on.
8. **New notes into the inbox.** Settings → Files and links → *Default location for new notes* → `01-Inbox`.
9. **Check it.** Make a note `01-Inbox/phone-test.md`, run *Git: Commit-and-sync*. It should show in GitHub within a minute and on the PC at the next session.

## Daily use

- Open Obsidian: it pulls. Write: it commits and pushes 10 minutes after you stop typing. Before closing the app after a real edit, run *Git: Commit-and-sync* by hand so nothing waits on the phone.
- New captures go in `01-Inbox/` (AGENTS.md rule 8). The next PC or cloud session files them.
- A cloud session from the phone (Claude app → Code) and Obsidian on the phone are two separate copies. Sync Obsidian first, then start the cloud session, or its clone won't have what you just wrote.

## When something breaks

- **"Merge conflict" in the plugin, or a file with `<<<<<<<` in it:** stop editing that file. The next PC session shows it to Samuel; nothing is auto-merged (AGENTS.md rule 8).
- **Push refused, 401/403:** the token expired or lacks Contents write. Make a new one (step 1), paste it in step 5.
- **Slow or stuck sync:** the plugin's mobile git is slow by nature. On Wi-Fi, run *Git: Pull* then *Git: Commit-and-sync* by hand. If it keeps failing, Syncthing is the fallback in the 2026-09-20 decision.
- **Lost the phone:** revoke the token on GitHub straight away. That's the only secret on the device.

Back to [[00-System/portability|Portability]]
