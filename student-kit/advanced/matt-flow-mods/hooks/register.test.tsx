import { expect, test } from 'claude-code/testing'
import type { TestBody } from 'claude-code/testing'
import type { FsEntry, SessionMessage, UiPane } from 'claude-code'

const REPO = '/repo'

type Engine = Parameters<TestBody>[0]

const PANE = {
  plugin: 'matt-flow',
  component: 'Pane',
  requestId: 'matt-flow',
  props: {
    title: '✦ Matt 導航',
    isFocused: false,
    bodyColumns: 40,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 40 },
    view: {},
  },
} as const

const SURFACES = ['terminal', 'desktop', 'vscode', 'mobile'] as const

const SETUP_FILE = 'docs/agents/issue-tracker.md'
// A project set up with the local markdown tracker.
const LOCAL = { [SETUP_FILE]: '# Issue tracker: Local Markdown\n' }
const GITHUB = { [SETUP_FILE]: '# Issue tracker: GitHub\n' }

type World = {
  // Paths relative to REPO, and their text.
  files?: Record<string, string>
  // What an earlier version left in the store for this project.
  stored?: unknown
  // Other projects' progress in the same store, by their roots.
  others?: Record<string, unknown>
  // What the person has half typed in the prompt box.
  draft?: string
  // The title `git log` gives the last commit.
  commit?: string
}

const DAY = 86_400_000

// Stands for the engine beneath the plugin. The files given predate the
// session; those `write` adds come later, newer than anything the plugin timed.
const engine = (
  on: Parameters<TestBody>[1],
  { files = LOCAL, stored, others = {}, draft = '', commit = 'Add a login page' }: World = {},
) => {
  const disk = new Map(Object.entries(files).map(([path, text]) => [path, { text, mtimeMs: 0 }]))
  const rel = (path: string) => (path.startsWith(`${REPO}/`) ? path.slice(REPO.length + 1) : path)
  const filled: { text: string; mode?: string }[] = []
  const suggested: string[] = []
  const toasts: string[] = []
  const panes: UiPane[] = []
  on('command.register', () => ({ value: { command: 'matt-flow' } }))
  on('ui.open', (_, e) => {
    panes.push({ id: e.id, title: e.title ?? '', isShown: true, isFocused: false, isPlaced: true })

    return { value: { isPlaced: true } }
  })
  on('ui.close', (_, e) => {
    panes.splice(panes.findIndex(pane => pane.id === e.id), 1)

    return { value: undefined }
  })
  on('ui.panes', () => ({ value: panes }))
  on('ui.status', () => ({ value: undefined }))
  on('ui.toast', (_, e) => {
    toasts.push(e.text)

    return { value: undefined }
  })
  on('session.usage', () => ({ value: { startedAt: 0, context: { tokens: 50_000, window: 200_000 }, rateLimits: [] } }))
  let now = 1
  on('clock.now', () => ({ value: now }))
  // The conversation the model holds: a test compacts, clears or rewinds it by hand.
  const conversation: SessionMessage[] = []
  on('session.messages', () => ({ value: conversation }))
  on('fs.read', (_, e) => ({ value: disk.get(rel(e.path))?.text ?? '' }))
  on('fs.exists', (_, e) => ({ value: disk.has(rel(e.path)) }))
  on('fs.list', (_, e) => {
    const dir = `${rel(e.path)}/`
    const entries = new Map<string, FsEntry>()
    for (const [path, { mtimeMs }] of disk) {
      if (!path.startsWith(dir)) continue
      const [name = '', ...rest] = path.slice(dir.length).split('/')
      const isDir = rest.length > 0
      entries.set(name, { name, kind: isDir ? 'dir' : 'file', size: 0, mtimeMs: isDir ? 0 : mtimeMs, isLink: false })
    }

    return { value: [...entries.values()] }
  })
  // The plugin's one store file, which every session of the plugin reads and writes.
  const store = new Map<string, unknown>([
    ...(stored === undefined ? [] : [[`progress:${REPO}`, stored] as const]),
    ...Object.entries(others).map(([root, saved]) => [`progress:${root}`, saved] as const),
  ])
  on('store.keys', () => ({ value: [...store.keys()] }))
  on('store.get', (_, e) => ({ value: store.get(e.key) }))
  on('store.set', (_, e) => {
    store.set(e.key, JSON.parse(JSON.stringify(e.value)))

    return { value: undefined }
  })
  on('prompt.fill', (_, e) => {
    filled.push({ text: e.text, mode: e.mode })

    return { isFilled: true }
  })
  on('prompt.suggest', (_, e) => {
    suggested.push(e.text)

    return { isShown: true }
  })
  on('prompt.read', () => ({ value: { text: draft, cursor: draft.length } }))
  // The repo's HEAD, moved by each commit Bash runs; a `--dry-run` moves nothing.
  let head = 0
  // `git rev-parse HEAD` answers the HEAD; `git log -1 --format=%s` the last commit's title.
  on('process.run', (_, e) => ({
    value: {
      exitCode: 0,
      stdout: `${e.argv.includes('rev-parse') ? `h${head}` : commit}\n`,
      stderr: '',
      isStdoutTruncated: false,
      isStderrTruncated: false,
    },
  }))
  on('turn.complete', () => ({ text: '' }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('session.end', (_, e) => ({ sessionId: e.sessionId }))
  on('prompt.submit', (_, e) => ({ text: e.text, context: e.context }))
  on('tool.call', (_, e) => {
    if (e.tool === 'Bash' && /\bcommit\b/.test(e.command) && !/--dry-run/.test(e.command)) head += 1

    return { result: {} }
  })

  return {
    filled,
    suggested,
    toasts,
    store,
    conversation,
    write: (path: string, text = '') => void disk.set(path, { text, mtimeMs: 2 }),
    // Moves the clock to `ms`.
    at: (ms: number) => void (now = ms),
  }
}

const start = ($: Engine) => $.session.start({ cwd: REPO, surface: 'terminal', isInteractive: true })

const turnEnds = ($: Engine) =>
  $.turn.complete({ answer: '', durationMs: 0, isAborted: false, turnId: 't', reason: 'answer' })

// The text of the pane's first Text matching `pattern`, on the terminal.
const seen = async ($: Engine, pattern: RegExp) => {
  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  const found = await ui.find({ type: 'Text', text: pattern })
  await ui.unmount()

  return found?.text
}

// The pane card's title: the step under way (▶), else the next one (→).
const card = ($: Engine) => seen($, /^[▶→] /)

// The person typing `/name`, as the engine raises it.
const typed = ($: Engine, name: string) =>
  $.prompt.submit({ text: `/${name}`, command: { name, args: '' }, wait: false, origin: { kind: 'composer' } })

test('a set-up project starts the beginner at grilling, on every surface', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: REPO, surface: 'terminal', isInteractive: true })

  for (const surface of SURFACES) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect((await ui.find({ type: 'Text', text: /設定專案/ }))?.text).toBe('✔ 1. 設定專案')
    expect((await ui.find({ type: 'Text', text: /^[▶→] / }))?.text).toBe('→ 2. 把想法問清楚')
    await ui.unmount()
  }
})

