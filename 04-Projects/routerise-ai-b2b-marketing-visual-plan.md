---
type: project
area: video-editing
status: active
updated: 2026-10-07
source: manual
tags: [client, routerise, long-form, visual-plan]
---

# Visual plan — "The Most Valuable AI B2B Marketing Training You'll Ever Watch"

Editor, 2026-10-07 (night of 10-06). Part of [[04-Projects/routerise-ai-b2b-marketing|the job note]]. Back to [[03-Areas/video-editing/video-editing|Video editing]].

**Cut it is built on:** *Cut v5 (Editor) - sections* as Samuel approved it on 2026-10-06 (his trims included): **29,990 frames, 20:50.7, 375 clips**, section clip colours kept, section markers removed by him. Every frame number below is a timeline frame at 23.976 fps on that timeline. Word timings come from the Whisper word map re-projected onto the approved clips (4,760 words, 379 sentences; `Docs\Editor working files (2026-10-06)\words_v5.json`, `sents_v5.txt`).

Alex's script and on-screen plan: `Docs\B2B-Marketing-Masterclass_Script.docx`. No screen recording exists for this job; every demo is built.

## 0. What governs this plan

Read before building: [[03-Areas/video-editing/ways-of-working|ways of working]], [[07-Agents/video-editor/memory|Editor memory]] (2026-09-30 onwards), [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]], [[03-Areas/video-editing/motion-gallery/motion-gallery|motion gallery]]. The rules that decide most of what's below:

