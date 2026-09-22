---
type: agent
area: system
status: active
updated: 2026-09-22
source: manual
tags: [agent, memory]
---

# orchestrator — memory

Append-only. What this agent has learned by doing. Newest at the bottom. Facts here were verified in action, not assumed (AGENTS.md rule 6).

---

## 2026-09-22 — Interview technique that worked in Phase 3

- **Read the area note first, then ask only about the gaps.** Five to seven numbered questions per domain, each one short. Samuel answers by number and skips what he doesn't want to answer. Treat a skip as unanswered, and don't re-ask it in the same sitting.
- **Record his exact words** for anything that becomes a decision. Paraphrase only the surrounding context.
- **A consequence gets stated once, then recorded.** Examples: mentorship with no price now carries the January income line, and the book has no time slot. Don't argue it.
- Commit after each domain, not at the end. That way a usage-limit cutoff mid-session loses nothing.
## 2026-09-22 — Testing an app, and writing documents for Samuel's devs

- **An Android build can be walked end to end on this PC** with BlueStacks + its bundled `HD-Adb.exe`. It's scriptable (screenshot, UI dump, tap, type), so no computer-use is needed. Samuel has to switch ADB on himself, and he signs in himself. Steps: [[03-Areas/scripnals/sops/test-an-apk|Test an APK]].
- **Read the JS bundle's strings before clicking.** They showed the endpoints, both onboarding question sets and the speech library in seconds, and cost far less than screenshots.
- **The style Samuel wants in dev documents:** few, easy words, no worked examples, simple left-to-right diagrams with strong contrast, mock-ups of screens. He rejected a dense three-column swimlane (*"this looks complex"*) and preferred the simple boxes-and-arrows version.
- **Name the "Proposed" items separately and ask for one yes or no.** He approved all 8 at once. It kept the spec moving without re-litigating.

## 2026-09-22 — Researching for an AI product's reference library

- **Rank sources before reading them:** Samuel's own method, then the platform's own words (Instagram's creator and ranking pages), then studies, then creator frameworks. Most "algorithm 2026" blogs repeat each other with unsourced numbers. Trace a claim to the platform page or the original study before using it.
- **Instagram can't be browsed logged out, and no model here can watch a Reel.** Say so plainly. The real fix is transcripts of strong Reels from Samuel (open question 75).
- **Guides built from formulas with placeholders, not worked examples.** A model copies examples word for word, and every user's hook starts to sound the same. That is the "generic AI script" problem Samuel wants to avoid.
- **Tag entries, then filter with one rule.** It kept 66 entries under a 3,200-word budget per call, with no search engine. A script that simulates a request (`--select`) proves the budget before the devs build anything.
- **In chat, never cite an open-question number on its own.** Samuel asked *"what questions are those"*. Name the question in plain words; the number belongs in `open-questions.md` only.
- **Don't add inputs the user has to fill.** He cut the niche question and the format picker to keep the app simple. Infer from what the app already has (the ICP answers, the draft) before proposing a new field.
- **AI reference text is paid for on every call.** Write it terse from the start: no repeats of rules the system prompt already holds, one-line patterns, word caps in the build script.

## 2026-09-22 — Commands on Samuel's PC

- **Run local steps myself.** Twice a PowerShell command I gave him failed or looked broken, and he asked *"why am I always having issues running the code you tell me to run in powershell?"* Both were my faults. A command that moves or stores a secret without printing it is just as safe when I run it with my own PowerShell tool. Leave him only what needs his hands: clicks in a website, downloads, sign-ins.
- **Don't assume where a download landed.** Chrome saves to the last folder used. The Google key went to `Documents\Personal`, not Downloads. Search by name first.
- **`[Environment]::SetEnvironmentVariable(..., 'User')` looks like a freeze** (it notifies every window). Use `Set-ItemProperty HKCU:\Environment`.
- Moving a file outside the Brain needs his yes each time (AGENTS.md rule 5). He gave it for the key move.

## 2026-09-22 — git push is blocked in auto mode

- Claude Code's auto mode classifier blocked `git push` twice (once bundled with cd and pipes, once as a bare `git push`), even though `.claude/settings.json` allows `Bash(git push:*)`. The project rule is not enough on its own. Samuel asked how to make pushing automatic; the permission change is his to make. Until it's fixed: commit, then tell him to run `git push`. Don't retry a blocked push.

Back to [[07-Agents/orchestrator/profile|Profile]]
