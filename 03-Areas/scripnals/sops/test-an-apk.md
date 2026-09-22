---
type: sop
area: scripnals
status: active
updated: 2026-09-22
source: manual
tags: [sop, testing, apk, bluestacks, adb]
---

# SOP: test a Scripnals APK on this PC

**Trigger:** the devs send a new APK.
**Owner:** Samuel + the main session.
**Time it takes:** about 30 minutes for a full walkthrough.
**Last used:** 2026-09-22.

## Inputs

- The APK, saved under `Desktop/HighSignals/HighSignals App/` (the latest went in `LATEST/`).
- BlueStacks 5 (`C:\Program Files\BlueStacks_nxt\`, instance `Pie64`, Android 9).
- **ADB turned on in BlueStacks.** Samuel flips this himself: Settings → Advanced → Android Debug Bridge → On. With it off, installs fail with `error: closed`.

## Steps

1. **Read the version:** `HD-Aapt.exe dump badging "<apk>"`. Note the package, `versionCode` and `versionName`. Compare them with the last build in [[03-Areas/scripnals/current-build|Current build]].
2. **Start BlueStacks:** `HD-Player.exe --instance Pie64`.
3. **Connect and install:**
   - `HD-Adb.exe connect 127.0.0.1:5555`
   - `HD-Adb.exe -s 127.0.0.1:5555 install -r -g "<apk>"`
   - `HD-Adb.exe -s 127.0.0.1:5555 shell monkey -p com.ayomiplenty.highSignals -c android.intent.category.LAUNCHER 1`. Change the package once the devs rename it.
4. **Sign-in is Samuel's step.** The AI never creates accounts or types passwords. He signs up a test account in the BlueStacks window.
5. **Walk every screen:**
   - Screenshot: `shell screencap` → pull the file, or `exec-out screencap -p > file.png`.
   - Visible text and tap targets: `shell uiautomator dump /sdcard/ui.xml` then `shell cat /sdcard/ui.xml`.
   - Tap: `shell input tap X Y` (the screen is 1080 × 1920, portrait).
   - Type: `shell input text "words%swith%sspaces"`.
   - Fill onboarding and drafts with **made-up test data only**.
6. **Read what's in the build without clicking:** unzip `assets/index.android.bundle` and `assets/app.config` from the APK. Pull printable strings with a script, then grep for `api/`, question text and UI copy. `app.config` holds the Expo config. **Mask any key** before quoting it.
7. **Test voice on Samuel's real phone,** not BlueStacks.
8. **Write it up:** update [[03-Areas/scripnals/current-build|Current build]] and [[03-Areas/scripnals/dev-bug-list|Bug list for the devs]], add a line to [[03-Areas/scripnals/scripnals-log|Log]], and commit.

## Done when

Every tab and every AI action has been tried, each finding is in Current build, and the bug list statuses are updated.

## Failure modes

- `error: closed` on install or shell → ADB is off in BlueStacks. Ask Samuel to turn it on.
- `uiautomator` says "could not get idle state" and returns the old screen → animations are running. Use a screenshot instead.
- **Never send `keyevent 111` (Escape).** The app treats it as Back and leaves onboarding.
- The voice recorder hangs on "Listening…" in BlueStacks, which has no Google speech service. That's expected there, so it proves nothing about real phones.
- A slow first AI call → the Render backend may be waking up. Retry once before calling it a bug.

## Notes

A PowerShell helper that screenshots and dumps the screen in one go was used on 2026-09-22. It was a throwaway script; the commands above are all it did.

Back to [[03-Areas/scripnals/scripnals|Scripnals]]