1. **Show, don't tell.** Anything Alex describes being *done* (filtering, warming inboxes, sorting replies, uploading a list, writing an email, grading a list) is a full-screen UI demo built from scratch to look like the real product, with my own scripted cursor, unhurried. Pills and cards carry nouns, lists and numbers only.
2. **Real UI looks real.** Each demo is measured off a real screenshot of the product (vendor site or Google Images, links in §6), rebuilt as a full-screen HTML page, rendered at the exact frame count. No Alex bubble on demos. Zoom and highlight live on a base clip *above* the demo: Brightness Contrast darkening the rest, eased zoom ≤ 1.3, a move takes ~18 frames, holds between moves.
3. **Motion graphics are editable Fusion comps**, on BGORANGE (full frame) or over the A-roll (preferred by Samuel, not too big, no small text). Every element in and out with Neo Anim (Expo, slide + blur, ~16–25 f in), one Neo Anim per element group, no bounces, no Transform pops. Static NeoLightSweep on every card, Neo Glow on borders/rings/lines, DropShadow node, one moving shine after a card lands. Geist only, ALL CAPS, two-tone titles (white + orange). Icons: Flaticon solid icons masking a Background node + light sweep. Real logos only.
4. **Mix the fills, keep the ground.** Neighbouring visuals never share a fill: solid orange, white paper, light orange/cream, graphite, grey glass (sparingly), outline. Glass and dashed lines not overused; plain Polygon lines on a Background and his Arrowline are the defaults.
5. **Lists land on his words**: the item being said lit orange, earlier ones settled graphite, upcoming ones blurred (signposting). Numbers always carry unit and source (Alex's note).
6. **Timing follows the cut.** A visual starts and stops on a timeline cut; elements land on the word. Nothing faster than the viewer can read: a landing every 4–6 s inside a visual, plain A-roll breathing 2–6 s between visuals, never past ~8 s. Target over the whole talk: a visual on screen ~75% of the time (TSB/#3/Apollo measure 71–81%).
7. **Node trees** follow the B04 v2 standard (main line at the bottom, a line per container, one row per repeated element, collector column over a clear canvas, every group joins the line once). Names `Type_Role`.
8. **Alex's production notes:** no client names or logos on screen (examples are generic), sales-call quotes anonymous, CTA `book.frontal.so`, "250+ B2B companies" only as written, numbers follow the script where the kept take differs (flagged in §7).
9. **The intro is Samuel's.** The hook (0:00–1:43.9) is ideated in §1 and only built if he says so.

## 0.1 Motifs that carry this video

| Motif | What it is | Where it appears |
|---|---|---|
| **The roadmap** | The seven steps as a horizontal stepper: numbered orange discs joined by a line, each with its name; done = orange with a tick, current = lit with a shine, upcoming = graphite. Also as a lower-third "STEP n · NAME" pill at every step start, with a mini strip. | Hook promise, "Seven steps", every step start, step 7's loop back to 1, recap (all ticked), last card |
| **The 90-day bar** | A horizontal bar KICKOFF → END OF Q1 with marks DAY 1 · WEEK 2 · WEEK 3 · MONTH 2 · QUARTER REVIEW, filling as the story reaches each mark. | Hook promise, after you sign (domain warm-up), step 3 (Tier 3 every quarter), step 7 (week 3, month 1, month 2, quarter review) |
| **The one list** | One account list (a CRM-style table card) at the centre, channels ADS · OUTBOUND · CONTENT as pills with Arrowlines into it. | Hook (Ivan, same list), phone books → one list, step 4 (signals rank accounts on the list), step 6 (one list on all channels), recap |
| **The tier board** | Four columns TIER 1 · TIER 2 · TIER 3 · SKIP, rows filling per tier, mixed fills per column (deep orange / light orange / graphite / outline). | Step 3, step 6 control group, step 4 "moves up" |
| **The weekly strip** | MON · TUE–THU · FRI chips with one job each. | Step 7 |
| **Ivan** | Ivan Falco's real photo (frontal.so) in a white medallion with an orange ring, name tag IVAN FALCO · HEAD OF ABM. | Hook mention, step 3 quote, step 6 (lower third, budget, control group, quote) |

## 0.2 Track plan on the duplicate timeline *Visuals v1 (Editor)*

| Track | Carries |
|---|---|
| V1 | A-roll, untouched |
| V2 | Full-frame pieces: UI demo renders (ProRes), browser captures, AI B-roll, and transparent base clips carrying full-frame BGORANGE Fusion comps |
| V3 | Focus and zoom over V2 demos: base clips with `F_*` comps (Brightness Contrast + eased Transform), generated from each demo's element boxes |
| V4 | Overlays on the A-roll: transparent base clips with Fusion comps (pills, cards, lower thirds, steppers) |
| V5 | Empty, reserved for Samuel's MagicZoom V3 punch-ins on the plain A-roll stretches (§5 lists where) and any MagicMask cut-outs |
| A1 | Mic, untouched. Music per Alex: none under the voice (§7). SFX pass after the picture is approved |

Renders go to `Graphics\Visuals v1\renders\`, builders to `Graphics\Visuals v1\<section>\build_<id>.py`, HTML engines to `Graphics\Visuals v1\engines\`, captures to `Screenshots\`.

---

## 1. HOOK · 0–2491 (0:00–1:43.9) — ideas for Samuel, built only on his yes

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| H1 | 0–90 | pipeline flat for months | Over A-roll, left: a small graphite card PIPELINE with a line chart drawing on flat across JAN…JUN, Neo Glow on the line. | V4 comp: RectangleMask card, Polygon line WriteOn, Text+ |
| H2 | 97–267 | more cold email, another SDR, a new AI tool, LinkedIn ads, LinkedIn content… nothing really moved | Five medallion pills in a row along the bottom, one landing per phrase (envelope · person · sparkle · LinkedIn logo · post icon), mixed fills; on "nothing really moved" (≈240) an orange marker ✗ swipes over each. | V4 comp, P01 pills + O09 marker strokes |
| H3 | 273–461 | buyers pick a favourite before they talk to a salesperson… wins 80% | BGORANGE: three vendor cards (A · B · C, outline), a ringed buyer avatar, the orange ring snaps to one card at "favorite vendor" (≈330), a SALES CALL tag lands after; "80%" counter rolls up with WINS THE DEAL · 6sense 2025 small caption. | V2 base + comp; Number Counter macro |
| H4 | 472–715 | what we do at Frontal… 250+… we eat our own dog food | Frontal logo in a graphite capsule over his head (the Apollo P9 build, reused), then a small cream pill "250+ B2B COMPANIES" landing on "250" (≈600). | V4 comp |
| H5 | 718–911 | in 2026 it's the minimum… irrelevant outreach… barely gets a reply | **Gmail inbox demo** full frame: an irrelevant cold email opened, cursor goes to Report spam (≈850); no reply arrives. | V2 render (gmail engine) + V3 focus |
| H6 | 916–1308 | exactly what we'd do if you signed… every step in order… kickoff to end of Q1… real numbers, tools, where AI does the work | BGORANGE: two-tone title IF YOUR COMPANY / SIGNED TOMORROW; **the roadmap** (seven discs, names) lands on "every step" (≈1060); **the 90-day bar** under it on "kickoff" (≈1100); three chips REAL NUMBERS · THE TOOLS · WHERE AI DOES THE WORK on their words (1141–1244). | V2 base + comp |
| H7 | 1316–1542 | Ivan, our Head of ABM, runs ads on the exact same list as our outbound… buyers know you before the first email | Over A-roll: Ivan medallion + name tag lands on "Ivan" (≈1340); then **the one list** small at the bottom with ADS and OUTBOUND arrows into the same list (≈1400–1542). | V4 comp |
| H8 | 1546–1739 | nobody on YouTube talks about that… ads and outbound sit in two teams that never talk | BGORANGE: ADS TEAM card (white) far left, OUTBOUND TEAM card (graphite) far right, a wall line between; on "never talk" (≈1700) a broken line and a ✗ in the middle. | V2 base + comp |
| H9 | 1743–1951 | in step four, the signal mistake almost every company makes… in your outbound right now | Over A-roll: the roadmap mini strip with 4 lit and a P02 status tag hanging off it: THE SIGNAL MISTAKE (≈1790). | V4 comp |
| H10 | 1957–2236 | most valuable training… for B2B tech companies that already have a product people buy, an existing sales team, a pipeline that isn't growing | B01 checklist beside him: A PRODUCT PEOPLE BUY ✓ (2073) · A SALES TEAM ✓ (2154) · PIPELINE NOT GROWING (flat-arrow icon, 2200). | V4 comp |
| H11 | 2241–2457 | which accounts to go after, when each is ready to buy, what to send them | Three numbered pills (1 WHICH ACCOUNTS · 2 WHEN THEY'RE READY · 3 WHAT TO SEND), landing on 2241 / 2324 / 2369, lit on word. | V4 comp |
| H12 | 2462–2491 | Alright, let's get into it | Everything out with Neo Anim; A-roll. | — |

---

## 2. WHAT WE TELL EVERY NEW CLIENT · 2495–5051 (1:44–3:30.7)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| C1 | 2495–2598 | you just signed… what I tell every new client on the first call | A-roll breath; on "first call" (≈2560) a Dynamic Island rises from the bottom: calendar icon · FIRST CALL · FRONTAL × YOU, drops back out at 2598. | V4 comp (P05) |
| C2a | 2601–2849 | sales calls, same things every week… marketing lead: $15K, three months, agency, three meetings, none qualified | **Call-recording transcript UI** full frame (dark, Fireflies/Gong look, no logo): header "Discovery call · Marketing lead, B2B SaaS · 34:12", transcript lines; the quote line scrolls into view and the highlight walks it as he says it: "…spent almost $15,000 over three months… three meetings… none of them qualified". Speaker labels by role only. | V2 render (calls engine) + V3 highlight (BC, no zoom) |
| C2b | 2853–2994 | head of marketing: 50 cold email inboxes in Instantly, nobody using them | **Instantly "Email Accounts" page** full frame: 50 rows (yourco-mail.com…), Warmup ON, "Sent 0" column; the page scrolls slowly; highlight settles on the Sent 0 column at "nobody was using them" (2966). | V2 render (instantly engine) + V3 highlight |
| C2c | 2999–3102 | an AE: if the AEs are outbounding all the time, who closes the deals? | Back to the calls UI, next call "Account executive": the question line highlighted. | V2 render + V3 |
| C3 | 3111–3206 | it's getting harder, buyers make up their minds before they talk to you | A-roll (punch-in spot). | — |
| C4a | 3209–3480 | 6sense surveyed B2B buyers… first reached out at 61% of the way through | **Real 6sense Buyer Experience Report page** captured in the browser (§6), scrolled to the point-of-first-contact finding; BC highlight on the 61% line as he says "61%" (3405), zoom 1.2 over 18 f. | V2 capture + V3 focus |
| C4b | 3484–3638 | that's where the 80% comes from… won about 80% of the time | Over A-roll, right: P09 stat pill with a fill bar filling to 80%: PRE-CONTACT FAVOURITE WINS · 8 OF 10 DEALS, caption 6sense 2025. | V4 comp |
| C5 | 3643–3751 | if they don't know you before… fighting for second place | Over A-roll, bottom pair: THEIR FAVOURITE card with a FIRST corner badge, YOU card with a 2ND PLACE badge (P04), arrow between. | V4 comp |
| C6a | 3757–3810 | when you reach out it better be relevant | A-roll. | — |
| C6b | 3814–3958 | Gartner: 73% avoid suppliers who send irrelevant outreach | **Real Gartner press release** captured (§6; if the capture is blocked, the stat card alone), 73% line highlighted; then over it on "irrelevant outreach" a cream stat pill 73% ACTIVELY AVOID IRRELEVANT OUTREACH · Gartner, June 2025. | V2 capture + V3 focus; V4 pill |
| C7a | 3966–4173 | cold email alone won't carry you… 551 campaigns, median reply below 1% | **Instantly campaign analytics** full frame: campaign list with Reply rate column, a summary tile "Median reply rate 0.64% · 551 campaigns" (script number); highlight on the tile at "below 1%" (4140). | V2 render + V3 |
| C7b | 4179–4370 | a good cold email gets 10%? ask what they're counting… for us 2% is a good campaign | Over A-roll: three fill bars stacked: "10%" (grey, struck on "what they're counting", 4263), "2% · A GOOD CAMPAIGN" (orange, lands 4296), "0.64% · MEDIAN" (light orange). | V4 comp |
| C8 | 4372–4487 | biggest problem: every channel on its own… an analogy | A-roll. | — |
| C9 | 4495–4711 | your ads team, your outbound team, your content team each have a different phone book… calling different people, nobody knows who picked up | BGORANGE: three columns land on their words (ADS TEAM white · OUTBOUND TEAM deep orange · CONTENT TEAM graphite), each with a Flaticon phone-book icon and three ringed avatar dots under it (different people); on "nobody knows who already picked up" the dots blink in different places. | V2 base + comp (one scene with C10) |
| C10 | 4716–5051 | everything starts from one list of accounts in your CRM… that's ABM, account-based marketing… pick the accounts first, every channel works on them together | Same scene continues: the three phone books slide into one **one-list** card at the centre (CRM table rows); two-tone title ACCOUNT-BASED / MARKETING lands on 4830; on "pick the accounts first" (4959) the list shines; on "every channel" (5004) the three team pills reattach with Arrowlines into the list and light in turn. Out on the cut at 5051. | same comp |

## 3. WHAT HAPPENS AFTER YOU SIGN · 5057–5854 (3:30.9–4:04.2)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| A1 | 5057–5192 | exactly what happens after you sign, in the order we do it… seven steps | BGORANGE: title AFTER YOU SIGN; **the roadmap** lands on "Seven steps" (5178): seven discs pop left→right 4 f apart with names 1 CLOSED-WON DEALS · 2 MAP THE MARKET · 3 TIER · 4 SIGNALS · 5 THE MESSAGE · 6 THE ADS · 7 EVERY WEEK; the 90-day bar under it. | V2 base + comp |
| A2a | 5198–5384 | before you sign we check fit… B2B tech, real demand, a real sales process | Over A-roll, left: B01 checklist GOOD FIT: B2B TECH ✓ · REAL DEMAND ✓ · A SALES PROCESS ✓ landing on words. | V4 comp |
| A2b | 5388–5504 | we're the fuel you pour on the fire… you need a fire | Over A-roll, right: a Flaticon flame icon (orange, Neo Glow) with YOU under it; a FUEL canister medallion tips toward it on "fuel" (5420); on "need a fire" (5480) the flame pulses. Small. | V4 comp |
| A3a | 5511–5656 | day one: separate domains and inboxes, warming up… never from your main domain | **Instantly Email Accounts demo**: cursor adds accounts (yourco-mail.com, yourco-hq.com, getyourco.com), Warmup toggles switch on one by one, status "Warming · day 1". | V2 render + V3 |
| A3b | 5662–5759 | Google and Microsoft started rejecting bulk senders | **Google's "Email sender guidelines" page** captured (§6), the bulk-sender requirements highlighted. | V2 capture + V3 |
| A3c | 5766–5854 | warm-up takes two weeks, runs while we build everything else | Over A-roll: **the 90-day bar** with DAY 1 → WEEK 2 segment filling, label DOMAINS WARMING, a small BUILD chip running alongside. | V4 comp |

## 4. STEP 1 · 5857–8001 (4:04.3–5:33.7)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| S1-0 | 5857–5980 | step one, closed-won deals in your CRM | Lower third: STEP 1 pill + START FROM YOUR CLOSED-WON DEALS, mini roadmap strip with 1 lit. Stays to 5980. | V4 comp (stepper kit) |
| S1-1 | 5895–6061 | closed-won deals already in your CRM… founders have a dream ICP in their head | **CRM deals demo** (HubSpot-style board, full frame): filter Closed won applied, won deals list with amount and contact; on "dream ICP in their head" (5986) cut to A-roll with a small thought-bubble box over Alex: DREAM ICP with a target icon (his thought-bubble rule: text + icons, small). | V2 render + V3 ; V4 comp |
| S1-2 | 6066–6188 | honest reality check… who actually paid you money | Back to the CRM list: sorted by Close date, Amount column highlighted. | V2 render + V3 |
| S1-3 | 6195–6750 | CRM access, last 40–50 closed-won deals, the people who signed… best customers + criteria… 10 dream accounts → 100–200 lookalikes… do-not-contact list… recordings of deals won and lost | Beside him, left: **WHAT WE ASK FOR** checklist (upcoming rows blurred): CRM ACCESS (6195) · LAST 40–50 CLOSED-WON DEALS (6250) · THE PEOPLE WHO SIGNED (6303) · (OR: BEST CUSTOMERS + YOUR CRITERIA, 6331) · 10 DREAM ACCOUNTS (6466) with a tag → 100–200 LOOKALIKES (6552) · DO-NOT-CONTACT LIST (6620) · CALL RECORDINGS · WON + LOST (6680). Mixed row fills. | V4 comp |
| S1-4 | 6757–6975 | by the kickoff an AI agent drafted a first ICP matrix from your website… kickoff call, we correct it together | **ICP matrix demo**: a Notion-style page "ICP matrix · draft by agent · EXAMPLE" where rows type in (Segment · Size · Industry · Must-have · Trigger) from "yourcompany.com"; on "correct it together" (6916) a cell is edited and a comment "Kickoff: change to 10+ entities" appears. | V2 render (notion engine) + V3 |
| S1-5 | 6980–7101 | the one thing that if missing means they'll never buy | Over A-roll: one outline card THE ONE THING with a key icon; IF IT'S MISSING → NEVER BUYS lands on 7050. | V4 comp |
| S1-6 | 7109–7453 | cash management client: legal entities, 1 = never, 10+ = top… another: monthly ad spend > $500K… higher-ed: student enrollment | BGORANGE: three cards land on their words (7109 / 7330 / 7400), mixed fills: LEGAL ENTITIES with a mini scale 1 ✗ NEVER BUYS → 10+ ✓ TOP OF THE LIST (7208–7275); MONTHLY AD SPEND · > $500K; STUDENT ENROLLMENT. Generic icons, no client names. | V2 base + comp |
| S1-7 | 7459–7539 | the criteria that define the list | A-roll (punch-in). | — |
| S1-8 | 7543–7722 | teams skip this and go straight to filters in a database… same size, industry, country | **Database filter demo** (Apollo-style Find companies, our own apollo engine): cursor sets Employees 51–200 → Industry Software → Country United States, the list refreshes; two rows with identical facts. | V2 render + V3 |
| S1-9 | 7730–8001 | can be completely different buyers… one just hired first salespeople, no pipeline… the other has a team and process… same message? | Over A-roll: two company cards from left and right (COMPANY A white, COMPANY B graphite) with the same three rows; A grows tags JUST HIRED FIRST SALESPEOPLE · NO PIPELINE (7778) while B dims; B grows A TEAM IN PLACE · PROCESS THAT WORKS (7878) while A dims; on "same message" (7960) one envelope between them gets a ✗. Out on 8001. | V4 comp (the Apollo VC build as the starting template, fills changed) |

## 5. STEP 2 · 8003–9700 (5:33.8–6:44.6)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| S2-0 | 8003–8079 | step 2, map your market, cut it down | Lower third STEP 2 · MAP THE MARKET, THEN CUT IT, strip with 2 lit. | V4 comp |
| S2-1 | 8081–8192 | pull companies from several data sources, no single database has everyone | Over A-roll, bottom: five medallion pills with real logos (Apollo · Clay · LinkedIn · Crunchbase · AI Ark) landing 4 f apart, Arrowlines from each into one MARKET list chip at the centre. | V4 comp |
| S2-2 | 8196–8441 | clients go quiet… thought their market was 50,000… cut down, 17,000 fit | BGORANGE: C03 counter card: big "50,000" with a THEY THOUGHT tag (8300), a hand-drawn arrow, the Number Counter drops to "17,000" with ACTUALLY FIT in orange (8400), a bar beside it shrinking from full to a third. | V2 base + comp |
| S2-3 | 8448–8630 | AI reads every company, accept or reject, writes the reason… Clay and Claude | **Clay table demo** full frame: columns Company · Website · Verdict · Reason; rows fill ACCEPT / REJECT chips with reasons typing ("No sales team yet", "Agency, 12 staff", "Sales team of 8, hiring SDRs"); the Verdict column header carries the Claude mark ("Claude · Decide fit"); highlight on the column header at "Clay and Claude" (8596). | V2 render (clay engine) + V3 |
| S2-4 | 8637–8785 | a person reads a sample of the rejects… change the rules, run it again | Same table: filter Reject, a reviewer comment on one row "Actually a fit", the prompt cell edited (rule added), Run again → that row flips to ACCEPT. | V2 render + V3 |
| S2-5 | 8789–9081 | my rule is 10-80-10… person decides the task, AI does 80%, a person checks the last 10%… AI leverage with human judgment | BGORANGE: a segmented bar 10 · 80 · 10 fills left to right on his words (8850 / 8916 / 9000) with icons above (person · sparkle · check) and labels PERSON DEFINES · AI DOES THE WORK · PERSON CHECKS; two-tone caption AI LEVERAGE / HUMAN JUDGMENT lands on 9045. | V2 base + comp (P09 bar) |
| S2-6 | 9091–9285 | find the people, 2–3 decision-makers per account: the buyer and the user | Over A-roll: an account card with two ringed avatar medallions popping on their words: SIGNS (9188) · USES (9240), a third faded. | V4 comp |
| S2-7 | 9293–9379 | only use an email if the verification tool says deliverable | **Email verification demo** (LeadMagic-style list): emails with status chips Deliverable ✓ / Risky / Invalid ✗, cursor filters to Deliverable only. | V2 render + V3 |
| S2-8 | 9383–9497 | grade the list, someone checks 10 random rows by hand | **Google Sheets demo**: a graded list (Grade A/B/C column), a Checked column where 10 random rows get ticks one by one (0.3 s per row). | V2 render (sheets engine) + V3 |
| S2-9 | 9506–9700 | test on 25 before automating 5,000… 100 messages, zero answers → 10,000 won't work | Over A-roll, C06 pair: TEST ON 25 (orange, 9506) → AUTOMATE 5,000 (graphite, 9560); then swap to 100 SENT · 0 REPLIES ✗ (9592) and 10,000 SENT struck through (9650). | V4 comp |

## 6. STEP 3 · 9703–12888 (6:44.7–8:57.5)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| S3-0 | 9703–9742 | step three, tier the accounts | Lower third STEP 3 · TIER THE ACCOUNTS, strip with 3 lit. | V4 comp |
| S3-1 | 9753–9916 | even if your market was 100 companies, not all equal, can't work all 100 the same | BGORANGE: a 10 × 10 grid of small graphite company tiles pops in; on "not all equal" (9808) a few turn orange and grow, others dim. | V2 base + comp (one scene with S3-2/S3-3) |
| S3-2 | 9920–10231 | two scores: fit and timing… fit = belongs on the list; signals = when; tier = how much effort | Same scene: the tiles slide onto a 2 × 2 **fit × timing grid** (axes FIT ↑, TIMING →) on "fit and timing" (9966); labels land: FIT → ON THE LIST? (9996), SIGNALS → WHEN? (10100), TIER → HOW MUCH EFFORT? (10164). | same comp |
| S3-3 | 10235–10494 | Ivan has a simple way: high fit, buying now → one-to-one; high fit, not yet → nurture; low fit → skip | Same grid: Ivan medallion + name tag at the top-left (10235); the quadrants light with their verdicts on his words: HIGH FIT · BUYING NOW → ONE-TO-ONE (10294), HIGH FIT · NOT YET → NURTURE (10378), LOW FIT → SKIP (10440). | same comp |
| S3-4 | 10503–10534 | here's what each tier gets | BGORANGE: **the tier board** lands: four empty columns TIER 1 · TIER 2 · TIER 3 · SKIP. | V2 base + comp (board kit, carried over S3-5…S3-8) |
| S3-5a | 10537–10908 | Tier 1: best fit + dream accounts… 100 or a couple thousand… weekly shortlist where signals stack, ~20 | Board, TIER 1 column lit (deep orange): BEST FIT + DREAM ACCOUNTS (10537) · 100 → A COUPLE THOUSAND (10657) · WEEKLY SHORTLIST ~20 · SIGNALS STACKING (10741–10832). | board comp |
| S3-5b | 10917–11375 | research each one, build something useful… founder on LinkedIn by hand… team calls… ads for that one company… gift or dinner… 3–5 people, nothing automated | Over A-roll, left: THE TIER 1 PLAYBOOK rows landing on words, Flaticon icons: RESEARCH + BUILD SOMETHING USEFUL (10917) · FOUNDER ON LINKEDIN, BY HAND (11039) · YOUR TEAM CALLS (11108) · ADS FOR THAT ONE COMPANY (11141) · A GIFT OR A DINNER (11199); on 11252 three ringed avatars with 3–5 PEOPLE PER ACCOUNT and a NOTHING AUTOMATED tag. | V4 comp |
| S3-6 | 11385–11655 | Tier 2: good fit, not your best… grouped by industry or use case… segment ads, automated LinkedIn and email… a case study… watch for signals | Board, TIER 2 column lit (light orange): GOOD FIT, NOT YOUR BEST (11385) · GROUPED BY INDUSTRY / USE CASE (11415) · SEGMENT ADS + AUTOMATED LINKEDIN & EMAIL (11480) · A CASE STUDY FROM THEIR INDUSTRY (11576) · WATCH FOR SIGNALS (11618). | board comp |
| S3-7a | 11664–12026 | Tier 3: good-enough fit… the bulk, thousands of accounts… automate email… broad ads, wait for signals | Board, TIER 3 column lit (graphite): GOOD-ENOUGH FIT (11664) · THE BULK · THOUSANDS (11767) · AUTOMATED EMAIL (11851) · BROAD ADS + RETARGETING (11921) · SIGNAL → MOVES UP (12000, an arrow from Tier 3 up to Tier 2). | board comp |
| S3-7b | 12028–12232 | reach your whole Tier 3 at least once every three months… you don't lose much | Over A-roll: the 90-day bar with a TIER 3 TOUCH flag at the end of each quarter, repeating ×3. | V4 comp |
| S3-7c | 12237–12401 | AI SDR: only this tier, never Tier 1 or 2 | Board: an AI SDR medallion (robot icon) docks onto TIER 3 (12237); on "never Tier 1 or Tier 2" (12334) ✗ marks over the T1 and T2 column heads. | board comp |
| S3-7d | 12404–12471 | everyone else, we skip, nothing | Board, SKIP column (outline): EVERYONE ELSE · NOTHING SENT. | board comp |
| S3-8 | 12478–12725 | tiers decide the channel… 15–20 LinkedIn messages a day per person… LinkedIn top tiers, email handles the volume | Board gets a CHANNEL row: a LinkedIn medallion with a counter 15–20 / DAY (12555) slides under T1 and T2 (12646), an email medallion under T3 with a VOLUME tag (12700). | board comp |
| S3-9 | 12730–12888 | score ~50 companies by hand, show you the sample, you approve before anything runs | **Google Sheets demo**: "Tier scoring · sample of 50" with Fit · Timing · Tier columns filled; a comment thread "Approved ✓ — client" appears on "you approve" (12841). | V2 render + V3 |

## 7. MID-VIDEO CTA · 12894–13230 (8:57.8–9:11.8)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| M1 | 12894–12935 | quick pause before signals | A-roll. | — |
| M2 | 12942–13181 | a team to build and run this with you… that's Frontal… go-to-market partner for B2B tech… extension of your GTM team | Frontal capsule over his head (Apollo P9 reuse) on "Frontal" (13010); then **frontal.so captured live** full frame, scrolling from the hero ("Grow Revenue Without Adding Headcount") to the team section on "extension of your go-to-market team" (13120). | V4 comp; V2 capture + V3 |
| M3 | 13180–13230 | link in the description to book a call | Lower third pill book.frontal.so + LINK IN THE DESCRIPTION with the down arrow (Apollo P10 reuse). | V4 comp |

## 8. STEP 4 · 13232–18125 (9:11.9–12:36)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| S4-0 | 13232–13303 | okay, signals. Step four, wire up the signals | Lower third STEP 4 · WIRE UP THE SIGNALS, strip with 4 lit. | V4 comp |
| S4-1 | 13305–13570 | a signal tells you the right moment; what you say comes from the situation behind it; mixing those up is the biggest mistake | Over A-roll, bottom pair: SIGNAL → WHEN TO REACH OUT (clock icon, white, 13305) and SITUATION → WHAT TO SAY (speech icon, orange, 13372); on "mixing those two up" (13470) the two cross over each other with a ✗ between. | V4 comp |
| S4-2 | 13579–13727 | three kinds of signals, not equal… strongest: the ones only you can see | BGORANGE: three tiers of unequal size land top to bottom (big, medium, small), upcoming two blurred: 1 ONLY YOU CAN SEE (orange, lit 13648) · 2 PEOPLE SIGNALS · 3 MARKET SIGNALS. | V2 base + comp (scene returns at S4-7a, S4-10a) |
| S4-3 | 13733–14101 | someone from a target account visits your pricing page… engages with your ads… comments on your founder's post… a deal you lost comes back to your site, checks the proposal | **Signals feed demo** (a dark, original "Signals" page in the GTM OS look): rows arrive on his words: Acme Robotics · viewed /pricing · 2 min ago (13760) · Northwind · engaged with your LinkedIn ad (13828) · Juno Health · commented on Alex's post (13867) · Closed-lost · Mar 2026 · back on /pricing · opened proposal.pdf (13952–14101). Fictional companies. Highlight walks each row. | V2 render (signals engine) + V3 |
| S4-4 | 14105–14297 | tools like RB2B or Vector show which companies visit… Fibbler shows which accounts engage with your ads | Each tool's **real UI full frame on its mention**: RB2B dashboard (14105), Vector (14156), Fibbler (14204), from the vendors' own product screenshots (§6), no cursor, a slow 1.1 push and highlight on the company list of each. | V2 captures + V3 |
| S4-5 | 14303–14403 | on LinkedIn we track who engages with your team's posts and competitors' posts | **LinkedIn post demo**: a team member's post with the reactions list open; the list scrolls; highlight on the names' companies. | V2 render (linkedin engine) + V3 |
| S4-6 | 14407–14515 | we turn website visitors into outreach the same week | Over A-roll: a feed row chip ACME · /PRICING with an Arrowline to an envelope medallion OUTREACH · THIS WEEK. | V4 comp |
| S4-7a | 14515–14554 | the second kind is people signals | The three-tiers scene returns, 2 lit. | S4-2 comp, second shot |
| S4-7b | 14563–14770 | a past champion changed jobs… a new leader starts: new CRO, new head of marketing | **LinkedIn job-change card demo**: "Maya Lindqvist started a new position as VP Sales at Acme Robotics" (14563), then a second card "New CRO at Northwind" (14673). | V2 render + V3 |
| S4-8 | 14772–15004 | UserGems: deals with a past champion win more than twice as often… they never come back unless you reach out | **UserGems blog page** captured (§6) with "Gems more than double your win rates" highlighted (14850); then over A-roll two fill bars: WITHOUT A CHAMPION 1× · WITH A PAST CHAMPION 2× (UserGems, 5,000+ opportunities) landing on "twice" (14880). | V2 capture + V3; V4 comp |
| S4-9 | 15010–15210 | someone relevant moves into a new role → a sequence reaches them within days | **Sequence demo** (Instantly/lemlist look): "Job-change sequence" steps DAY 1 EMAIL · DAY 3 LINKEDIN · DAY 6 EMAIL, triggered by the job-change card, the first step firing on "within days" (15099). | V2 render + V3 |
| S4-10a | 15222–15264 | the third kind is market signals | Three-tiers scene, 3 lit. | S4-2 comp, third shot |
| S4-10b | 15273–15420 | hiring for roles tied to your problem… raised money… added or dropped a tool… new market | Over A-roll: four medallion pills landing on words: HIRING · RAISED MONEY · ADDED / DROPPED A TOOL · NEW MARKET, mixed fills. | V4 comp |
| S4-11 | 15440–15527 | where most people get signals wrong. One, they chase them | BGORANGE: title THE 3 SIGNAL MISTAKES; numbered cards 1 · 2 · 3 land, 1 CHASING THEM lit on 15500, 2 and 3 blurred. | V2 base + comp (returns at S4-13a, S4-14a) |
| S4-12 | 15535–15710 | only use signals to rank accounts already on your list; otherwise you email every company that raised money | BGORANGE: **the one list** card; funding badges fall onto accounts in the list and their score chips tick up (15535–15610); on "otherwise" (15607) a badge lands outside the list, greys out with a ✗ (NOT ON THE LIST). | V2 base + comp |
| S4-13a | 15715–15754 | Two, they bet on one signal | Mistakes scene, 2 lit. | S4-11 comp |
| S4-13b | 15758–16142 | overused: open jobs, fundraises… every deal we closed had at least three signals stacked… signals fade: a funding round from March vs a first SDR hire from last Tuesday | BGORANGE: an account card; OPEN JOBS and FUNDRAISE chips land grey with an OVERUSED tag (15800); then three chips stack on it 6 f apart and a score bar jumps to TIER 1 on "three signals stacked" (15914–15977); on "signals fade" (15984) a time axis appears: FUNDING ROUND · MARCH dims to 30% while FIRST SDR HIRE · LAST TUESDAY stays bright (16036–16142). | V2 base + comp |
| S4-14a | 16149–16254 | Three, the mistake I promised: putting the signal in the email | Mistakes scene, 3 lit: THE SIGNAL IN THE EMAIL. | S4-11 comp |
| S4-14b | 16259–16556 | "Congrats on the Series B", "so you're hiring SDRs"… every company that raises money gets a pile of those emails the same week | **Gmail inbox demo**: emails arrive one after another, subjects "Congrats on the Series B!" from different senders (eight of them by 16500), "Saw you're hiring SDRs" among them; the inbox count climbs. | V2 render (gmail engine) + V3 |
| S4-14c | 16559–16589 | they don't need you to remind them | Over A-roll: B08 quote card with the line CONGRATS ON THE SERIES B struck through by an orange marker stroke and a tag THE MISTAKE. | V4 comp |
| S4-15a | 16593–16804 | a round raises the account's score, never goes in the copy… write about the situation behind the signal | Over A-roll, bottom: SERIES A badge → Arrowline → SCORE chip ticking +1 (16650); a COPY chip gets a ✗ (16720); then SITUATION chip lights (16752). | V4 comp |
| S4-15b | 16812–17131 | instead of "they raised a Series A": "they promised their board a growth number, and the two founders are still the only people who've ever sold the product"… a problem they recognize | **Gmail compose demo**: the first line typed as "Congrats on the Series A" then deleted; the situation line typed in full on his words (16812–16997); highlight on it at "a problem to recognize" (17104). | V2 render + V3 |
| S4-16 | 17139–17241 | same with ads: never "I saw you clicked on our ad"… creepy | Same compose: a new line "Hey, I saw you clicked on one of our ads" typed, then an orange marker strike over it (17227) on the overlay. | V2 render; V4 marker |
| S4-17 | 17248–17572 | signals aren't magic… for one client the plain email beat the signal-based campaigns… a strong offer works without any signal | Over A-roll: two fill bars without numerals: PLAIN EMAIL (orange, longer) vs SIGNAL-BASED (graphite, shorter) on 17284–17363; on "without any signal" (17450) a small STRONG OFFER pill with a ✓. | V4 comp |
| S4-18a | 17577–17647 | before you pay for intent data, look at your own CRM | **CRM contacts demo** (HubSpot-style): the full contacts list. | V2 render + V3 |
| S4-18b | 17651–17804 | TrustRadius: 79% had heard of the product before they started researching | **TrustRadius page** captured (§6), the 79% finding highlighted; stat pill 79% ALREADY KNEW THE PRODUCT · TrustRadius 2026 over it. | V2 capture + V3; V4 pill |
| S4-18c | 17813–17918 | best signals: past champions, closed-lost deals, old customers | Back to the CRM: filter chips applied one by one on his words: PAST CHAMPIONS (17813) · CLOSED-LOST (17875) · OLD CUSTOMERS (17900), the list refreshing each time. | V2 render + V3 |
| S4-19 | 17927–18125 | a Series A company cleaned their CRM the night before the call: more than a thousand companies sitting there, nobody prospecting | CRM list filtered "Owner: unassigned · Last activity > 12 months", rows scrolling; over it a Number Counter rolling to 1,000+ COMPANIES · NOBODY WORKING THEM (18040). | V2 render; V4 counter |

## 9. STEP 5 · 18129–20680 (12:36.1–14:22.6)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| S5-0 | 18129–18194 | step 5, write the message before you build the list | Lower third STEP 5 · WRITE THE MESSAGE FIRST, strip with 5 lit. | V4 comp |
| S5-1 | 18197–18385 | outbound = right offer, right person, right moment; if any is missing it doesn't work | BGORANGE: O07 Venn, three circles land on words RIGHT OFFER (18245) · RIGHT PERSON (18290) · RIGHT MOMENT (18310), the overlap lights OUTBOUND; on "if any is missing" (18328) one circle slides away, the overlap goes out with a ✗. | V2 base + comp |
| S5-2a | 18388–18606 | before a single email, we work on the offer… write the best email for one situation… | Over A-roll: P11 flow chips: the usual order LIST → EMAIL (grey) breaks on "backwards" cue; ours lands: OFFER (18430) → EMAIL (18520) → LIST (18580), orange. | V4 comp |
| S5-2b | 18615–18743 | …then build the list of people for whom every sentence is true… backwards, but it works | **Email → list demo** (dark original screen): the email on the left, five sentences; on the right a people list where each person added gets five ticks as the sentences are checked true. | V2 render + V3 |
| S5-3a | 18749–18967 | rules: under 100 words, about their problem; offer something useful, ask if they want it: "want me to send it over?" | **Docs-style compose demo** with a live word count at the bottom (a real Docs feature): the email types to 92 words; highlight on the count at "under 100" (18791); the last line "Want me to send it over?" typed and highlighted on 18935. (Script says 100 words; Alex says characters: §7.) | V2 render + V3 |
| S5-3b | 18967–19153 | separate emails for the person who uses the product and the person who buys… same account, different conversation | **Two Gmail compose windows** side by side: To: Head of SDR (the user) and To: VP Sales (the buyer), different first lines; highlight swaps between them on "same account, different conversation" (19083). | V2 render (gmail engine) + V3 |
| S5-4 | 19163–19473 | relevance beats personalization… grandma's name and dog's name in the first line… zero interest → not replying | Over A-roll: P08 verdict pair: PERSONALIZED card (cream) showing a first line "Hi Alex, how's grandma Rosa and Max the dog?" with grandma and dog icons, gets ✗ NO REPLY on 19380; RELEVANT card (orange) gets ✓. | V4 comp |
| S5-5 | 19480–19680 | automated email: three emails, then stop… after the third nothing good comes back, unsubscribes go up | BGORANGE: sequence strip EMAIL 1 → EMAIL 2 → EMAIL 3 → STOP (stop-sign medallion, 19540); under it two Polygon lines draw on from email 3: GOOD REPLIES falling, UNSUBSCRIBES rising (19563–19680). | V2 base + comp |
| S5-6 | 19684–20016 | best campaign: our webinar… before the registration link we asked target buyers for their opinion on the topic… people love giving opinions… easier to invite | **Gmail demo**: compose "Quick question on [topic]" asking for their take (19752); the inbox then fills with three replies (19890); then a second compose with the registration link (19958). | V2 render + V3 |
| S5-7 | 20020–20344 | look at existing sales calls to learn the vocabulary buyers use… use it in your copy | The **call transcript UI** again (C2 engine), buyer phrases highlighted ("pipeline coverage", "ramp time", 20100–20290); cut to a compose where the same words type into the email (20296–20344). | V2 renders + V3 |
| S5-8 | 20351–20588 | reply with interest → your sales team the same day, research attached… follow up fast, deals stall | **Slack handoff demo**: a reply "Interested, send it over" card → a message in #sales with research.pdf attached and SAME DAY in the timestamp (20351–20484); then A-roll on "follow up fast" (punch-in). | V2 render + V3 |
| S5-9 | 20595–20680 | about a third (he says half) of positive replies become booked meetings | Over A-roll: P09 fill bar POSITIVE REPLIES → BOOKED MEETINGS filling to the script's 1 IN 3 · Frontal (§7 flag). | V4 comp |

## 10. STEP 6 · 20686–26133 (14:22.8–18:10)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| S6-0 | 20686–20792 | step six is the ads, Ivan's part, he runs ABM for clients | Lower third STEP 6 · PUT THE ADS ON THE SAME LIST (20686) with Ivan's medallion and tag IVAN FALCO · HEAD OF ABM · FRONTAL sliding in beside it on "Ivan" (20740). | V4 comp |
| S6-1 | 20800–21180 | misconception: ABM is LinkedIn ads on a tiny list… people should see you on LinkedIn, Meta, Google, emails, webinar invites… top of mind | BGORANGE: a card LINKEDIN ADS ON A TINY LIST? with a ✗ stamp (20888); then an O01 hub ring: a ringed buyer avatar at the centre, real logo medallions orbiting in on their words LinkedIn (20950) · Meta (21000) · Google (21010) · Email (21020) · Webinar (21030); on "top of mind" (21040) the ring glows. | V2 base + comp |
| S6-2 | 21187–21431 | ABM only when deals are big enough… cheap self-serve / PLG, not worth it | Over A-roll, C06 pair: BIG DEALS ✓ ABM (orange) vs SELF-SERVE · PLG ✗ (grey, 21315). | V4 comp |
| S6-3 | 21433–21597 | Ivan starts from the budget… $5K a month covers 100–200 accounts | Over A-roll: Ivan medallion small; a budget card $5K / MONTH (21481) → a strip of account tiles filling to 100–200 ACCOUNTS (21540). | V4 comp |
| S6-4a | 21603–21823 | LinkedIn first, target the exact people… upload the same account list you use for outbound, target the right titles | **LinkedIn Campaign Manager demo**: Audiences → Upload list → accounts.csv (1,250 companies) → Matched audience; then job titles added: VP Sales · Head of Marketing · CRO. | V2 render (campaign-manager engine) + V3 |
| S6-4b | 21828–21865 | one list on all the channels | Over A-roll: the one-list chip with the four channel medallions, brief. | V4 comp |
| S6-5a | 21874–22162 | most spend → thought leader ads: posts from real people, promoted only to target accounts… by the time outreach lands they know you | **LinkedIn feed demo**: a founder's post with the Promoted label and "Thought leader ad" tag, scrolling into view; highlight on the Promoted label (21949) and on the author (22000). | V2 render + V3 |
| S6-5b | 22165–22295 | LinkedIn's own data: 1.7× the click-through rate of single-image ads | **LinkedIn thought-leader-ads PDF** captured (§6), the 1.7× line highlighted; stat pill 1.7× CLICK-THROUGH RATE · LinkedIn over it. | V2 capture + V3; V4 pill |
| S6-6 | 22301–22434 | Ivan only promotes posts that already did well organically | **LinkedIn post analytics demo**: impressions and engagement chart up and to the right, cursor hits Boost post. | V2 render + V3 |
| S6-7 | 22436–22921 | split accounts by how warm they are: cold → thought leader posts; warm (engaged in the last 90 days) → customer proof, objection answers; hot (high intent, last 30 days) → case studies, direct offer | BGORANGE: the **cold / warm / hot ladder**: three rungs with a thermometer fill, each lit on its word with its chips: COLD · THOUGHT LEADER POSTS (22501) · WARM · ENGAGED IN 90 DAYS · CUSTOMER PROOF + OBJECTIONS (22600) · HOT · INTENT IN 30 DAYS · CASE STUDIES + DIRECT OFFER (22721–22836); on 22840 all three hold. | V2 base + comp |
| S6-8a | 22927–23165 | top Tier 1: one-to-one ads, one ad set per company with their name, a page built just for them | **Campaign Manager demo**: campaign group "1:1 · Acme Robotics", the ad preview reads "Built for Acme's RevOps team", the landing page tab acme.yourcompany.com opens. | V2 render + V3 |
| S6-8b | 23163–23373 | LinkedIn needs 300 people in an audience, ~$10 a day per company… 10–20 companies at a time | BGORANGE: the one-to-one maths as three cards landing on words: 300 PEOPLE · MINIMUM AUDIENCE (23200) · $10 A DAY · PER COMPANY (23260) · 10–20 COMPANIES · AT A TIME (23311). Mixed fills. | V2 base + comp |
| S6-9a | 23377–23494 | once LinkedIn works he adds Meta, retargeting first, cheaper | **Meta Ads Manager demo**: new campaign "Retargeting · engaged accounts", budget set lower than the LinkedIn one. | V2 render + V3 |
| S6-9b | 23502–23609 | founders aren't on Instagram? they are | **AI B-roll (Flow, Omni Flash)**: a startup founder in a modern office scrolling Instagram on his phone, close-up over the shoulder, cinematic, no readable text on the phone. | V2 clip |
| S6-10a | 23616–23721 | ad ideas come from questions buyers ask on sales calls | The **call transcript UI**: a buyer question highlighted ("How do you prove the ads caused pipeline?"). | V2 render + V3 |
| S6-10b | 23737–23945 | the team comes up with the idea, AI makes variations, launch ~5 ads per idea, turn off the losers fast | **Ads Manager demo**: one idea → five ad rows appear (23779–23837); then three toggles switch off (23895–23945), the winner stays on. | V2 render + V3 |
| S6-11 | 23950–24313 | when an account hits 5 clicks or 10 engagements, a salesperson reaches out and mentions what was on the ad | BGORANGE: an account card with a click counter rolling 1→5 (Number Counter, 23950–24060), a threshold line, Arrowline to a ringed SALESPERSON medallion (24150); then a small email card with the ad's topic line (24194–24313). | V2 base + comp |
| S6-12 | 24324–24753 | how do you know the ads caused the pipeline? Ivan: a control group, Tier 1 and 2 split in half, half gets ads, half doesn't, compare pipeline | BGORANGE: Ivan medallion; the tier board's T1+T2 account dots gather and split in two halves on "split them in half" (24582); ADS badge on the left half (24653), NO ADS on the right (24679); two pipeline bars rise under them on "compares pipeline" (24702–24753). | V2 base + comp |
| S6-13 | 24761–24939 | fastest way to waste an ABM budget: spread across LinkedIn, Meta and Google without tracking | Over A-roll: three logo medallions (LinkedIn · Meta · Google) with a $ bar draining into each and a ? corner badge on each (P04). | V4 comp |
| S6-14 | 24947–25144 | depending how you count, the same spend looks like a loss or a 7× return… a benchmark this year | Over A-roll, C06 pair: 0.56× (grey) vs 7.6× (orange), SAME SPEND · Metadata 2026 (§7 flag). | V4 comp |
| S6-15 | 25153–25271 | Ivan: if you judge LinkedIn ads only on demos, you'll kill ABM early | Ivan's photo (medallion, larger) with a B08 quote card beside it: "IF YOU JUDGE LINKEDIN ADS ON DEMOS, YOU'LL KILL ABM EARLY", marker highlight on KILL ABM EARLY (25240). | V4 comp |
| S6-16 | 25277–25489 | look at how much of your list you reached, how many engaged, how many turned into pipeline, pipeline per dollar | BGORANGE: one results card (B03, one card not tiles) with a four-stage funnel lit on words: LIST REACHED (25300) → ACCOUNTS ENGAGED (25340) → PIPELINE (25383) → PIPELINE PER $ (25440). No invented numbers. | V2 base + comp |
| S6-17 | 25499–25790 | content: every two weeks a 30-minute interview with your founder → posts → thought leader ads → engagers become signals | BGORANGE: **the content loop** (O03 orbit): INTERVIEW · 30 MIN · EVERY 2 WEEKS (mic icon, 25537) → POSTS (25600) → THOUGHT LEADER ADS (25658) → ENGAGERS (25720) → SIGNALS (25760), Arrowlines, the last arrow back into the first. | V2 base + comp |
| S6-18 | 25794–26133 | people who book calls followed us 6–12 months without liking a post… your ICP can follow you, never engage, then book | Over A-roll: a timeline bar FOLLOWS → 6–12 MONTHS (grey heart icons, none lit) → BOOKED A CALL (calendar chip, 25900); on "never engaging" (26060) the hearts stay grey, the calendar chip shines. | V4 comp |

## 11. STEP 7 · 26136–28907 (18:10.1–20:05.7)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| S7-0 | 26136–26214 | last step seven, run it every week | Lower third STEP 7 · RUN IT EVERY WEEK, strip with 7 lit. | V4 comp |
| S7-1 | 26219–26397 | nothing works if you set it up once and walk away… the part nobody wants to do, makes everything work | Over A-roll, bottom pair: SET IT UP ONCE ✗ (grey) · EVERY WEEK ✓ (orange, 26308), a calendar icon with weeks ticking. | V4 comp |
| S7-2 | 26402–26655 | first emails go out around week three, domains warm, messaging approved… weekly rhythm you can copy | BGORANGE: the 90-day bar fills to WEEK 3 · FIRST EMAILS (26470) with DOMAINS WARM ✓ · MESSAGING APPROVED ✓ chips; on "weekly rhythm" (26548) **the weekly strip** lands under it: MON · TUE–THU · FRI. | V2 base + comp (strip returns S7-3…S7-5) |
| S7-3 | 26660–26909 | Monday: sending health; bounces above the line → pause, figure out why; a burned domain costs weeks | Strip with MON lit (26660); then **Instantly sending-health demo**: accounts table with a Bounce rate column, one account's rate in red above the threshold, cursor hits Pause campaign (26800). Threshold value: §7. | V4 comp; V2 render + V3 |
| S7-4 | 26913–27177 | during the week sort every reply: interested, not interested, not a fit; interested → salesperson same day, research attached | Strip, TUE–THU lit (26913); **Unibox demo**: replies labelled by the cursor INTERESTED (orange) · NOT NOW · NOT A FIT (26982–27042); an interested one → Send to sales → the Slack handoff card (27048–27177). | V4 comp; V2 render + V3 |
| S7-5 | 27179–27298 | Friday: look at each campaign, one decision: keep, change or kill | Strip, FRI lit (27179); **campaign list demo**: three campaigns get KEEP ✓ · CHANGE ✎ · KILL ✗ on his words (27257–27298). | V4 comp; V2 render + V3 |
| S7-6 | 27301–27586 | change one thing at a time: the list, the offer or the copy, launch both versions the same day… three things at once, you learn nothing, no proper A/B test | BGORANGE: B02 compare: VERSION A and VERSION B cards identical, one chip differs and lights (THE OFFER, 27364); the three chips LIST · OFFER · COPY land on words (27364–27416); SAME DAY tag (27421); then a third card with three chips changed gets a ✗ LEARN NOTHING (27474–27586). | V2 base + comp |
| S7-7 | 27593–27742 | be careful what you measure: opens are unreliable, we don't track them | Over A-roll: a metric chip OPENS struck through by the orange marker (27640). | V4 comp |
| S7-8 | 27747–28029 | positive replies ÷ emails sent, then meetings, then qualified pipeline; ads: list reached, accounts engaged, pipeline | BGORANGE: WHAT TO MEASURE board, two columns: EMAIL: POSITIVE REPLIES / EMAILS SENT (a fraction, 27747) → MEETINGS (27820) → QUALIFIED PIPELINE (27850); ADS: LIST REACHED (27870) → ACCOUNTS ENGAGED (27940) → PIPELINE (28000). | V2 base + comp |
| S7-9 | 28038–28214 | outbound takes weeks to ramp, don't judge it in month one… offer, copy, targeting take a while | Over A-roll: a ramp line drawing on over MONTH 1 · 2 · 3, Neo Glow, with three small chips OFFER · COPY · TARGETING (28145). | V4 comp |
| S7-10 | 28222–28442 | month one: emails land, right people reply; month two: double down, cut what doesn't, add signal-based campaigns | BGORANGE: the 90-day bar, MONTH 1 segment with chips EMAILS LAND · RIGHT PEOPLE REPLY (28222–28316), MONTH 2 with DOUBLE DOWN · CUT WHAT DOESN'T · ADD SIGNAL CAMPAIGNS (28321–28442). | V2 base + comp (one scene with S7-11) |
| S7-11 | 28446–28907 | end of the quarter: sit down with your team: which segments replied, which offers got meetings, which signals showed up before won deals… newest closed-won deals → back to step one… repeat every three months | Same scene: QUARTER REVIEW lights (28446); three chips SEGMENTS THAT REPLIED · OFFERS THAT GOT MEETINGS · SIGNALS BEFORE WON DEALS (28540–28674); then the roadmap appears under the bar and a curved Arrowline loops from 7 back to 1 on "back to step one" (28720); on "every three months" (28850) the loop pulses. | same comp |

## 12. RECAP AND CTA · 28913–29986 (20:05.9–20:50.7)

| ID | Frames | Alex says | Visual | Build |
|---|---|---|---|---|
| R1 | 28913–29177 | the whole thing: closed-won deals, map and cut, tier, signals, message first, ads on the same list, run it every week | BGORANGE: title THE WHOLE THING; the roadmap with all seven names; each disc ticks orange on its phrase (28936 / 28982 / 29027 / 29053 / 29079 / 29108 / 29140). | V2 base + comp |
| R2 | 29179–29285 | what we'd do for any new client, you can copy every step, starting today | A-roll (punch-in). | — |
| R3 | 29291–29455 | rather not spend months building it… book a call, we build and run it with your team | **frontal.so captured**: the hero with "Book a 30-minute call", the cursor hovering the button. | V2 capture + V3 |
| R4 | 29460–29663 | Frontal: the go-to-market partner for B2B tech… GTM services, ads, content engineering, RevOps… start with just one | BGORANGE: Frontal logo (real SVG) with the two-tone line THE GO-TO-MARKET PARTNER / FOR B2B TECH COMPANIES; four service pills land on words GTM SERVICES (29560) · ADS (29580) · CONTENT ENGINEERING (29595) · REVOPS (29610), mixed fills; on "just one" (29640) three dim and one shines. | V2 base + comp |
| R5 | 29669–29759 | on the call we tell you where you are… the link is in the description | Lower third book.frontal.so pill + LINK IN THE DESCRIPTION (M3 reuse). | V4 comp |
| R6 | 29768–29935 | start on your own this week, go back to step one, pull your last 40–50 closed-won deals | BGORANGE: STEP ONE · THIS WEEK, roadmap with 1 lit; a card PULL YOUR LAST 40–50 CLOSED-WON DEALS with a CRM icon lands on 29843. | V2 base + comp |
| R7 | 29939–29986 | thanks for watching | A-roll. | — |

---

## 13. Pacing check against the targets

Counted from the tables: **116 visual blocks** (hook ideas included), about 30 full-screen UI demos and captures, about 50 Fusion overlays on the A-roll, about 30 full-frame BGORANGE comps, 1 AI B-roll. Inside them about 290 timed landings, so a new element every 4–5 s of talk. Plain A-roll stretches: 3111–3206 (4 s), 3757–3810, 4372–4487 (4.8 s), 7459–7539, 12894–12935, 20491–20588, 29179–29285 (4.4 s), 29939–end. None over 8 s. Visual on screen about 80% of the talk.

**Punch-in spots for Samuel (V5, MagicZoom V3):** 3111, 4372, 7459, 12894, 20491, 29179, plus the inside of long A-roll-with-overlay stretches where the overlay sits to one side (6195–6750, 10917–11375).

**Where a MagicMask cut-out of Alex would help** (his GUI, optional): the roadmap landing behind him at A1 and R1 if he prefers it over the A-roll instead of full-frame BGORANGE.

## 14. Node kit per visual type

- **Lower-third stepper (S*-0):** canvas → RectangleMask capsule (CornerRadius 1) → fill Background (deep orange `#BE4117`→`#591E0B` gradient) + Instance border `#FF5A1F` with Neo Glow → NeoTextMotion Geist ExtraBold "STEP n" (orange) + Text+ name (white) → NeoLightSweep static → DropShadow → Neo Anim (in from the left, 20 f, out on the end cut). Mini strip: 7 EllipseMask discs on a Polygon line, the current one with Neo Glow, done ones `#FF5A1F`, upcoming `#3A2A24`. One row per disc, collector column.
- **Pill / medallion (P01):** RectangleMask capsule → fill; EllipseMask white disc + Instance orange ring with Neo Glow; Loader logo → Transform → masked by the disc; Text+ Geist SemiBold; NeoBevel → NeoLightSweep → DropShadow → Neo Anim. Icon pills: Flaticon solid SVG→PNG Loader masking a Background (orange or white) + light sweep.
- **Card:** RectangleMask (CornerRadius 0.30–0.34) → gradient fill → Instance border → Neo Glow on the border → NeoLightSweep → moving shine (BrightnessContrast under an inclined RectangleMask, 0.07 wide, one pass after landing) → DropShadow → Neo Anim. Header texts, chips and dividers on their own line over a clear canvas.
- **Fill bars (P09):** two RectangleMasks (track graphite, fill orange) with the fill's Width keyed on a spline (Expo), Number Counter macro for the figure.
- **Counters:** his Number Counter macro.
- **Lines and arrows:** Polygon on a Background with WriteOn (Neo Glow when it leads the eye); his Arrowline macro for arrows; Moving dashed line only in S4-12 (the badge that lands outside the list).
- **Marker strikes and circles (O09):** Paint PolylineStroke, orange, WriteOnEnd, slight roughness.
- **Dim / settle:** BrightnessContrast (Gain) per element group, keyed; his Opacity macro for fades. Never Merge Blend.
- **Ground:** his BGORANGE macro at the start of the main line for full-frame comps; nothing for overlays.
- **Focus comps on demos (V3):** BrightnessContrast darkening outside a RectangleMask (soft edge), Transform zoom ≤ 1.3, keys on spline, 18 f moves, generated from the DOM boxes by `focusgen` (the Apollo M6 settings).

## 15. Build order (phases) and checkpoints

Each phase ends with the project saved, a check render looked at, a log line and a commit of this note.

1. **Engines and captures** (first, they gate the demos): copy the Apollo engines (`gmail.html`, `notion.html`, `apollo8.html`, `browser.html`, `render3.py`, `focusgen6.py`) into `Graphics\Visuals v1\engines\`; build the new ones: calls, instantly, crm, clay, sheets, signals, linkedin (feed, job change, reactions, campaign manager, analytics), ads manager, slack, verify, sequence, docs-compose. Capture the eight real pages (§6) in the browser at 1920×1080 device pixels.
2. **Kits:** `stepper`, `board`, `roadmap`, `bar90`, `onelist` builders on `pk.py` / `m6kit.py`; the Ivan/Alex medallion asset; Flaticon icon set (solid, black) for every icon named above.
3. **Sections in this order:** Step 3 (9703–12888, the board carries it) → Step 4 (13232–18125) → Step 2 → Step 1 → After you sign → Step 5 → Step 6 → Step 7 → Recap → Mid CTA → What we tell every new client → Hook (only on Samuel's yes). Each section: render demos → place on V2 → focus comps on V3 → Fusion overlays on V4 → check render of the section → log.
4. **Whole-video check render**, contact sheet, fixes.
5. **Sound** after Samuel's picture approval: SFX only unless he overrides Alex's no-music note.

## 16. Open items for Samuel

1. **Numbers where the kept take differs from the script** (cards follow the script unless he says otherwise): 6sense "5,000 buyers" (he) vs 4,500 (script) vs "nearly 4,000" (the report itself) → the card carries the source only, no count; bounce rate "above 5%" (he) vs 2% (script) → S7-3 shows the red rate above a line, no number, unless he picks one; booked meetings "about half" (he) vs "about a third" (script) → S5-9; "under 100 characters" (he) vs words (script) → S5-3a shows a word count.
2. **The hook** (0:00–1:43.9): ideated in §1. Build it too, or leave it to him?
3. **Music:** Alex's note says none under the voice. The house style scores every section. His call before the sound pass.
4. **Metadata 2026 "0.56× vs 7.6×"**: the numbers are from Alex's on-screen plan; the live page doesn't show that exact comparison. Keep as Alex wrote it, with the source caption?
5. **Gartner page capture** may be blocked (403 on fetch); fallback is the stat pill alone.
6. **Ivan's photo** from frontal.so is used at every mention (hook, step 3, step 6 ×4). Alex's plan asks for a lower third at step 6 only; the extra uses are mine.

Sources for every number on screen: 6sense Buyer Experience Report 2025 · Gartner press release 2025-06-25 · TrustRadius 2026 Buying Disconnect · UserGems "How much are previous champions worth" · Demand Gen Report 2025 ABM benchmark · LinkedIn Thought Leader Ads two-pager · Metadata 2026 benchmark · Google sender guidelines · Frontal campaign data (0.64%, 1 in 3).

## 6 (assets). Where each real UI and page comes from

| Needed | Source to measure from |
|---|---|
| Gmail inbox and compose | mail.google.com (Samuel's Chrome, signed in; capture a blank inbox for layout) |
| Instantly: Email accounts, Campaign analytics, Unibox, Sending health | https://instantly.ai (product pages) and Google Images "instantly.ai email accounts page", "instantly unibox" (vendor help-centre shots, no marketing frames) |
| HubSpot CRM deals board and contacts list | https://knowledge.hubspot.com (help-centre screenshots of the Deals board view and Contacts index) |
| Clay table | https://www.clay.com (product shots), Google Images "clay table enrichment column" |
| Notion page (ICP matrix) | the Apollo job's `notion.html` engine |
| Apollo Find companies filters | the Apollo job's `apollo8.html` engine |
| LeadMagic email verification | https://leadmagic.io (product shots) |
| Google Sheets | docs.google.com/spreadsheets (new blank sheet in Chrome) |
| Signals feed (original, GTM OS look) | the Apollo job's `GTM OS demo\gtm_os.html` dark theme |
| RB2B · Vector · Fibbler dashboards | https://www.rb2b.com · https://www.vector.co · https://www.fibbler.co (their own product screenshots; skip any with callouts) |
| LinkedIn feed post, job-change card, reactions list, post analytics | linkedin.com in Samuel's Chrome (signed in; a public figure's post for layout; hide the messaging dock) |
| LinkedIn Campaign Manager | https://www.linkedin.com/help/lms (help-centre screenshots of Audiences → Upload a list and the campaign setup), Google Images |
| Meta Ads Manager | https://www.facebook.com/business/help (help-centre screenshots of the campaign table and toggles) |
| Slack channel | slack.com product shots (dark theme) |
| Call transcript UI | original, Fireflies/Gong-like layout from their product pages (no logo) |
| Real pages to capture | 6sense https://6sense.com/science-of-b2b/buyer-experience-report-2025/ · Gartner https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-sales-survey-finds-61-percent-of-b2b-buyers-prefer-a-rep-free-buying-experience · TrustRadius https://solutions.trustradius.com/buyer-blog/beyond-the-hype/ · UserGems https://www.usergems.com/blog/how-much-are-previous-champions-worth · LinkedIn PDF https://business.linkedin.com/content/dam/lem/business/en/advertise/ads/sponsored-content/thought-leader-ads-two-pager.pdf · Google https://support.google.com/mail/answer/14229414 · Frontal https://frontal.so |
| Team photos and logo | https://frontal.so/assets/team/ivan.jpg, alex.jpg; logo SVGs. Saved in `Screenshots\Frontal team\` |
| Logos | Google favicon service `s2/favicons?domain=<site>&sz=128` for Apollo, Clay, LinkedIn, Crunchbase, Meta, Google, Instantly; Claude's own mark from the Apollo job's `Graphics\Logos\` |
| Icons | Flaticon solid icons (black), exported as PNG: envelope, person, sparkle, post, phone book, flame, fuel can, target, key, clock, speech bubble, robot, calendar, mic, heart, stop sign, check, cross, dollar, building, trophy |
