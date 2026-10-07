export type Limit = { kind: string; percentUsed: number; resetsAt?: string }

export type UsageSnapshot = {
  context: { tokens?: number; window: number; percent?: number }
  rateLimits: Limit[]
  cost?: { usd: number }
}

declare module 'claude-code' {
  interface PluginState {
    'brain-hud': {
      agent: string | null
      dirty: number
      isHidden: boolean
      usage: UsageSnapshot | null
    }
  }
}
