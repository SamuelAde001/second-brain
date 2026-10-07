import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Limit, UsageSnapshot } from '../types'

// Brain HUD: who is working, how full the context is, how much of the 5-hour
// and weekly limits is gone (resets in WAT), and how many files wait for a
// commit (AGENTS.md rule 4). Warns before a limit runs out so /hand-back can
// run while there is still room (00-System/relay.md).

const PANE = 'brain-usage'
const agent = atom({ plugin: 'brain-hud', key: 'agent' } as const, null)
const dirty = atom({ plugin: 'brain-hud', key: 'dirty' } as const, 0)
const isHidden = atom({ plugin: 'brain-hud', key: 'isHidden' } as const, false)
const usage = atom({ plugin: 'brain-hud', key: 'usage' } as const, null)

const AGENT_TAG = /\*\*\[([^\]\n]{1,30})\]\*\*/g
const WAT_OFFSET_MS = 3600_000
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const LIMIT_STEPS = [75, 90]
const CONTEXT_STEPS = [70, 85]

export function lastAgent(text: string): string | null {
  let found: string | null = null
  for (const m of text.matchAll(AGENT_TAG)) found = m[1] ?? found
  return found
}

export function wat(iso: string | undefined, withDay: boolean): string {
  const t = iso ? Date.parse(iso) : NaN
  if (Number.isNaN(t)) return '?'
  const d = new Date(t + WAT_OFFSET_MS)
  const hm = `${String(d.getUTCHours()).padStart(2, '0')}:${String(d.getUTCMinutes()).padStart(2, '0')}`
  return withDay ? `${DAYS[d.getUTCDay()]} ${hm}` : hm
}

function windowName(kind: string): string {
  if (kind === 'five_hour') return '5h'
  if (kind === 'seven_day') return 'Week'
  return kind.replace(/_/g, ' ')
}

function k(n: number): string {
  return n >= 1000 ? `${Math.round(n / 1000)}k` : String(n)
}

function tone(p: number): string {
  return p >= 85 ? 'red' : p >= 60 ? 'yellow' : 'green'
}

function bar(p: number, width = 12): string {
  const full = Math.max(0, Math.min(width, Math.round((p / 100) * width)))
  return '█'.repeat(full) + '░'.repeat(width - full)
}

// The highest step a value has crossed, 0 for none.
export function stepFor(p: number, steps: number[]): number {
  return steps.filter(s => p >= s).pop() ?? 0
}

function limitWarning(r: Limit, step: number): string {
  const name = windowName(r.kind)
  const resets = wat(r.resetsAt, r.kind !== 'five_hour')
  return step >= 90
    ? `${name} limit at ${r.percentUsed}%, resets ${resets} WAT. Run /hand-back now so Gemini can pick up.`
    : `${name} limit at ${r.percentUsed}%, resets ${resets} WAT. Finish this piece and commit; /hand-back if you need to keep going.`
}

function contextWarning(p: number, step: number): string {
  return step >= 85
    ? `Context ${p}% full, compaction is close. Commit, update build-state, start a fresh session.`
    : `Context ${p}% full. Good point to commit and start a fresh session.`
}

// Steps already toasted, per window; a window that drops back resets.
const warned = new Map<string, number>()

function warn($: EngineInterface, key: string, step: number, text: string): void {
  if (step === 0) {
    warned.delete(key)
    return
  }
  if ((warned.get(key) ?? 0) >= step) return
  warned.set(key, step)
  $.ui.toast(text, { timeoutMs: 12000 })
}