test('progress saved by 0.2 carries over: its steps passed, its rounds finished features', async ($, on) => {
  engine(on, { stored: { level: 'intermediate', done: ['grill', 'spec'], rounds: 2 } })
  await $.session.start({ cwd: REPO, surface: 'terminal', isInteractive: true })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect((await ui.find({ type: 'Text', text: /把想法問清楚/ }))?.text).toBe('✔ 2. 把想法問清楚')
  expect((await ui.find({ type: 'Text', text: /^[▶→] / }))?.text).toBe('→ 4. 切成任務卡')
  expect(await ui.find({ type: 'Text', text: /已完成 2 個功能/ })).toBeDefined()
  // Its spec passed with no folder on record to name the feature by.
  expect((await ui.find({ type: 'Text', text: /進行中/ }))?.text).toBe('功能進行中')
  await ui.unmount()
})

test('progress 0.2 left on a finished round loads as a finished feature, not a stuck one', async ($, on) => {
  engine(on, { stored: { level: 'beginner', done: ['setup', 'grill', 'build', 'review', 'retro'], rounds: 1 } })
  await start($)

  expect(await seen($, /已完成/)).toMatch(/已完成 2 個功能/)
  expect(await seen($, /進行中/)).toBe('還沒有進行中的功能')
  expect(await card($)).toBe('→ 2. 把想法問清楚')
})

test('a step the person types is under way, not passed: ▶ until the next step starts, then ✔', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'mattpocock-skills:grill-with-docs')

  expect(await card($)).toBe('▶ 2. 把想法問清楚（進行中）')
  expect(await seen($, /之後/)).toBe('   問題問完之後：/implement')
  expect(await seen($, /動手做/)).toBe('○ 3. 動手做')
  expect(await seen($, /\d \/ \d/)).toBe('1 / 5')

  await typed($, 'implement')
  expect(await seen($, /把想法問清楚/)).toBe('✔ 2. 把想法問清楚')
  expect(await card($)).toBe('▶ 3. 動手做（進行中）')
  expect(await seen($, /\d \/ \d/)).toBe('2 / 5')
})

test('the pane is a dashboard on every surface: the card offers skip and stuck, nothing that runs or passes a step', async ($, on) => {
  engine(on)
  await start($)
  await turnEnds($)

  for (const surface of SURFACES) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect(await ui.find({ key: 'skip' })).toBeDefined()
    expect(await ui.find({ key: 'stuck' })).toBeDefined()
    expect(await ui.find({ key: 'fill' })).toBeUndefined()
    expect(await ui.find({ key: 'mark' })).toBeUndefined()
    expect(await ui.find({ key: 'level-expert' })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /50k \/ 150k/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /已完成 0 個功能/ })).toBeDefined()
    await ui.unmount()
  }
})

test('skip on the pane works like /matt-flow skip: it passes over the next step, and a skipped step looks unlike a passed one', async ($, on) => {
  const { toasts } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  await ui.press({ key: 'skip' })
  expect(toasts.at(-1)).toBe('↷ 跳過「檢查」→ 下一步 /retro')
  expect((await ui.find({ type: 'Text', text: /把想法問清楚/ }))?.text).toBe('✔ 2. 把想法問清楚')
  expect((await ui.find({ type: 'Text', text: /4\. 檢查/ }))?.text).toBe('↷ 4. 檢查（跳過）')
  expect((await ui.find({ type: 'Text', text: /^[▶→] / }))?.text).toBe('▶ 3. 動手做（進行中）')
  await ui.unmount()
})

test('a skip passes over the step in the way: the next one, so the one under way still passes as it should', async ($, on) => {
  engine(on, { files: GITHUB, stored: { level: 'intermediate' } })
  await start($)
  await typed($, 'grill-with-docs')
  expect((await typed($, 'to-tickets')).drop).toMatch(/下一步是「寫成規格書」/)

  expect(await flow($, 'skip')).toBe('↷ 跳過「寫成規格書」→ 下一步 /to-tickets')
  expect((await typed($, 'to-tickets')).drop).toBeUndefined()
  expect(await seen($, /把想法問清楚/)).toBe('✔ 2. 把想法問清楚')
  expect(await card($)).toBe('▶ 4. 切成任務卡（進行中）')
})

test('a step under way that cannot be left is the one a skip passes over: a spec never written lets the tickets go on without files', async ($, on) => {
  engine(on, { stored: { level: 'intermediate' } })
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'to-spec')
  expect((await typed($, 'to-tickets')).drop).toMatch(/「寫成規格書」還沒做完/)

  expect(await flow($, 'skip')).toBe('↷ 跳過「寫成規格書」→ 下一步 /to-tickets')
  expect((await typed($, 'to-tickets')).drop).toBeUndefined()
  // No spec, so no folder to look in: the tickets wait for nothing.
  expect((await typed($, 'implement')).drop).toBeUndefined()
  expect(await card($)).toBe('▶ 5. 動手做（進行中）')
})

test('stuck puts /ask-matt with where the person is into the prompt box, the command first and their draft after it', async ($, on) => {
  const { filled } = engine(on, { draft: '為什麼一直被擋' })
  await start($)

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  await ui.press({ key: 'stuck' })
  expect(filled).toEqual([
    {
      text: '/ask-matt 我在 Matt 導航的「新手」流程，卡在「把想法問清楚」(/grill-with-docs)。沒有跳過步驟。現在會被擋：改程式碼（Edit、Write、NotebookEdit）。我遇到的狀況是：為什麼一直被擋',
      mode: 'replace',
    },
  ])
  await ui.unmount()
})

