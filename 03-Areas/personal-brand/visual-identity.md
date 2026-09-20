---
type: knowledge
area: personal-brand
status: needs-input
source: memory-export
tags: [brand, design, gamma]
---

# Visual identity and the Gamma production system

From the Claude memory export for the project named **"My Custom brand project"**, 2026-09-06. A systematised production operation for branded visual deliverables — Instagram carousels, pitch decks and workbooks — generated through **Gamma.app**.

> ⚠️ **Which brand is this for?** The source says "Samuel's brand system" without ever naming the brand. It could be the personal brand (@SamuelSignals), HighSignals, or a client-facing service. It is filed here provisionally. `needs-input` — see open questions.

## The idea

Encode every brand constraint **once**, then change only the topic between uses. "Separate locked from swappable variables: only the TOPIC line changes per use." The output is a **paste-ready prompt** Samuel can run directly in Gamma with no further editing.

## The locked brand system — non-negotiable across all deliverables

**Colours**

| Name | Hex |
|------|-----|
| Cobalt Blue | `#0540AD` |
| Deep Navy | `#002253` |
| Ink | `#424140` |
| Icon Blue | `#A9D4FE` |
| White | `#FFFFFF` |
| Content gradient | `#FBFEFF` → `#94E8F9` |

**Typography:** Poppins, across defined weights and a set size hierarchy.
**Icons:** thin-line, Lucide / Feather style.
**Illustration:** 3D soft-rendered for covers and closers; single-colour line icons for body slides.
**Footer:** one fixed structure across every format.

## Format templates

| Format | Size | Structure |
|--------|------|-----------|
| **Instagram carousel** | 1080×1350, 4:5 portrait | 6 slides locked: hook cover → reframe → three numbered principle slides → CTA closer. Slides 3–5 use a punchier large-number format — a deliberate deviation from the default card anatomy that Samuel adopted. |
| **Pitch deck** | 16:9 landscape | 7 slides, investor structure: cover, problem, solution, market, traction, business model, ask. Landscape overrides the portrait default; all other brand variables stay locked. |
| **Workbook** | Letter portrait | Article-to-workbook conversion, under 30 pages, **each section ends in one immediate action step**. |

## Working principles

- **Structure before aesthetics.** Narrative logic and sequencing beat polish. Every strong deck shares one skeleton: **hook → tension → proof → mechanism → close.**
- **One flex per deck** — lead with a single undeniable strength. Applies to investor pitches and carousels alike.
- **Reference ≠ brand.** Visual or structural elements borrowed from a reference carousel belong to *that reference*, not to Samuel's system. New concepts get built on his own locked system.
- **Format follows function.** Format overrides are deliberate, never defaults.
- Iteration is systematic: refine the previous prompt version rather than rebuilding from scratch.

## Known friction

**Gamma drifts on exact hex values — run a colour check after every generation.**

Worth reading alongside [[03-Areas/academy/current-production|Academy production]], where Gamma was dropped for course slides in favour of PPTX via `pptxgenjs` after unsatisfactory results. Same tool, two verdicts, different jobs.

## Current state, 2026-09-06

Carousels, pitch decks and workbooks in production in parallel. Next step for workbooks: pre-fill section structures with real source frameworks instead of leaving interpretation to Gamma. Ongoing study of canonical pitch decks (Airbnb, LinkedIn, Uber) for narrative architecture.

## needs-input

- **Which brand does this locked system belong to** — @SamuelSignals, HighSignals, or client work?
- Is this still running, and what has it produced?
- If these are client deliverables, that is a service line the vault has no record of.

Back to [[03-Areas/personal-brand/_index|Personal brand]]