async function countDirty($: EngineInterface): Promise<number> {
  try {
    const { exitCode, stdout } = await $.process.run(['git', 'status', '--porcelain'])
    return exitCode === 0 ? stdout.split(/\r?\n/).filter(line => line.trim() !== '').length : 0
  } catch {
    return 0
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'brain',
      description: 'Brain HUD: open the usage pane; "hide" or "show" the band',
    })
    const u = await $.session.usage()
    await update($, usage, () => ({ context: u.context, rateLimits: u.rateLimits, cost: u.cost }))
    const n = await countDirty($)
    await update($, dirty, () => n)

    return next(e)
  })

  on('session.measure', async ($, e, next) => {
    const snap: UsageSnapshot = { context: e.context, rateLimits: e.rateLimits, cost: e.cost }
    await update($, usage, () => snap)

    for (const r of e.rateLimits) {
      const step = stepFor(r.percentUsed, LIMIT_STEPS)
      warn($, r.kind, step, limitWarning(r, step))
    }
    const p = e.context.percent
    if (p !== undefined) {
      const step = stepFor(p, CONTEXT_STEPS)
      warn($, 'context', step, contextWarning(p, step))
    }

    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const name = lastAgent(e.answer)
    if (name !== null) await update($, agent, () => name)
    const n = await countDirty($)
    await update($, dirty, () => n)

    const snap = await read($, usage)
    const five = snap?.rateLimits.find(r => r.kind === 'five_hour')
    const ctx = snap?.context.percent
    $.ui.status(
      `[${name ?? (await read($, agent)) ?? 'General Manager'}]` +
        (ctx !== undefined ? ` ctx ${ctx}%` : '') +
        (five ? ` · 5h ${five.percentUsed}%` : ''),
    )

    return next(e)
  })

  on('command.run', { command: 'brain' }, async ($, e) => {
    const arg = e.args.trim().toLowerCase()
    if (arg === 'hide' || arg === 'show') {
      await update($, isHidden, () => arg === 'hide')
      return { text: arg === 'hide' ? 'Brain HUD band hidden. /brain show brings it back.' : 'Brain HUD band shown.' }
    }
    const u = await $.session.usage()
    await update($, usage, () => ({ context: u.context, rateLimits: u.rateLimits, cost: u.cost }))
    await $.ui.open({ id: PANE, title: 'Brain usage' })

    return { text: 'Brain usage pane opened.' }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey || (await read($, isHidden))) return next(e)
    const snap = await read($, usage)
    if (snap === null) return next(e)

    const { Box, Button, Text } = $.ui.resolve(e)
    const who = (await read($, agent)) ?? 'General Manager'
    const files = await read($, dirty)
    const ctx = snap.context

    return (
      <Box flexDirection="row">
        <Text bold>[{who}]</Text>
        <Text dimColor> │ </Text>
        {ctx.percent !== undefined ? (
          <Text color={tone(ctx.percent)}>
            Context {ctx.percent}% ({k(ctx.tokens ?? 0)}/{k(ctx.window)})
          </Text>
        ) : (
          <Text dimColor>Context –</Text>
        )}
        {snap.rateLimits.map(r => (
          <Text key={r.kind} color={tone(r.percentUsed)}>
            {'  '}
            {windowName(r.kind)} {r.percentUsed}% → {wat(r.resetsAt, r.kind !== 'five_hour')}
          </Text>
        ))}
        {files > 0 && <Text color="yellow">{'  '}{files} uncommitted</Text>}
        <Text> </Text>
        <Button key="details" label="Details" onPress={async () => {
          await $.ui.open({ id: PANE, title: 'Brain usage' })
        }} />
        <Button key="hide" label="Hide" onPress={() => update($, isHidden, () => true)} />
      </Box>
    )
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Button, Text } = $.ui.resolve(e)
    const full = await $.session.usage({ breakdown: 'summary' })
    const snap = (await read($, usage)) ?? full
    const who = (await read($, agent)) ?? 'General Manager'
    const files = await read($, dirty)
    const b = full.context.breakdown
    const rows = (b?.categories ?? []).filter(c => c.tokens > 0).sort((x, y) => y.tokens - x.tokens)

    return (
      <Box flexDirection="column">
        <Text bold>Working: [{who}]</Text>
        <Text> </Text>
        <Text bold>Plan limits (Max, resets in WAT)</Text>
        {snap.rateLimits.length === 0 && <Text dimColor>No reading yet. Shows after the first reply.</Text>}
        {snap.rateLimits.map(r => (
          <Text key={r.kind} color={tone(r.percentUsed)}>
            {windowName(r.kind).padEnd(6)} {bar(r.percentUsed)} {String(r.percentUsed).padStart(5)}%  resets {wat(r.resetsAt, true)}
          </Text>
        ))}
        <Text> </Text>
        <Text bold>Context window</Text>
        {snap.context.percent !== undefined ? (
          <Text color={tone(snap.context.percent)}>
            {bar(snap.context.percent)} {snap.context.percent}%  {k(snap.context.tokens ?? 0)} of {k(snap.context.window)}
          </Text>
        ) : (
          <Text dimColor>No reading yet.</Text>
        )}
        {rows.map(c => (
          <Text key={c.name} dimColor>
            {'  '}{c.name.padEnd(22)} {k(c.tokens).padStart(6)}
          </Text>
        ))}
        {b?.memoryFiles && b.memoryFiles.length > 0 && (
          <Text dimColor>  Memory files: {b.memoryFiles.length}, {k(b.memoryFiles.reduce((s, f) => s + f.tokens, 0))}</Text>
        )}
        {b?.mcpTools && b.mcpTools.length > 0 && (
          <Text dimColor>  MCP tools loaded: {b.mcpTools.length}, {k(b.mcpTools.reduce((s, t) => s + t.tokens, 0))}</Text>
        )}
        <Text> </Text>
        <Text bold>Session</Text>
        <Text dimColor>
          API-value of this session: USD {(snap.cost?.usd ?? 0).toFixed(2)} (not billed on Max; a size gauge only)
        </Text>
        <Text color={files > 0 ? 'yellow' : 'green'}>
          {files > 0 ? `${files} files not committed yet` : 'Everything committed'}
        </Text>
        <Text> </Text>
        <Box flexDirection="row">
          <Button key="refresh" label="Refresh" onPress={async () => {
            const u = await $.session.usage()
            await update($, usage, () => ({ context: u.context, rateLimits: u.rateLimits, cost: u.cost }))
          }} />
          <Button key="show" label="Show band" onPress={() => update($, isHidden, () => false)} />
        </Box>
      </Box>
    )
  })
}
