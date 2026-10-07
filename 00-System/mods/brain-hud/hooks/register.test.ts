import { expect, test } from 'claude-code/testing'

import { lastAgent, stepFor, wat } from './register'

test('reads the last agent tag in a reply', async () => {
  expect(lastAgent('**[General Manager]** routing\n\n**[Money man]** logged it')).toBe('Money man')
  expect(lastAgent('no tag here')).toBe(null)
})

test('shows reset times in WAT (UTC+1)', async () => {
  expect(wat('2026-10-07T13:20:00Z', false)).toBe('14:20')
  expect(wat('2026-10-12T08:00:00Z', true)).toBe('Mon 09:00')
  expect(wat(undefined, false)).toBe('?')
})

test('warning steps', async () => {
  expect(stepFor(40, [75, 90])).toBe(0)
  expect(stepFor(76, [75, 90])).toBe(75)
  expect(stepFor(93, [75, 90])).toBe(90)
})
