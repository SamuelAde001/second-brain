---
type: knowledge
area: video-editing
status: active
updated: 2026-10-14
source: manual
tags: [resolve, project-manager, organisation]
---

# Resolve project library

How DaVinci Resolve's Project Manager (Local Database) is sorted, and where a new project goes. Sorted by the Editor on 2026-10-14 at Samuel's request: *"go through Davinci resolve project manager and help me sort everything properly"*. He approved the structure and the method the same day. 137 projects before and after; nothing deleted.

## Structure

| Folder | What lives there |
|---|---|
| `Routerise/` | Route Rise jobs **in progress**, plus `Project Template` (the job-setup template). Stays at the **root**: scripts and crash recovery open it with `OpenFolder("Routerise")` from the root ([[03-Areas/video-editing/resolve-automation-lessons\|lessons]]). |
| `Routerise/Delivered/` | Every finished Route Rise video (44 on 2026-10-14). |
| `Routerise/My babe/` | `TRIAL EDIT`. Left as it was. |
| `Clients/` | Every other client: `FK/` (Samuel's mentor; he worked for him and still edits for him sometimes, Samuel 2026-10-14), `SMS/` (a community or programme he did work for, Samuel 2026-10-14: Quotes, SMS Bootcamp), `Solar Agency Edits/` (the [AD] projects, Aug–Sep 2026), and the projects Break into tech, Jonathan Isah, TCC. |
| `HighSignals/` | HighSignals sessions, webinar, welcome message, shorts, the HighSignals edits, and `Course/Called to Edit Academy Beginners/`. |
| `Samuel Signals/` | His personal-brand projects (@SamuelSignals). `My videos/` inside it is the older personal-brand folder (late 2025 to mid 2026), kept with its subfolders. |
| `Church/` | `Sunday 29 march`. |
| `Tests & experiments/` | Test, cuts, `Compress/`. |
| `_Review to delete/` | Candidates only. Samuel decides; no agent deletes a project. On 2026-10-14: the Route Rise "(template copy - to delete)", and two projects with 0 timelines (`Claude tests`, `Samuel Signals/New Project 2`). |

Left as found: projects with no clear name (`New Project 1/2` in Solar Agency, `Untitled Project 1` in HighSignals, `New Project 1` in Samuel Signals and My videos), because their folder is the only clue to what they are. The empty `Samuel Signals/My videos/HighSignals` folder is still there.

## Where a new project goes

- **New Route Rise job:** `Routerise/`. When it's delivered, move it to `Routerise/Delivered/` ([[03-Areas/video-editing/sops/end-of-job-review|end-of-job review]] step 5).
- **Other client:** `Clients/<client>/`.
- **Personal brand:** `Samuel Signals/`. **HighSignals:** `HighSignals/`.
- **A test:** `Tests & experiments/`.

## Moving projects

The scripting API (21.1) has no move-project call. Move them in the Project Manager GUI: select, **Ctrl+X**, open the target folder, **Ctrl+V**. Ctrl+X and Ctrl+V also work on folders. Details: [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]].

Back to [[03-Areas/video-editing/video-editing|Video editing]]