test('in a project the rail is quiet in, stuck tells /ask-matt nothing is locked', async ($, on) => {
  const { filled } = engine(on, { files: {} })
  await start($)

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  await ui.press({ key: 'stuck' })
  expect(filled.at(-1)?.text).toBe(
    '/ask-matt 我在 Matt 導航的「新手」流程，卡在「設定專案」(/setup-matt-pocock-skills)。沒有跳過步驟。現在沒有會被擋的動作。我遇到的狀況是：',
  )
  await ui.unmount()
})

test('stuck tells /ask-matt the steps skipped, what is locked, and how long the project has been left', async ($, on) => {
  const { filled, at } = engine(on)
  at(0)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  await flow($, 'skip')
  at(4 * DAY)

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  await ui.press({ key: 'stuck' })
  expect(filled.at(-1)?.text).toBe(
    '/ask-matt 我在 Matt 導航的「新手」流程，卡在「動手做」(/implement)。跳過了「檢查」。現在會被擋：git commit。4 天沒動。我遇到的狀況是：',
  )
  await ui.unmount()
})

test('inside a feature the person started, a skill the model runs through the Skill tool moves the guide on too', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:code-review' })

  expect(await seen($, /動手做/)).toBe('✔ 3. 動手做')
  expect(await card($)).toBe('▶ 4. 檢查（進行中）')
})

test('only the person starts a feature: a skill the model runs with none under way starts nothing', async ($, on) => {
  engine(on)
  await start($)
  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:grilling' })

  expect(await seen($, /進行中/)).toBe('還沒有進行中的功能')
  expect(await card($)).toBe('→ 2. 把想法問清楚')
})

test('a later step typed before building runs and moves nothing: building is not skipped, code stays locked', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  expect((await typed($, 'mattpocock-skills:code-review')).drop).toBeUndefined()

  expect(await card($)).toBe('▶ 2. 把想法問清楚（進行中）')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/implement/)
})

test('/retro typed with no feature under way starts nothing and finishes nothing', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'retro')

  expect(await seen($, /進行中/)).toBe('還沒有進行中的功能')
  expect(await seen($, /已完成/)).toMatch(/已完成 0 個功能/)
})

test('changing level while building goes on past the new level\'s building, code still open', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  await ui.press({ key: 'level-expert' })
  expect((await ui.find({ type: 'Text', text: /^[▶→] / }))?.text).toBe('→ 6. 開 PR 附證據')
  await ui.unmount()
  expect((await edit($, 'src/app.ts')).deny).toBeUndefined()
})

test('an expert building in parallel who turns beginner goes on to code-review', async ($, on) => {
  engine(on, { files: GITHUB, stored: { level: 'expert' } })
  await start($)
  for (const skill of ['grill-with-docs', 'to-spec', 'to-tickets', 'implement-spec']) await typed($, skill)

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  await ui.press({ key: 'level-beginner' })
  expect((await ui.find({ type: 'Text', text: /^[▶→] / }))?.text).toBe('→ 4. 檢查')
  await ui.unmount()
})

test('the expert level builds in parallel', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: REPO, surface: 'terminal', isInteractive: true })

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  await ui.press({ key: 'level-expert' })
  expect(await ui.find({ type: 'Text', text: /\/implement-spec/ })).toBeDefined()
  await ui.unmount()
})

test('a feature is done once the person ends it with its retro under way: it counts, and the next starts from grilling', async ($, on) => {
  engine(on)
  await start($)
  expect(await seen($, /進行中/)).toBe('還沒有進行中的功能')

  await typed($, 'grill-with-docs')
  expect(await seen($, /進行中/)).toBe('功能進行中')
  for (const skill of ['implement', 'mattpocock-skills:code-review', 'retro']) await typed($, skill)
  expect(await card($)).toBe('▶ 5. 複盤（進行中）')
  expect(await seen($, /之後/)).toBe('   複盤建議的環境改完之後：/matt-flow end')
  expect(await seen($, /已完成/)).toMatch(/已完成 0 個功能/)

  expect(await flow($, 'end')).toBe('🎉 功能結束，已完成 1 個功能 → 下一個從 /grill-with-docs 開始')
  expect(await seen($, /已完成/)).toMatch(/已完成 1 個功能/)
  expect(await card($)).toBe('→ 2. 把想法問清楚')
})

test('while the retro is under way code stays open for its changes, until the person ends the feature', async ($, on) => {
  const { toasts } = engine(on)
  await start($)
  for (const skill of ['grill-with-docs', 'implement', 'mattpocock-skills:code-review', 'retro']) await typed($, skill)

  expect(toasts.at(-1)).toBe('✔ 檢查 通過 · ▶ 開始「複盤」：複盤建議的環境改完之後，下一步 /matt-flow end')
  expect((await edit($, 'src/app.ts')).deny).toBeUndefined()
  // Grilling the model runs for a triage meanwhile moves nothing.
  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:grilling' })
  expect(await card($)).toBe('▶ 5. 複盤（進行中）')
  expect((await edit($, 'src/app.ts')).deny).toBeUndefined()
  await flow($, 'end')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/grill-with-docs/)
})

test('typing /grill-with-docs with the retro under way ends that feature done and starts the next', async ($, on) => {
  const { toasts } = engine(on)
  await start($)
  for (const skill of ['grill-with-docs', 'implement', 'mattpocock-skills:code-review', 'retro', 'grill-with-docs']) await typed($, skill)

  expect(toasts.at(-1)).toBe('🎉 功能結束，已完成 1 個功能 · ▶ 開始「把想法問清楚」：問題問完之後，下一步 /implement')
  expect(await card($)).toBe('▶ 2. 把想法問清楚（進行中）')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/implement/)
})

test('the next command goes in the prompt box once the step is seen done: after code-review ran, not as /implement starts', async ($, on) => {
  const { suggested, toasts } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  expect(toasts.at(-1)).toBe('✔ 把想法問清楚 通過 · ▶ 開始「動手做」：寫完之後，下一步 /mattpocock-skills:code-review')
  await turnEnds($)
  expect(suggested).toEqual([])

  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:code-review' })
  expect(toasts.at(-1)).toBe('✔ 動手做 通過 · ▶ 開始「檢查」：檢查完之後，下一步 /retro')
  await turnEnds($)
  expect(suggested).toEqual(['/retro'])
  // Offered once, not again every turn.
  await turnEnds($)
  expect(suggested).toEqual(['/retro'])
})

test('grilling and the retro are done when the person says so: neither offers the next command', async ($, on) => {
  const { suggested, toasts } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await turnEnds($)
  expect(toasts).toEqual(['▶ 開始「把想法問清楚」：問題問完之後，下一步 /implement'])
  expect(suggested).toEqual([])

  for (const skill of ['implement', 'mattpocock-skills:code-review', 'retro']) await typed($, skill)
  await turnEnds($)
  expect(suggested).toEqual([])
})

