---
type: knowledge
area: scripnals
status: active
updated: 2026-09-22
source: manual
tags: [bugs, dev-handover]
---

# Bug list for the devs

The direct message Samuel sends the devs, built from the walkthrough of the 2026-09-22 APK ([[03-Areas/scripnals/current-build|Current build]]).

**Status:** drafted 2026-09-22. Samuel is sending it as a direct message. It isn't confirmed sent. **Update this note first**, then re-send, whenever a bug is fixed or found.

**Not in the list, because Samuel already sent it in the group on 2026-09-22** ([[03-Areas/scripnals/scripnals-log|Log]]): the new logo, the waveform, transcript auto-scroll, the 3-2-1 countdown, the edit page reusing the Scripting page, the empty space on the home screen, and a forced re-login after an update.

## The message, ready to paste (WhatsApp formatting)

```text
*Scripnals: bugs from testing today's APK (2026-09-22)*

*Fix before any tester sees the app*

1. *App ID.* It's still com.ayomiplenty.highSignals. Once we put it on the Play Store it can never change, and it shows in the store link. Change it to a Scripnals ID before the first upload. Also tell me which accounts own the Expo/EAS project and the Firebase/Google Cloud project.

2. *Version numbers.* Every build since May says version 1.0.0, code 2. Raise the version code by 1 on every build. Use 0.2.0 for this release, 0.2.1 for a bug fix, 0.3.0 for new features.

3. *Voice recorder hangs.* On a phone without Google's speech service it sits on "Listening…" forever with no error. Add a timeout and an error message. Also handle when the user says no to mic access.

4. *Render.* Is the backend on the free plan? If yes, it sleeps, and the first request takes 30–60 seconds. Testers will think the app is broken.

*Bugs*

5. Onboarding can be skipped. Press the phone's Back button on question 1 and it goes to the welcome screen. Open the app again and you're on the dashboard with no ICP.

6. The last onboarding question says "optional", but "Complete Setup" stays grey until you type something. Only Skip works.

7. Business path: question 2 ("Describe your dream client") and question 6 ("Demographics of your dream client") ask the same thing. Merge them or reword one.

8. Content list: when I change a post's stage from the dropdown, the card doesn't update until I refresh. The dashboard updates straight away.

9. The stage dropdown's title says "Status Update Modal". Change it to "Move to".

10. The bell on the dashboard does nothing. Hide it until notifications work.

11. A brand-new account's first visit says "Welcome back". Say "Welcome" the first time.

12. The welcome screen never shows the name Scripnals.

*AI (fixed by the new AI doc, listing so nothing is lost)*

13. The AI result shows raw ### and ** symbols, and Insert leaves a stray * behind.

14. Insert adds the AI version under the original instead of replacing it.

15. The AI tips are general. They don't use the ICP or the content type.

16. Rewrite adds points I never wrote.

17. The daily counter still showed 10/10 after a review. Check what counts.

Send me a new APK when these are in and I'll test again.
```

## Tracking

| # | Bug | Status |
|---|---|---|
| 1–4 | Must fix before testers | Open |
| 5–12 | Bugs | Open |
| 13–17 | AI, covered by [[03-Areas/scripnals/ai-workflow|AI workflow]] | Open |

When the next APK arrives, re-test with [[03-Areas/scripnals/sops/test-an-apk|Test an APK]] and update the Status column.

Back to [[03-Areas/scripnals/scripnals|Scripnals]]
