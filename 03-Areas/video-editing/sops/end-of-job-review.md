---
type: sop
area: video-editing
status: active
updated: 2026-09-28
source: manual
tags: [editor, review, routerise]
---

# End-of-job review

**Owner:** Editor. **When:** the day a job is delivered, right after the row in [[03-Areas/video-editing/delivered-projects|delivered projects]]. About 15 minutes. Samuel's yes, 2026-09-28, after he decided the pipeline stays as SOPs, scripts and small skills while it still changes ([[00-System/decisions|decision]]).

It exists to do three things: keep one copy of every rule, keep tested scripts apart from one-offs, and show whether the Editor is doing more of the editing over time (target 60–80%, [[07-Agents/video-editor/profile|profile]]).

## Steps

1. **What Samuel fixed.** In the job's project note (`04-Projects/`), add a section `## End-of-job review` with one line per fix: the step (setup, cut, sectioning, transcript, visuals, Fusion, render), what the Editor handed over, what Samuel changed, his words where he gave them. Then one count line: `Fixes: N (setup a · cut b · visuals c · Fusion d · other e)`. From the job's log and his messages only; nothing guessed.
2. **Fold each new rule into one place.** For every fix that became a rule, find where it belongs: the step's SOP ([[routerise-job-setup]], [[routerise-cut-workflow]], [[visual-sheet-pipeline]]), [[03-Areas/video-editing/ways-of-working|ways of working]] for Samuel's preferences, or [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] for API and crash know-how. Write it there once. Search the other places for an older version (a script, not by reading them) and replace it with a link. Rules in the append-only memory and logs stay; add a line pointing to the new home.
3. **Sort the scripts the job made.** A script that worked and will be used again gets a row in the [[00-System/systems-register|systems register]] (scripts table). A one-off moves to `03-Areas/video-editing/scripts/jobs/<job-slug>/`. Nothing is deleted.
4. **Did any task run the same way again?** For each step, note in the project note whether it ran unchanged from the last job. Update the step's **Runs** line in its SOP. A task that ran the same way three times in a row is a candidate for a small skill: propose it to Samuel, build only on his yes (the ladder in the systems register).
5. **Log and commit.** One line in the [[07-Agents/video-editor/log|Editor log]] with the fix count, then commit and push.

## Reading the trend

The fix counts across jobs are the Editor's scorecard. Fewer fixes in a step means that step is settling; the same fix twice means the rule from step 2 didn't land where the Editor reads it.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