test('only the person starts building: the model running implement is told to hand over, tdd moves nothing', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')

  expect((await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:tdd' })).deny).toBeUndefined()
  expect((await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:implement' })).deny).toMatch(
    /由人輸入 \/implement 才開始.*停下來/,
  )
  expect(await card($)).toBe('▶ 2. 把想法問清楚（進行中）')
  await typed($, 'mattpocock-skills:implement')
  expect(await card($)).toBe('▶ 3. 動手做（進行中）')
})

test('the model never settles a step for the person: running the next step itself is denied, the review after building aside', async ($, on) => {
  engine(on, { files: GITHUB, stored: { level: 'intermediate' } })
  await start($)
  // With no feature under way, the model starts nothing and jumps nowhere either.
  expect((await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:implement' })).deny).toMatch(/由人輸入 \/implement 才開始/)
  expect((await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:to-spec' })).deny).toMatch(/還沒到「寫成規格書」/)

  await typed($, 'grill-with-docs')
  expect((await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:to-spec' })).deny).toMatch(
    /「寫成規格書」要由人輸入 \/to-spec 才開始.*停下來交棒/,
  )
  expect(await card($)).toBe('▶ 2. 把想法問清楚（進行中）')
})

test('while a step is under way a denied edit names the unlock command but does not prefill it: the person settles the step', async ($, on) => {
  const { suggested } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')

  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/implement/)
  await turnEnds($)
  expect(suggested).toEqual([])
})

test('a step typed ahead of the next one is dropped, naming the next step and /matt-flow skip; nothing moves', async ($, on) => {
  const { toasts } = engine(on)
  await start($)

  expect((await typed($, 'implement')).drop).toBe(
    'matt-flow：還沒到「動手做」。下一步是「把想法問清楚」：輸入 /grill-with-docs 加上你的想法；真的要跳過，先輸入 /matt-flow skip。',
  )
  expect(toasts).toEqual([])
  expect(await seen($, /進行中/)).toBe('還沒有進行中的功能')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/grill-with-docs/)

  // Skipping on purpose lets it through.
  expect(await flow($, 'skip')).toBe('↷ 跳過「把想法問清楚」→ 下一步 /implement')
  expect((await typed($, 'implement')).drop).toBeUndefined()
  expect(await card($)).toBe('▶ 3. 動手做（進行中）')
})

test('a step after the next one is dropped while building too, and the model jumping is told to hand over', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')

  expect((await typed($, 'retro')).drop).toMatch(/還沒到「複盤」。下一步是「檢查」：輸入 \/mattpocock-skills:code-review；/)
  expect((await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:retro' })).deny).toMatch(/還沒到「複盤」.*停下來/)
  expect(await card($)).toBe('▶ 3. 動手做（進行中）')
})

test('on the local tracker, spec and tickets wait for their files, written since the feature started; then the next command is offered', async ($, on) => {
  const { suggested, write } = engine(on, {
    files: { ...LOCAL, '.scratch/old/spec.md': '', '.scratch/old/issues/01-a.md': '' },
    stored: { level: 'intermediate' },
  })
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'to-spec')
  await turnEnds($)
  expect(await card($)).toBe('▶ 3. 寫成規格書（進行中）')
  expect(suggested).toEqual([])
  expect((await typed($, 'to-tickets')).drop).toBe(
    'matt-flow：「寫成規格書」還沒做完：還沒看到 .scratch/<功能>/spec.md。做完再輸入 /to-tickets；真的要跳過，先輸入 /matt-flow skip。',
  )

  write('.scratch/rail/spec.md')
  await turnEnds($)
  expect(await seen($, /進行中/)).toBe('功能「rail」進行中')
  expect(suggested).toEqual(['/to-tickets'])

  await typed($, 'to-tickets')
  await turnEnds($)
  expect(await card($)).toBe('▶ 4. 切成任務卡（進行中）')
  expect((await typed($, 'implement')).drop).toMatch(/還沒看到 \.scratch\/rail\/issues\/ 裡的任務卡/)
  write('.scratch/rail/issues/01-state-shape.md')
  await turnEnds($)
  expect(suggested).toEqual(['/to-tickets', '/implement'])
  await typed($, 'implement')
  expect(await card($)).toBe('▶ 5. 動手做（進行中）')
})

test("an old feature's ticket touched meanwhile is not this feature's tickets", async ($, on) => {
  const { write } = engine(on, { files: { ...LOCAL, '.scratch/old/issues/01-a.md': '' }, stored: { level: 'intermediate' } })
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'to-spec')
  write('.scratch/old/issues/01-a.md', 'Status: done')
  write('.scratch/rail/spec.md')
  await turnEnds($)
  await typed($, 'to-tickets')

  expect((await typed($, 'implement')).drop).toMatch(/還沒看到 \.scratch\/rail\/issues\//)
})

test('a beginner feature is not named or moved by a spec file written meanwhile', async ($, on) => {
  const { write } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  write('.scratch/rail/spec.md')
  await turnEnds($)

  expect(await seen($, /進行中/)).toBe('功能進行中')
  expect(await card($)).toBe('▶ 2. 把想法問清楚（進行中）')
})

test('a step outside the level runs and moves nothing: no toast, nothing offered', async ($, on) => {
  const { suggested, toasts } = engine(on, { files: GITHUB })
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  const shown = toasts.length
  expect((await typed($, 'to-spec')).drop).toBeUndefined()
  await turnEnds($)

  expect(toasts.length).toBe(shown)
  expect(suggested).toEqual([])
  expect(await card($)).toBe('▶ 3. 動手做（進行中）')
})

test('on the GitHub tracker, spec and tickets have no files to wait for: each passes once the next step starts', async ($, on) => {
  engine(on, { files: GITHUB, stored: { level: 'intermediate' } })
  await start($)
  for (const skill of ['grill-with-docs', 'to-spec', 'to-tickets', 'implement']) await typed($, skill)

  expect(await seen($, /切成任務卡/)).toBe('✔ 4. 切成任務卡')
  expect(await card($)).toBe('▶ 5. 動手做（進行中）')
  // No folder names the feature.
  expect(await seen($, /進行中/)).toBe('功能進行中')
})

test('a project set up this turn hands over to grilling', async ($, on) => {
  const { suggested, write } = engine(on, { files: {} })
  await start($)
  await typed($, 'setup-matt-pocock-skills')
  write(SETUP_FILE, '# Issue tracker: Local Markdown\n')
  await turnEnds($)

  expect(suggested).toEqual(['/grill-with-docs'])
  expect(await card($)).toBe('→ 2. 把想法問清楚')
})

test('a project never set up stays quiet: skills there start nothing', async ($, on) => {
  const { suggested, toasts } = engine(on, { files: {} })
  await start($)
  await typed($, 'grill-with-docs')
  await turnEnds($)

  expect(toasts).toEqual([])
  expect(suggested).toEqual([])
  expect(await seen($, /進行中/)).toBe('還沒有進行中的功能')
})

// Claude editing `path` under REPO, or outside it when absolute.
const edit = ($: Engine, path: string) =>
  $.tool.call({ tool: 'Edit', file_path: path.startsWith('/') ? path : `${REPO}/${path}`, old_string: 'a', new_string: 'b' })

test('with no feature under way, code is locked: the denial names /grill-with-docs, and offers it', async ($, on) => {
  const { suggested } = engine(on)
  await start($)

  const denied = (await edit($, 'hooks/register.tsx')).deny
  expect(denied).toMatch(/把想法問清楚/)
  expect(denied).toMatch(/\/grill-with-docs/)
  expect(denied).toMatch(/停下來交棒/)
  expect(denied).toMatch(/Bash/)
  expect((await $.tool.call({ tool: 'Write', file_path: `${REPO}/src/new.ts`, content: '' })).deny).toBeDefined()
  expect(
    (await $.tool.call({ tool: 'NotebookEdit', notebook_path: `${REPO}/play.ipynb`, new_source: '' })).deny,
  ).toBeDefined()
  await turnEnds($)
  expect(suggested).toEqual(['/grill-with-docs'])
})

test('during a feature, the denial names the next step on the way to building', async ($, on) => {
  engine(on, { files: GITHUB, stored: { level: 'intermediate' } })
  await start($)
  await typed($, 'grill-with-docs')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/to-spec/)

  await typed($, 'to-spec')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/to-tickets/)
})

test('code unlocks once the person types /implement', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/implement/)

  await typed($, 'implement')
  expect((await edit($, 'src/app.ts')).deny).toBeUndefined()
})

test('markdown, docs, the tracker folder and files outside the project are never locked', async ($, on) => {
  engine(on)
  await start($)

  for (const path of ['GLOSSARY.md', 'docs/adr/0001.ts', '.scratch/rail/notes.txt', '/elsewhere/app.ts']) {
    expect((await edit($, path)).deny).toBeUndefined()
  }
})

test('a project never set up locks nothing', async ($, on) => {
  engine(on, { files: {} })
  await start($)

  expect((await edit($, 'src/app.ts')).deny).toBeUndefined()
})

const bash = ($: Engine, command: string) => $.tool.call({ tool: 'Bash', command })

test('a beginner building cannot commit until code-review runs, then every later commit goes', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')

  expect((await bash($, 'git commit -m "wip"')).deny).toMatch(/code-review/)
  expect((await bash($, `git -C ${REPO} commit -m "wip"`)).deny).toMatch(/code-review/)
  for (const options of ['--no-pager -c user.name=x --git-dir=.git', '--work-tree /w', '--git-dir repo/.git', `-C "${REPO}/a b"`]) {
    expect((await bash($, `git ${options} commit -m "wip"`)).deny).toMatch(/code-review/)
  }
  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:code-review' })
  expect((await bash($, 'git commit -m "feat"')).deny).toBeUndefined()
  expect((await bash($, 'git commit -m "fix review"')).deny).toBeUndefined()
})

