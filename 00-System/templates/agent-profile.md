---
type: agent
area: <primary-area>
status: active
updated: YYYY-MM-DD
source: interview
tags: [agent]
name: <agent-name>
description: >-
  One or two sentences: what it owns and when to use it. Tools route work by this text.
tier: standard
tools: [read, write]
---

# <Agent name>

## Mission
One paragraph. What this agent is for.

## Scope
**Owns:** 
**Does not touch:** 

## Folders it may write
- 

## Folders it may read
- 

## Folders outside the Brain it may access
- (explicit list, or "none")

## Tools and MCPs
- The frontmatter `tools:` list is the grant, in neutral names — `read`, `write`, `shell`, `send-file`, `web`, `mcp:<server>:<tool>` ([[00-System/portability|portability]]). `tier:` is `light`, `standard` or `strong`, never a model name.
- After creating or editing this profile, run `python 00-System/scripts/build_adapters.py`.

## Skills
- 

## Rituals and triggers
- When it runs, and what starts it.

## Hard limits
- Never:

## Must ask Samuel before
- 

## Handoff rules
Reports to the orchestrator. Cross-domain requests go through [[handoffs]].

## Output format
What its answers look like: length, structure, whether it cites note links.