test('an intermediate building waits for code-review too, the person typing it counts', async ($, on) => {
  engine(on, { files: GITHUB, stored: { level: 'intermediate' } })
  await start($)
  for (const skill of ['grill-with-docs', 'to-spec', 'to-tickets', 'implement']) await typed($, skill)

  expect((await bash($, 'git commit -m "wip"')).deny).toMatch(/code-review/)
  await typed($, 'mattpocock-skills:code-review')
  expect((await bash($, 'git commit -m "feat"')).deny).toBeUndefined()
})

test('a denied commit offers the review command, and each /implement the person types wants its own review', async ($, on) => {
  const { suggested } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  await turnEnds($)

  const offered = suggested.length
  expect((await bash($, 'git commit -m "wip"')).deny).toBeDefined()
  await turnEnds($)
  expect(suggested.slice(offered)).toEqual(['/mattpocock-skills:code-review'])
  await typed($, 'mattpocock-skills:code-review')
  expect((await bash($, 'git commit -m "first"')).deny).toBeUndefined()
  await typed($, 'implement')
  expect((await bash($, 'git commit -m "second"')).deny).toMatch(/code-review/)
})

test("the commit gate holds this project's commits only: one sent elsewhere by an absolute path goes", async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')

  for (const command of [
    'git -C /elsewhere/repo commit -m "x"',
    'cd /elsewhere/repo && git commit -m "x"',
    'cd "/elsewhere/a b"; git commit -m "x"',
    'mkdir -p /elsewhere/x\ncd /elsewhere/x && git init -q && git commit -m "x"',
    '(cd /elsewhere/x && git commit -m "x")',
  ]) {
    expect((await bash($, command)).deny).toBeUndefined()
  }
  // Each commit's own folder decides: this project's, a relative one, ~ or a variable, or one the path only seems to leave.
  for (const command of [
    `git -C ${REPO}/hooks commit -m "x"`,
    `cd ${REPO} && git commit -m "x"`,
    'cd sub && git commit -m "x"',
    'cd ~/x && git commit -m "x"',
    'cd "$TMPDIR/x" && git commit -m "x"',
    `cd /elsewhere/repo && git commit -m "x" && cd ${REPO} && git commit -m "y"`,
    'git commit -m "x" && cd /elsewhere',
    'git -C /elsewhere status && git commit -m "x"',
    'git add . && make -C /elsewhere/b && git commit -m "x"',
    'git commit -m "add the -C /tmp flag"',
    `git -C /elsewhere/..${REPO} commit -m "x"`,
  ]) {
    expect((await bash($, command)).deny).toMatch(/code-review/)
  }
})

test('commits outside building, and Bash that does not commit, always go', async ($, on) => {
  engine(on)
  await start($)
  expect((await bash($, 'git commit -m "docs"')).deny).toBeUndefined()

  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  for (const command of ['git status', 'git log --grep commit', 'npm test']) {
    expect((await bash($, command)).deny).toBeUndefined()
  }
})

test('the expert commits freely: /implement-spec reviews its own work', async ($, on) => {
  engine(on, { files: GITHUB, stored: { level: 'expert' } })
  await start($)
  for (const skill of ['grill-with-docs', 'to-spec', 'to-tickets', 'implement-spec']) await typed($, skill)

  expect((await bash($, 'git commit -m "wip"')).deny).toBeUndefined()
})

test('a subagent finishing does not take the hand-over meant for the person', async ($, on) => {
  const { suggested } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:code-review' })
  await $.turn.complete({ answer: '', durationMs: 0, isAborted: false, turnId: 's', reason: 'answer', agentId: 'a1' })
  expect(suggested).toEqual([])

  await turnEnds($)
  expect(suggested).toEqual(['/retro'])
})

test('a subagent running code-review does not unlock the commit', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:code-review', agentId: 'a1' })

  expect((await bash($, 'git commit -m "wip"')).deny).toMatch(/code-review/)
})

test('below expert, /implement-spec lets its subagents commit; the main thread still waits for code-review', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement-spec')

  expect((await $.tool.call({ tool: 'Bash', command: 'git commit -m "ticket"', agentId: 'a1' })).deny).toBeUndefined()
  expect((await bash($, 'git commit -m "merge"')).deny).toMatch(/code-review/)
})

test('a gate that breaks still holds code and commits, and lets everything else go', async ($, on) => {
  let isBroken = false
  // Once broken, progress reads back as a corrupt state would.
  on('state.get', { plugin: 'matt-flow', key: 'progress' }, (_, e, next) =>
    isBroken ? ({ value: null, version: 1 } as never) : next(e),
  )
  engine(on)
  await start($)
  isBroken = true

  expect((await edit($, 'src/app.ts')).deny).toMatch(/關卡出錯/)
  expect((await bash($, 'git commit -m "wip"')).deny).toMatch(/關卡出錯/)
  expect((await edit($, 'README.md')).deny).toBeUndefined()
  expect((await bash($, 'ls')).deny).toBeUndefined()
})

// A prompt the person types; resolves the context the model reads beside it.
const said = async ($: Engine, text: string) =>
  (await $.prompt.submit({ text, wait: false, origin: { kind: 'composer' } })).context ?? []

// What rides along with the person's next prompt, as one text.
const rail = async ($: Engine) => (await said($, 'hi')).join()

test('with no feature, the rail says code is locked behind /grill-with-docs, what still goes, and the rules', async ($, on) => {
  engine(on)
  await start($)

  const text = await rail($)
  expect(text).toMatch(/還沒有進行中的功能/)
  expect(text).toMatch(/新手/)
  expect(text).toMatch(/下一步：把想法問清楚（\/grill-with-docs）/)
  expect(text).toMatch(/改程式碼（Edit.*\/grill-with-docs/)
  expect(text).toMatch(/仍可以：讀檔、跑測試、改 markdown/)
  expect(text).not.toMatch(/git commit/)
  expect(text).toMatch(/停下來/)
  expect(text).toMatch(/除了下一步的指令和 \/matt-flow，不要主動建議流程指令/)
  expect(text).toMatch(/\/ask-matt/)
  expect(text).toMatch(/Bash/)
})

test("the rail lets Claude name Matt's ways in when no feature is under way or the person asks what to do", async ($, on) => {
  engine(on)
  await start($)

  const text = await rail($)
  expect(text).toMatch(/沒有進行中的功能、或人問該怎麼辦時，可以點名 Matt 的入口/)
  for (const entry of ['/triage', '/diagnosing-bugs', '/wayfinder', '/improve-codebase-architecture', '/to-questionnaire']) {
    expect(text).toContain(entry)
  }
})

test('once the spec is written, the rail names the feature and points at /to-tickets', async ($, on) => {
  const { write } = engine(on, { stored: { level: 'intermediate' } })
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'to-spec')
  write('.scratch/rail/spec.md')
  await turnEnds($)

  const text = await rail($)
  expect(text).toMatch(/「rail」/)
  expect(text).toMatch(/進階/)
  expect(text).toMatch(/下一步：切成任務卡（\/to-tickets）/)
  expect(text).toMatch(/改程式碼（Edit.*\/to-tickets/)
})

test('while building, the rail locks only the commit, until code-review runs', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')

  const text = (await typed($, 'implement')).context?.join()
  expect(text).not.toMatch(/改程式碼（Edit/)
  expect(text).not.toMatch(/仍可以/)
  expect(text).toMatch(/git commit.*code-review/)
  expect((await typed($, 'mattpocock-skills:code-review')).context?.join()).toMatch(/現在會被擋的動作：沒有/)
})

test('the rail rides along with a prompt only when it changed', async ($, on) => {
  engine(on)
  await start($)

  expect(await rail($)).toMatch(/# matt-flow 軌道[^]*下一步：把想法問清楚/)
  expect(await said($, 'hi again')).toEqual([])
  expect((await typed($, 'grill-with-docs')).context?.join()).toMatch(/下一步：動手做/)
  expect(await said($, 'and again')).toEqual([])
})

test('while grilling, the rail names building as the next step, never as the step under way', async ($, on) => {
  engine(on)
  await start($)

  const text = (await typed($, 'grill-with-docs')).context?.join()
  expect(text).toMatch(/下一步：動手做（\/implement）/)
  expect(text).toMatch(/進行中：把想法問清楚（問題問完才算做完，由人決定什麼時候往下）/)
  expect(text).toMatch(/流程的 skill 只能照順序跑，跳步的會被擋下；要跳過一步，由人輸入 \/matt-flow skip/)
  expect(text).not.toMatch(/目前的步驟/)
})

const message = (role: 'user' | 'assistant', text: string): SessionMessage => ({ role, text, toolUses: [] })

test('once the conversation is compacted, the next prompt carries the rail again', async ($, on) => {
  const { conversation } = engine(on)
  await start($)
  await said($, 'hi')
  conversation.push(message('user', 'hi'), message('assistant', 'hello'))
  await turnEnds($)
  expect(await said($, 'and again')).toEqual([])

  // A compaction puts its summary first; the conversation need not get any shorter.
  conversation.splice(0, 1, message('user', 'This session is being continued from a previous conversation.'))
  expect(await rail($)).toMatch(/# matt-flow 軌道/)
})

test('a rewind or /clear takes the rail away, and the next prompt carries it again', async ($, on) => {
  const { conversation } = engine(on)
  await start($)
  await said($, 'hi')
  conversation.push(message('user', 'hi'), message('assistant', 'hello'))
  await turnEnds($)
  conversation.push(message('user', 'more'), message('assistant', 'sure'))
  await turnEnds($)

  conversation.splice(2)
  expect(await rail($)).toMatch(/# matt-flow 軌道/)
  expect(await said($, 'and again')).toEqual([])
  conversation.splice(0)
  expect(await rail($)).toMatch(/# matt-flow 軌道/)
})

// The engine dropping the session's state as /clear does: every value the plugin holds reads as never set, until written again.
const clearable = (on: Parameters<TestBody>[1]) => {
  const held = new Set<string>()
  const dropped = new Set<string>()
  on('state.get', { plugin: 'matt-flow' }, (_, e, next) => {
    held.add(e.key)

    return dropped.has(e.key) ? next(e).then(read => ({ value: { value: undefined, version: read.value?.version ?? 0 } })) : next(e)
  })
  on('state.set', { plugin: 'matt-flow' }, (_, e, next) => {
    held.add(e.key)
    dropped.delete(e.key)

    return next(e)
  })

  return () => held.forEach(key => dropped.add(key))
}

test('after /clear, the next tool call or prompt finds the project again: its locks, its rail, its pane', async ($, on) => {
  const clear = clearable(on)
  const { conversation } = engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await $.session.end({ reason: 'clear', sessionId: 's', resume: { id: 's' } })
  clear()
  conversation.splice(0)

  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/implement/)
  expect(await rail($)).toMatch(/下一步：動手做/)
  expect(await seen($, /進行中/)).toBe('功能進行中')
})

test('after /clear, the commit gate holds too', async ($, on) => {
  const clear = clearable(on)
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  await $.session.end({ reason: 'clear', sessionId: 's', resume: { id: 's' } })
  clear()

  expect((await bash($, 'git commit -m "wip"')).deny).toMatch(/code-review/)
})

test('a project never set up gets no rail beside its prompts', async ($, on) => {
  engine(on, { files: {} })
  await start($)

  expect(await said($, 'hi')).toEqual([])
})

// Progress another session of the project saved: grilling passed, building next.
const GRILLED = {
  level: 'beginner',
  steps: { grill: 'passed' },
  feature: { name: null, since: 1 },
  isReviewed: false,
  isOff: false,
  features: 0,
}

test('a turn that changed nothing leaves alone the progress another session saved', async ($, on) => {
  const { store } = engine(on)
  await start($)
  store.set(`progress:${REPO}`, GRILLED)
  await turnEnds($)

  expect(store.get(`progress:${REPO}`)).toEqual(GRILLED)
})

test('each prompt reads the progress afresh: a step another session passed shows here', async ($, on) => {
  const { store } = engine(on)
  await start($)
  store.set(`progress:${REPO}`, GRILLED)

  expect((await said($, 'hi')).join()).toMatch(/下一步：動手做/)
})

test('a session opened in a subfolder works on its project: its progress, its locks', async ($, on) => {
  engine(on, { stored: { level: 'intermediate' } })
  await $.session.start({ cwd: `${REPO}/hooks`, surface: 'terminal', isInteractive: true })

  expect((await said($, 'hi')).join()).toMatch(/等級：進階/)
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/grill-with-docs/)
})

// The person typing `/matt-flow args`; resolves the line it answers.
const flow = async ($: Engine, args = '') =>
  (
    await $.command.run({
      command: 'matt-flow',
      args,
      origin: { kind: 'composer' },
      presentation: { isFullscreen: true, columns: 120 },
    })
  ).text

test('/matt-flow alone still opens and closes the pane; an unknown argument shows the usage', async ($, on) => {
  engine(on)
  await start($)

  expect(await flow($)).toMatch(/已打開/)
  expect(await flow($)).toMatch(/已關閉/)
  expect(await flow($, 'nope')).toMatch(/skip.*end.*off.*on/)
})

test('/matt-flow skip skips the step the flow stands on, and says what is next', async ($, on) => {
  engine(on)
  await start($)

  expect(await flow($, 'skip')).toBe('↷ 跳過「把想法問清楚」→ 下一步 /implement')
  expect(await seen($, /進行中/)).toBe('功能進行中')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/implement/)
  expect(await flow($, 'skip')).toBe('↷ 跳過「動手做」→ 下一步 /mattpocock-skills:code-review')
  expect((await edit($, 'src/app.ts')).deny).toBeUndefined()
})

test('a feature ended before its retro is aborted and does not count; one ended with its retro under way is done', async ($, on) => {
  engine(on)
  await start($)
  expect(await flow($, 'end')).toBe('沒有進行中的功能 → 下一步 /grill-with-docs')

  await typed($, 'grill-with-docs')
  expect(await flow($, 'end')).toBe('⏹ 功能中止：沒做到複盤，不算完成 → 下一個從 /grill-with-docs 開始')
  expect(await seen($, /進行中/)).toBe('還沒有進行中的功能')
  expect(await seen($, /已完成/)).toMatch(/已完成 0 個功能/)

  // Skipping a retro never started leaves it undone.
  for (const step of ['把想法問清楚', '動手做', '檢查']) expect(await flow($, 'skip')).toMatch(step)
  expect(await flow($, 'skip')).toBe('⏹ 功能中止：沒做到複盤，不算完成 → 下一個從 /grill-with-docs 開始')

  // A retro under way ran: skipping it, like ending the feature, finishes the feature done.
  for (const skill of ['grill-with-docs', 'implement', 'mattpocock-skills:code-review', 'retro']) await typed($, skill)
  expect(await flow($, 'skip')).toBe('🎉 功能結束，已完成 1 個功能 → 下一個從 /grill-with-docs 開始')
})

test('/matt-flow all lists every project with progress, the longest left first, and marks a feature left over 3 days', async ($, on) => {
  const { at } = engine(on, {
    others: {
      '/Users/me/billing': {
        level: 'intermediate',
        steps: { grill: 'passed', spec: 'passed' },
        feature: { name: 'invoices', since: 0 },
        isReviewed: false,
        isOff: false,
        features: 2,
      },
      '/Users/me/finished': { level: 'beginner', steps: {}, feature: null, isReviewed: false, isOff: false, features: 1 },
      '/private/tmp/scratch': { level: 'beginner', steps: {}, feature: null, isReviewed: false, isOff: false, features: 0 },
    },
  })
  at(5 * DAY)
  await start($)
  await typed($, 'grill-with-docs')

  expect(await flow($, 'all')).toBe(
    [
      '⚠ ~/billing · 🚀 進階 · 功能「invoices」進行中 · 下一步 /to-tickets · 5 天沒動',
      '  /repo · 🌱 新手 · 功能進行中 · 下一步 /implement · 不到 1 天沒動',
      '  ~/finished · 🌱 新手 · 還沒有進行中的功能 · 下一步 /grill-with-docs · 已完成 1 個功能',
      '最近 7 天結束的功能：沒有',
    ].join('\n'),
  )
})

test('the overview lists the features ended in the last 7 days, how long each took and what it skipped, the aborted apart', async ($, on) => {
  const { at } = engine(on)
  at(DAY)
  await start($)
  for (const skill of ['grill-with-docs', 'implement']) await typed($, skill)
  // Skipping the review on purpose: the build is not held for one.
  await flow($, 'skip')
  expect((await typed($, 'retro')).drop).toBeUndefined()
  at(3 * DAY)
  await flow($, 'end')
  await typed($, 'grill-with-docs')
  at(4 * DAY)
  await flow($, 'end')

  const ended = async () => (await flow($, 'all'))?.split('\n').slice(-2)
  expect(await ended()).toEqual([
    '最近 7 天結束的功能：/repo（2 天，跳過「檢查」）',
    '最近 7 天中止的功能：/repo（1 天）',
  ])
  at(12 * DAY)
  expect(await ended()).toEqual([
    '  /repo · 🌱 新手 · 還沒有進行中的功能 · 下一步 /grill-with-docs · 8 天沒動 · 已完成 1 個功能',
    '最近 7 天結束的功能：沒有',
  ])
})

test('a skill that moves nothing, a level change, or the rail turned off and on leaves the time the flow last moved', async ($, on) => {
  const { at } = engine(on)
  at(0)
  await start($)
  await typed($, 'grill-with-docs')
  at(4 * DAY)
  await $.tool.call({ tool: 'Skill', skill: 'mattpocock-skills:grilling' })
  await flow($, 'off')
  await flow($, 'on')
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  await ui.press({ key: 'level-intermediate' })
  await ui.unmount()

  expect((await flow($, 'all'))?.split('\n')[0]).toBe('⚠ /repo · 🚀 進階 · 功能進行中 · 下一步 /to-spec · 4 天沒動')
})

test('/matt-flow off quiets the gates and takes the rail back in this project; on brings them back', async ($, on) => {
  engine(on)
  await start($)
  expect(await rail($)).toMatch(/# matt-flow 軌道/)

  expect(await flow($, 'off')).toMatch(/關掉了.*\/matt-flow on/)
  expect((await edit($, 'src/app.ts')).deny).toBeUndefined()
  expect(await rail($)).toMatch(/先前的規矩不再適用/)
  expect(await said($, 'hi again')).toEqual([])
  await typed($, 'grill-with-docs')
  await typed($, 'implement')
  expect((await bash($, 'git commit -m "wip"')).deny).toBeUndefined()

  expect(await flow($, 'on')).toBe('軌道打開了 → 下一步 /grill-with-docs')
  expect((await edit($, 'src/app.ts')).deny).toMatch(/\/grill-with-docs/)
  expect(await rail($)).toMatch(/# matt-flow 軌道/)
})

test('in a project never set up, the subcommands say why the rail does nothing', async ($, on) => {
  engine(on, { files: {} })
  await start($)

  expect(await flow($, 'skip')).toMatch(/還沒設定.*\/setup-matt-pocock-skills/)
})

test('an intermediate building hands over both ways: the next ticket, or the retro once all are done', async ($, on) => {
  const { suggested, toasts } = engine(on, { files: GITHUB, stored: { level: 'intermediate' } })
  await start($)
  for (const skill of ['grill-with-docs', 'to-spec', 'to-tickets']) await typed($, skill)
  await turnEnds($)
  const offered = suggested.length
  const text = (await typed($, 'implement')).context?.join()
  await turnEnds($)

  expect(toasts.at(-1)).toBe(
    '✔ 切成任務卡 通過 · ▶ 開始「動手做」：寫完之後，還有任務卡就 /clear 後 /implement 下一張，都做好了再 /retro',
  )
  expect(suggested.slice(offered)).toEqual([])
  expect(text).toMatch(/還有任務卡就 \/clear 後 \/implement 下一張，都做好了再 \/retro/)

  // The next ticket is the step under way again; the retro waits for this build's code-review.
  expect((await typed($, 'implement')).drop).toBeUndefined()
  expect((await typed($, 'retro')).drop).toMatch(/「動手做」還沒做完：這次動手做還沒跑過 code-review。做完再輸入 \/retro/)
  await typed($, 'mattpocock-skills:code-review')
  expect((await typed($, 'retro')).drop).toBeUndefined()
  expect(await card($)).toBe('▶ 6. 複盤（進行中）')
})

test("an expert's /implement-spec hands over to /pr, not to another /implement", async ($, on) => {
  const { toasts } = engine(on, { files: GITHUB, stored: { level: 'expert' } })
  await start($)
  for (const skill of ['grill-with-docs', 'to-spec', 'to-tickets', 'implement-spec']) await typed($, skill)

  expect(toasts.at(-1)).toBe('✔ 切成任務卡 通過 · ▶ 開始「讓 AI 並行開發」：分身都合併之後，下一步 /pr')
})

test('the feature takes the title of the first commit Claude makes while building, when no spec named it', async ($, on) => {
  engine(on, { commit: 'Add a login page' })
  await start($)
  for (const skill of ['grill-with-docs', 'implement', 'mattpocock-skills:code-review']) await typed($, skill)
  await bash($, 'git commit -m "Add a login page"')

  expect(await seen($, /進行中/)).toBe('功能「Add a login page」進行中')
  expect((await said($, 'hi')).join()).toMatch(/功能「Add a login page」進行中/)
})

test('a commit before building, one denied, or one that moved nothing names nothing', async ($, on) => {
  engine(on)
  await start($)
  await typed($, 'grill-with-docs')
  await bash($, 'git commit -m "Docs: a glossary"')
  await typed($, 'implement')
  await bash($, 'git commit -m "wip"')
  await typed($, 'mattpocock-skills:code-review')
  await bash($, 'git commit --dry-run -m "wip"')

  expect(await seen($, /進行中/)).toBe('功能進行中')
})
