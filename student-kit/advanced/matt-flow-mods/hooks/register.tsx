import { atom, read, update } from 'claude-code'
import type { EngineInterface, FsEntry, Register } from 'claude-code'

import type { FeatureRecord, Level, Progress, StepState } from '../types'

const PANE = 'matt-flow'
const TITLE = '✦ Matt 導航'
// ask-matt's smart zone: compact at a phase boundary before crossing it.
const SMART_ZONE = 150_000
// Written by /setup-matt-pocock-skills: a project holding it is set up.
const SETUP_FILE = 'docs/agents/issue-tracker.md'
// Where the local markdown tracker keeps a folder per feature.
const SCRATCH = '.scratch'

type Step = { title: string; command: string; skills: string[]; what: string; tip: string; criterion: string }

const STEPS = {
  setup: {
    title: '設定專案',
    command: '/setup-matt-pocock-skills',
    // Passes on SETUP_FILE alone.
    skills: [] as string[],
    what: '告訴 AI 任務放哪裡（GitHub 或本地檔案）、文件放哪裡。每個專案只要做一次。',
    tip: '做過就會自動通過，之後每個新功能都從下一步開始。',
    criterion: '設定好',
  },
  grill: {
    title: '把想法問清楚',
    command: '/grill-with-docs',
    skills: ['grill-with-docs', 'grill-me', 'grilling'],
    what: 'AI 會一直問你問題，直到需求沒有模糊的地方，並把專有名詞記進 GLOSSARY.md。',
    tip: '沒有共同的詞彙表，AI 就會把「客戶」和「使用者」搞混。',
    criterion: '問題問完',
  },
  spec: {
    title: '寫成規格書',
    command: '/to-spec',
    skills: ['to-spec'],
    what: '把剛剛聊清楚的內容整理成一份規格，發到你的 issue tracker。這步不會再問你問題。',
    tip: '從問清楚到切任務卡，都留在同一段對話裡，中間不要 /clear。',
    criterion: '規格書寫出來',
  },
  tickets: {
    title: '切成任務卡',
    command: '/to-tickets',
    skills: ['to-tickets'],
    what: '把規格切成一張張能獨立完成的任務卡，每張寫明「被哪幾張卡住」。',
    tip: '卡片邊界切清楚，之後同時開工才不會互相改到同一個檔案。',
    criterion: '任務卡切好',
  },
  build: {
    title: '動手做',
    command: '/implement',
    skills: ['implement'],
    what: 'AI 用測試先行的方式一小塊一小塊寫，寫完自己跑檢查再 commit。',
    tip: '任務卡很多的話，一次做一張，每張做完就 /clear。',
    criterion: '寫完',
  },
  review: {
    title: '檢查',
    // The full name: Claude Code has a /code-review of its own, which matt-flow cannot see.
    command: '/mattpocock-skills:code-review',
    skills: ['code-review'],
    what: '對照專案規範和規格，從兩個方向檢查這次的改動。/implement 通常會自己跑這步。',
    tip: '檢查的 AI 只看 diff，不用重新摸索整個專案，所以抓得準。',
    criterion: '檢查完',
  },
  parallel: {
    title: '讓 AI 並行開發',
    command: '/implement-spec',
    skills: ['implement-spec'],
    what: '沒被卡住的任務卡會同時交給好幾個分身去做，最後全部合進同一條整合分支。',
    tip: '並行時打架，通常不是 AI 笨，是任務卡的邊界切得太模糊。',
    criterion: '分身都合併',
  },
  pr: {
    title: '開 PR 附證據',
    command: '/pr',
    skills: ['pr'],
    what: 'PR 說明要有最小的架構圖、改動前後的證據，以及這是單向門還是雙向門。',
    tip: '人只需要親自看單向門的 PR：改了就回不去的那種。',
    criterion: 'PR 開好',
  },
  retro: {
    title: '複盤',
    command: '/retro',
    skills: ['retro'],
    what: '回頭看這次哪裡卡住、哪裡浪費，建議怎麼改環境：自動檢查、規範、工具。',
    tip: '修環境，不修 prompt：與其每次提醒 AI，不如裝一把兒童安全鎖。',
    criterion: '複盤建議的環境改完',
  },
} satisfies Record<string, Step>

type StepKey = keyof typeof STEPS

const LEVELS: Record<Level, { icon: string; name: string; goal: string; steps: StepKey[] }> = {
  beginner: {
    icon: '🌱',
    name: '新手',
    goal: '一次做完一個小功能',
    steps: ['setup', 'grill', 'build', 'review', 'retro'],
  },
  intermediate: {
    icon: '🚀',
    name: '進階',
    goal: '大功能，分好幾次對話做完',
    steps: ['setup', 'grill', 'spec', 'tickets', 'build', 'retro'],
  },
  expert: {
    icon: '👑',
    name: '高手',
    goal: '讓 AI 同時做好幾件事',
    steps: ['setup', 'grill', 'spec', 'tickets', 'parallel', 'pr', 'retro'],
  },
}
const ORDER: Level[] = ['beginner', 'intermediate', 'expert']
// Each level's building: only the person starts it.
const BUILD: StepKey[] = ['build', 'parallel']
// The steps after building: typed before it, they run and move nothing.
const LATE: StepKey[] = ['review', 'pr', 'retro']
// With the local tracker these are done once their files are written.
const ARTIFACTS: StepKey[] = ['spec', 'tickets']

const FRESH: Progress = {
  level: 'beginner',
  steps: {},
  feature: null,
  isReviewed: false,
  isOff: false,
  features: 0,
  records: [],
  movedAt: null,
}

const project = atom({ plugin: 'matt-flow', key: 'project' } as const, null)
const progress = atom({ plugin: 'matt-flow', key: 'progress' } as const, FRESH)
const isSetUp = atom({ plugin: 'matt-flow', key: 'isSetUp' } as const, false)
const tokens = atom({ plugin: 'matt-flow', key: 'tokens' } as const, null)

// The next step's command, offered in the prompt box once the turn ends.
let suggestion: string | undefined
// The step last seen done and offered its next command, as `feature start:step`: offered once, not every turn.
let offered: string | undefined
// The rail last sent beside a prompt: it rides along again only once it changes, or once the
// conversation lost it. Not in the system prompt: a managed hook may send prompt.compose past user
// plugins, as it does skill.prompt.
let sent: string | undefined
// The conversation as last seen: its first message when the rail went out (a compaction replaces it),
// and how many messages it held (a rewind or /clear leaves fewer). The rail is not in the messages
// a plugin reads, and the managed security plugin sends session.compact past this one.
let seen: { head?: string; count: number } = { count: 0 }
// The project the session started in: /clear drops the session's state, and no session.start follows to load it again.
let home: string | null = null

const stateOf = (p: Progress, key: StepKey, setUp: boolean): StepState | undefined =>
  key === 'setup' && setUp ? 'passed' : p.steps[key]
// The first step with no state: the one whose command the person types next.
const nextStep = (p: Progress, setUp: boolean) => LEVELS[p.level].steps.find(key => !stateOf(p, key, setUp))
// The step under way: started by its command, it passes once the next one starts.
const underWay = (p: Progress) => LEVELS[p.level].steps.find(key => p.steps[key] === 'underWay')
const mark = (p: Progress, keys: StepKey[], state: StepState): Progress => ({
  ...p,
  steps: { ...p.steps, ...Object.fromEntries(keys.map(key => [key, state] as const)) },
})
// Code opens once building starts, and stays open until the feature ends: the retro's changes to the environment too.
const isBuilding = (p: Progress) => BUILD.some(key => p.steps[key])
// The step whose command unlocks code: grilling without a feature, else the next one.
const unlockStep = (p: Progress) => (p.feature && nextStep(p, true)) || 'grill'
// A `git commit`, past the options git takes first (`git -C dir commit`, `git --no-pager commit`).
// ponytail: knows the options that take a separate value by name; an alias (`git ci`) or another such option gets past, add it when one shows.
const GIT_COMMIT =
  /\bgit((?:\s+(?:(?:-[cC]|--(?:git-dir|work-tree|namespace|exec-path|config-env))\s+(?:"[^"]*"|'[^']*'|\S+)|--?[\w-]+(?:=\S+)?))*)\s+commit\b/
const unquote = (word: string) => word.replace(/^(["'])(.*)\1$/, '$2')
// An absolute path with `.` and `..` folded away, so `/elsewhere/../repo` reads as `/repo`.
const fold = (path: string) =>
  `/${path.split('/').reduce<string[]>((parts, part) => (part === '..' ? parts.slice(0, -1) : part === '' || part === '.' ? parts : [...parts, part]), []).join('/')}`
// Whether every commit in a command runs, by its own `git -C` or a `cd` before it, in a folder outside the project:
// the gate holds this project's commits alone.
// ponytail: a relative, `~` or `$VAR` folder counts as the project, and only `; & | ( )` and new lines part commands; resolve more when that blocks real work elsewhere.
const isElsewhere = (root: string, command: string) => {
  let dir: string | undefined
  let commits = 0
  for (const part of command.split(/&&|\|\||[;&|()\n]/)) {
    const cd = /^\s*cd\s+("[^"]*"|'[^']*'|\S+)\s*$/.exec(part)?.[1]
    if (cd !== undefined) dir = unquote(cd)
    const options = GIT_COMMIT.exec(part)?.[1]
    if (options === undefined) continue
    commits += 1
    const own = /-C\s+("[^"]*"|'[^']*'|\S+)/.exec(options)?.[1]
    const at = own === undefined ? dir : unquote(own)
    if (at === undefined || !at.startsWith('/') || `${fold(at)}/`.startsWith(`${root}/`)) return false
  }

  return commits > 0
}
// Beginners and intermediates commit what they build only after code-review has run.
const isCommitLocked = (p: Progress) => p.level !== 'expert' && isBuilding(p) && !p.isReviewed
// The retro under way ends with this: the feature is done then.
const END = '/matt-flow end'
// Intermediate building goes a ticket at a time: until the person starts the retro, the next is either.
const NEXT_TICKET = '還有任務卡就 /clear 後 /implement 下一張，都做好了再 /retro'
const isTicketByTicket = (p: Progress) => p.level === 'intermediate' && p.steps.build === 'underWay'
// The retro under way holds the feature open, code unlocked, until the person ends it.
const isInRetro = (p: Progress) => underWay(p) === 'retro'
// Matt's ways in for work that is no feature yet: Claude may name them, for the person to type.
const WAYS_IN =
  '/triage（別人丟來的 bug 或需求）、/diagnosing-bugs（東西壞了）、/wayfinder（又大又模糊的工作）、/improve-codebase-architecture（整理架構）、/to-questionnaire（答案在別人腦袋裡）'
// The command the person types next; intermediate building names both ways on.
const nextOf = (p: Progress) =>
  isTicketByTicket(p)
    ? '/implement 下一張，或 /retro'
    : isInRetro(p)
      ? END
      : STEPS[nextStep(p, true) ?? 'grill'].command
const thenOf = (p: Progress) => (isTicketByTicket(p) ? NEXT_TICKET : `下一步 ${nextOf(p)}`)
const DAY = 86_400_000
// A feature under way idle longer than this is marked in the overview.
const LONG_IDLE = 3 * DAY
// The overview lists the features ended within this long.
const LATELY = 7 * DAY
const days = (ms: number) => (ms < DAY ? '不到 1 天' : `${Math.floor(ms / DAY)} 天`)
// When the flow last moved on: a record older than movedAt has only its feature's start.
const movedOf = (p: Progress) => p.movedAt ?? p.feature?.since ?? null
// How long the project has been idle, as said; nothing while no time is known.
const idleFor = (p: Progress, now: number) => {
  const moved = movedOf(p)

  return moved === null ? [] : [`${days(now - moved)}沒動`]
}
// A project's root as the overview names it, the home folder as `~`.
// ponytail: guesses the home folder from the path, so /Users/Shared/app reads as ~/app; ask the engine if it ever tells.
const where = (root: string) => root.replace(/^\/(?:Users|home)\/[^/]+/, '~')
// Steps by their titles, as toasts and the overview quote them; a key no step has any more stays as it is.
const titled = (keys: string[]) => keys.map(key => `「${STEPS[key as StepKey]?.title ?? key}」`).join('')
const skippedOf = (p: Progress) => Object.keys(p.steps).filter(key => p.steps[key] === 'skipped')
const recordLine = (root: string, { name, since, end, skipped }: FeatureRecord) =>
  `${where(root)}${name === null ? '' : `「${name}」`}（${days(end - since)}${skipped.length === 0 ? '' : `，跳過${titled(skipped)}`}）`
const featureLine = ({ feature }: Progress) =>
  feature === null ? '還沒有進行中的功能' : feature.name === null ? '功能進行中' : `功能「${feature.name}」進行中`
// The way past a refusal, which a person who means it takes.
const SKIP_WAY = '真的要跳過，先輸入 /matt-flow skip。'
// What refusing a jump says: the step the flow is at, and the way past it.
const aheadLine = (key: StepKey, next: StepKey) =>
  `matt-flow：還沒到「${STEPS[key].title}」。下一步是「${STEPS[next].title}」：輸入 ${STEPS[next].command}${next === 'grill' ? ' 加上你的想法' : ''}；${SKIP_WAY}`
// What a move the model tried adds: the person decides, so Claude hands over.
const HAND_OVER = '停下來交棒：把這件事和該打的指令告訴人，然後結束這次回覆。'
// What isCode guards: a project file that is not markdown, outside the tracker's folder and docs.
// ponytail: `..` is not resolved; the gate keeps Claude on the flow, it is no sandbox (Bash gets past it anyway).
const isCode = (root: string, path: string) =>
  path.startsWith(`${root}/`) &&
  !/\.md$/i.test(path) &&
  ![`${SCRATCH}/`, 'docs/'].some(dir => path.startsWith(`${root}/${dir}`))
// What a gate that throws still holds: it cannot tell the project, so it judges the path alone.
const mayBeCode = (path: string) => !/\.md$/i.test(path) && ![`/${SCRATCH}/`, '/docs/'].some(dir => path.includes(dir))
const BROKEN =
  "matt-flow：關卡出錯，先擋下改程式碼和 commit。停下來告訴人：把 matt-flow 退回上一個能用的版本（git -C ~/.claude/skills/matt-flow reset --hard 'HEAD@{1}'），或把它移出 skills 資料夾；/matt-flow off 讀的是同一份狀態，可能也沒用。"
// Ends the feature: done once its retro ran, else aborted. Either leaves its record; only a done one counts,
// and every step but setup starts over.
const finish = (p: Progress, now: number, isDone: boolean): Progress => ({
  ...p,
  steps: p.steps.setup ? { setup: p.steps.setup } : {},
  feature: null,
  isReviewed: false,
  features: p.features + (isDone ? 1 : 0),
  records:
    p.feature === null
      ? p.records
      : [
          ...p.records,
          { name: p.feature.name, since: p.feature.since, end: now, skipped: skippedOf(p), ...(isDone ? {} : { isAborted: true as const }) },
        ],
})
const bar = (part: number, width: number) => Math.max(0, Math.min(width, Math.round(part * width)))

// Writes the progress once it changed. A move of the flow times it; a level changed or the rail switched is none.
async function save($: EngineInterface) {
  const key = await read($, project)
  if (key === null) return
  const now = await $.clock.now()
  const stored = restore((await $.store.get(`progress:${key}`)) as Saved | undefined, now)
  const p = await read($, progress)
  const isStored = (q: Progress) => JSON.stringify(q) === JSON.stringify(stored)
  if (isStored(p)) return
  if (!isStored({ ...p, level: stored.level, isOff: stored.isOff })) await update($, progress, q => ({ ...q, movedAt: now }))
  await $.store.set(`progress:${key}`, await read($, progress))
}

type Saved = Partial<Progress> & { done?: string[]; rounds?: number }

// 0.2 stored the passed steps as `done` and the finished features as `rounds`.
function restore(saved: Saved | undefined, now: number): Progress {
  const level = saved?.level && ORDER.includes(saved.level) ? saved.level : FRESH.level
  if (saved?.steps) return { ...FRESH, ...saved, level }
  const done = saved?.done ?? []
  const features = saved?.rounds ?? 0
  // A round 0.2 had finished but not moved past is a finished feature.
  if (done.includes('retro')) return { ...FRESH, level, features: features + 1 }
  const steps = Object.fromEntries(done.map(key => [key, 'passed'] as const))
  const isUnderWay = Object.keys(steps).some(key => key !== 'setup')

  return { ...FRESH, level, steps, feature: isUnderWay ? { name: null, since: now } : null, features }
}

async function checkSetup($: EngineInterface) {
  const hasSetup = await $.fs.exists(`${await read($, project)}/${SETUP_FILE}`)
  await update($, isSetUp, () => hasSetup)
}

// The nearest folder at or above `cwd` that is set up, else `cwd`: a session opened in a
// subfolder works on its project, and a linked worktree with its own checkout is a project of its own.
async function projectRoot($: EngineInterface, cwd: string) {
  for (let dir = cwd; dir !== ''; dir = dir.slice(0, dir.lastIndexOf('/'))) {
    if (await $.fs.exists(`${dir}/${SETUP_FILE}`)) return dir
  }

  return cwd
}

// Another session of the project may have moved it on: read it afresh before acting on it.
// ponytail: $.store has no compare-and-set, so a write another session lands between this read and the save after it is lost.
async function reread($: EngineInterface) {
  await revive($)
  const key = await read($, project)
  if (key === null) return
  const saved = (await $.store.get(`progress:${key}`)) as Saved | undefined
  const now = await $.clock.now()
  await update($, progress, () => restore(saved, now))
}

async function load($: EngineInterface, root: string) {
  await update($, project, () => root)
  await checkSetup($)
  await reread($)
}

// Loads the project again once a /clear has dropped it.
async function revive($: EngineInterface) {
  if (home !== null && (await read($, project)) === null) await load($, home)
}

// Why the rail stays out of this project (never set up, or turned off), or undefined while it is on.
async function quietLine($: EngineInterface) {
  if (!(await read($, isSetUp))) return `這個專案還沒設定，軌道沒有作用：先輸入 ${STEPS.setup.command}`
  if ((await read($, progress)).isOff) return '軌道在這個專案關著：輸入 /matt-flow on 打開'

  return undefined
}
const isQuiet = async ($: EngineInterface) => (await quietLine($)) !== undefined

async function isLocalTracker($: EngineInterface) {
  const text = await $.fs.read(`${await read($, project)}/${SETUP_FILE}`).catch(() => '')

  return /^# Issue tracker: Local Markdown/im.test(text)
}

const list = ($: EngineInterface, path: string) => $.fs.list(path).catch((): FsEntry[] => [])

async function refreshStatus($: EngineInterface) {
  const p = await read($, progress)
  const going = underWay(p)
  if ((going ?? nextStep(p, await read($, isSetUp))) === undefined || (await isQuiet($))) return $.ui.status(undefined)
  $.ui.status(`✦ ${LEVELS[p.level].icon} ${going ? `▶ ${STEPS[going].title} · ` : ''}下一步 ${nextOf(p)} · /matt-flow`)
}

// `/matt-flow all`: every project with progress, the one left longest first, then the features ended lately,
// the done apart from the aborted.
async function overview($: EngineInterface) {
  const now = await $.clock.now()
  const projects: { root: string; p: Progress }[] = []
  for (const key of await $.store.keys()) {
    if (!key.startsWith('progress:')) continue
    const p = restore((await $.store.get(key)) as Saved | undefined, now)
    if (p.feature !== null || p.features > 0 || p.records.length > 0) projects.push({ root: key.slice('progress:'.length), p })
  }
  // A project with no time it moved goes last: it says nothing about being idle.
  const lastMoved = ({ p }: { p: Progress }) => movedOf(p) ?? Number.MAX_SAFE_INTEGER
  const rows = projects
    .filter(({ p }) => p.feature !== null || p.features > 0)
    .sort((a, b) => lastMoved(a) - lastMoved(b))
    .map(({ root, p }) => {
      const moved = movedOf(p)
      const isIdle = p.feature !== null && moved !== null && now - moved > LONG_IDLE

      return [
        `${isIdle ? '⚠' : ' '} ${where(root)}`,
        `${LEVELS[p.level].icon} ${LEVELS[p.level].name}`,
        featureLine(p),
        `下一步 ${nextOf(p)}`,
        ...idleFor(p, now),
        // With no feature under way, what the project has done instead.
        ...(p.feature === null && p.features > 0 ? [`已完成 ${p.features} 個功能`] : []),
      ].join(' · ')
    })
  const ended = (isAborted: boolean) =>
    projects
      .flatMap(({ root, p }) =>
        p.records
          .filter(record => now - record.end <= LATELY && (record.isAborted === true) === isAborted)
          .map(record => ({ root, record })),
      )
      .sort((a, b) => b.record.end - a.record.end)
      .map(({ root, record }) => recordLine(root, record))
  const aborted = ended(true)

  return [
    ...rows,
    `最近 7 天結束的功能：${ended(false).join('、') || '沒有'}`,
    ...(aborted.length > 0 ? [`最近 7 天中止的功能：${aborted.join('、')}`] : []),
  ].join('\n')
}

const NEXT_FEATURE = ` → 下一個從 ${STEPS.grill.command} 開始`

// Ends the feature, saying so: done once its retro ran, else aborted, which does not count.
async function endFeature($: EngineInterface, isDone: boolean) {
  const now = await $.clock.now()
  await update($, progress, p => finish(p, now, isDone))

  return isDone ? `🎉 功能結束，已完成 ${(await read($, progress)).features} 個功能` : '⏹ 功能中止：沒做到複盤，不算完成'
}

async function startFeature($: EngineInterface) {
  const now = await $.clock.now()
  await update($, progress, p => (p.feature ? p : { ...p, feature: { name: null, since: now } }))
}

// Setup passes on its file alone, and hands over to grilling.
async function passSetup($: EngineInterface) {
  await update($, progress, p => mark(p, ['setup'], 'passed'))
  suggestion = STEPS.grill.command
  await save($)
  $.ui.toast(`✔ ${STEPS.setup.title} 通過 → 下一步 ${suggestion}`)
}

// The steps whose skill `name` is: a plugin's skill arrives as `mattpocock-skills:to-spec`.
const stepsOf = (name: string) => {
  const skill = name.split(':').pop() ?? name

  return (Object.keys(STEPS) as StepKey[]).filter(key => STEPS[key].skills.includes(skill))
}

// Whether the local tracker holds the level's spec and tickets: only then do their files show them done.
const tracksFiles = async ($: EngineInterface, p: Progress) =>
  LEVELS[p.level].steps.includes('spec') && (await isLocalTracker($))

// The artifacts written since the feature started, and their folder. Until a spec names the feature's
// folder only a spec counts, in any folder; then both count, in that folder alone.
// ponytail: written means modified (fs has no creation time), so an old spec or ticket of the same folder edited now counts.
async function artifacts($: EngineInterface, p: Progress) {
  if (p.feature === null || !(await tracksFiles($, p))) return undefined
  const { name, since } = p.feature
  const root = `${await read($, project)}/${SCRATCH}`
  const isNew = (entries: FsEntry[], file: RegExp) =>
    entries.some(entry => entry.kind === 'file' && file.test(entry.name) && entry.mtimeMs >= since)
  const folders = name !== null ? [name] : (await list($, root)).filter(entry => entry.kind === 'dir').map(entry => entry.name)
  for (const folder of folders) {
    const keys: StepKey[] = []
    if (isNew(await list($, `${root}/${folder}`), /^spec\.md$/)) keys.push('spec')
    if (name !== null && isNew(await list($, `${root}/${folder}/issues`), /\.md$/)) keys.push('tickets')
    if (keys.length > 0) return { folder, keys }
  }

  return undefined
}
const isWritten = async ($: EngineInterface, p: Progress, key: StepKey) =>
  (await artifacts($, p))?.keys.includes(key) ?? false

// What leaving the step under way for `next` still waits for, said for the person; undefined once it may be left.
async function holdOf($: EngineInterface, p: Progress, going: StepKey, next: StepKey | undefined) {
  // Tickets are looked for in the spec's folder: with no spec there is none, so they wait for nothing.
  const name = p.feature?.name ?? null
  const isLooked = going === 'spec' || (going === 'tickets' && name !== null)
  if (ARTIFACTS.includes(going) && isLooked && (await tracksFiles($, p)) && !(await isWritten($, p, going))) {
    return going === 'spec' ? `還沒看到 ${SCRATCH}/<功能>/spec.md` : `還沒看到 ${SCRATCH}/${name}/issues/ 裡的任務卡`
  }
  // An intermediate build is done once code-review ran; the beginner's review is a step of its own, skipped on purpose or not.
  if (going === 'build' && p.level === 'intermediate' && next !== undefined && !p.isReviewed) return '這次動手做還沒跑過 code-review'

  return undefined
}

// The step a skip passes over: the one under way when it cannot be left (or ends the flow), else the next one.
async function skipTarget($: EngineInterface, p: Progress) {
  const going = underWay(p)
  const next = nextStep(p, true)
  if (going && (next === undefined || (await holdOf($, p, going, next)))) return going

  return next ?? going
}

type Move = { key: StepKey } | { deny: string } | undefined

// What a step's skill does to the flow, decided before it runs so a jump never starts. Nothing moves for the step
// under way again, an earlier one, one outside the level, or one after building typed before it.
async function judge($: EngineInterface, keys: StepKey[], byPerson: boolean): Promise<Move> {
  if (keys.length === 0) return undefined
  await reread($)
  if (await isQuiet($)) return undefined
  const p = await read($, progress)
  const order = LEVELS[p.level].steps
  // Building typed outside its level stands for the level's own.
  const key = keys.find(each => order.includes(each)) ?? (byPerson && keys.some(each => BUILD.includes(each)) ? order.find(each => BUILD.includes(each)) : undefined)
  if (key === undefined) return undefined
  const going = underWay(p)
  // The first step again with the retro under way: this feature is done, and the next starts.
  if (isInRetro(p) && key === 'grill') return byPerson ? { key } : undefined
  const next = nextStep(p, true)
  if (key === going || next === undefined || order.indexOf(key) < order.indexOf(next)) return undefined
  if (LATE.includes(key) && !isBuilding(p)) return undefined
  if (BUILD.includes(key) && !byPerson) return { deny: `matt-flow：「${STEPS[key].title}」要由人輸入 ${STEPS[key].command} 才開始。` }
  if (key !== next) return { deny: aheadLine(key, next) }
  // Only the person starts a feature, and settles a step: the model moves on only by the review after building.
  if (!byPerson) {
    if (p.feature === null) return undefined
    if (!(key === 'review' && going && BUILD.includes(going))) {
      return { deny: `matt-flow：「${STEPS[key].title}」要由人輸入 ${STEPS[key].command} 才開始，前一步什麼時候定案由人決定。` }
    }
  }
  const hold = going && (await holdOf($, p, going, key))
  if (hold && going) {
    return { deny: `matt-flow：「${STEPS[going].title}」還沒做完：${hold}。做完再輸入 ${STEPS[key].command}；${SKIP_WAY}` }
  }

  return { key }
}

// The one place a step passes: the next one starts, the person moving on is what settles it. A retro under way ends
// its feature done first; building typed outside the level is marked too, so its subagents may commit.
async function moveOnto($: EngineInterface, key: StepKey, typed: StepKey[]) {
  const before = await read($, progress)
  const ended = isInRetro(before) ? await endFeature($, true) : undefined
  const passed = ended === undefined ? underWay(before) : undefined
  await startFeature($)
  const order = LEVELS[(await read($, progress)).level].steps
  const outside = typed.filter(each => BUILD.includes(each) && !order.includes(each))
  await update($, progress, p => mark(passed ? mark(p, [passed], 'passed') : p, [key, ...outside], 'underWay'))
  const said = `▶ 開始「${STEPS[key].title}」：${STEPS[key].criterion}之後，${thenOf(await read($, progress))}`
  $.ui.toast([ended, passed && `✔ ${STEPS[passed].title} 通過`, said].filter(Boolean).join(' · '))
}

// A step's skill ran: the flow moves as judged, and the review a commit waits for is noted.
async function noteRan($: EngineInterface, keys: StepKey[], move: Move, byPerson: boolean) {
  if (keys.length === 0 || (await isQuiet($))) return
  if (move && 'key' in move) await moveOnto($, move.key, keys)
  // One review per build, and each /implement the person types is a build; the fixes after a review commit without another.
  if (byPerson && keys.some(key => BUILD.includes(key))) await update($, progress, p => ({ ...p, isReviewed: false }))
  if (keys.includes('review')) await update($, progress, p => (isBuilding(p) ? { ...p, isReviewed: true } : p))
  await save($)
  await refreshStatus($)
}

// A spec written since the feature started names the feature after its folder.
async function checkArtifacts($: EngineInterface) {
  const p = await read($, progress)
  if (p.feature === null || p.feature.name !== null || (await isQuiet($))) return
  const found = await artifacts($, p)
  if (!found?.keys.includes('spec')) return
  await update($, progress, q => (q.feature ? { ...q, feature: { ...q.feature, name: found.folder } } : q))
  await save($)
}

// Once the step under way is seen done its next command is offered, once: spec and tickets when their files are
// written, code-review when it ran. Grilling and the rest are done when the person says so.
async function offer($: EngineInterface) {
  const p = await read($, progress)
  const going = underWay(p)
  const at = `${p.feature?.since}:${going}`
  if (going === undefined || offered === at || (await isQuiet($))) return
  if (going === 'review' || (ARTIFACTS.includes(going) && (await isWritten($, p, going)))) {
    suggestion = nextOf(p)
    offered = at
  }
}

// The project's HEAD, or '' outside a repo: a commit names the feature only if it moved it.
async function headOf($: EngineInterface, root: string) {
  const { exitCode, stdout } = await $.process.run(['git', 'rev-parse', 'HEAD'], { cwd: root })

  return exitCode === 0 ? stdout.trim() : ''
}

// Whether a commit Claude runs now could name the feature: building, and no spec or commit named it yet.
async function mayName($: EngineInterface) {
  const p = await read($, progress)

  return p.feature !== null && p.feature.name === null && isBuilding(p) && !(await isQuiet($))
}

// The commit that moved the project's HEAD names the feature by its title. One that failed, or went to another
// repo (`git -C other`), moved nothing here and names nothing.
async function nameByCommit($: EngineInterface, root: string, before: string) {
  if ((await headOf($, root)) === before) return
  const { exitCode, stdout } = await $.process.run(['git', 'log', '-1', '--format=%s'], { cwd: root })
  const name = stdout.trim()
  if (exitCode !== 0 || name === '') return
  await update($, progress, q => (q.feature && q.feature.name === null ? { ...q, feature: { ...q.feature, name } } : q))
  await save($)
}

// Why editing `path` is denied, or undefined while it may go ahead. The unlock command goes in the prompt box only
// while no step is under way: one under way is settled when the person says so.
async function codeGate($: EngineInterface, path: string) {
  await revive($)
  const root = await read($, project)
  // Quiet first: as long as the state reads at all, /matt-flow off holds.
  if (root === null || (await isQuiet($)) || !isCode(root, path)) return undefined
  const p = await read($, progress)
  if (isBuilding(p)) return undefined
  const key = unlockStep(p)
  const isOffered = underWay(p) === undefined
  if (isOffered) suggestion = STEPS[key].command

  return `matt-flow：還沒到動手做，程式碼鎖著。下一步是「${STEPS[key].title}」，解鎖要由人輸入 ${STEPS[key].command}${isOffered ? '（已預填在輸入框）' : ''}。停下來交棒：把這個指令告訴人，然後結束這次回覆。不要改用 Bash 或其他方式寫這個檔案。`
}

// What the rail holds now, and how each unlocks.
const locksOf = (p: Progress) => [
  ...(isBuilding(p)
    ? []
    : [{ action: '改程式碼（Edit、Write、NotebookEdit）', unlock: `由人輸入 ${STEPS[unlockStep(p)].command} 解鎖` }]),
  ...(isCommitLocked(p) ? [{ action: 'git commit', unlock: `先跑 code-review（Skill 工具，或請人輸入 ${STEPS.review.command}）` }] : []),
]

// Why running `command` is denied, or undefined while it may go ahead. A subagent
// of /implement-spec commits its ticket: the person started that run.
async function commitGate($: EngineInterface, command: string, isAgent: boolean) {
  if (!GIT_COMMIT.test(command)) return undefined
  await revive($)
  const root = await read($, project)
  if (root === null || (await isQuiet($)) || isElsewhere(root, command)) return undefined
  const p = await read($, progress)
  if ((isAgent && p.steps.parallel) || !isCommitLocked(p)) return undefined
  suggestion = STEPS.review.command

  return `matt-flow：這次動手做還沒跑過 code-review，先不能 commit。先用 Skill 工具跑 code-review（或請人輸入 ${STEPS.review.command}），跑過之後的 commit 都會放行。不要繞過這個阻擋。`
}

// Claude's own map of the rail, sent beside the person's prompt: where the flow
// stands, what is locked and how it unlocks, what still goes, and how to hand over.
async function railPrompt($: EngineInterface) {
  if (await isQuiet($)) return undefined
  const p = await read($, progress)
  const going = underWay(p)
  const step = STEPS[nextStep(p, true) ?? 'grill']
  const isByTicket = isTicketByTicket(p)
  const locks = locksOf(p)

  return [
    '# matt-flow 軌道',
    '',
    '這個專案照 Matt Pocock 的流程走，由 matt-flow 把關，人輸入每一步的指令。',
    `- ${featureLine(p)}`,
    `- 等級：${LEVELS[p.level].name}`,
    ...(going ? [`- 進行中：${STEPS[going].title}（${STEPS[going].criterion}才算做完，由人決定什麼時候往下）`] : []),
    `- 下一步：${isByTicket ? NEXT_TICKET : isInRetro(p) ? `結束功能（${END}）` : `${step.title}（${step.command}）`}`,
    `- 現在會被擋的動作：${locks.length === 0 ? '沒有' : ''}`,
    ...locks.map(({ action, unlock }) => `  - ${action}：${unlock}`),
    ...(isBuilding(p)
      ? []
      : ['- 仍可以：讀檔、跑測試、改 markdown、docs/、.scratch/；跟目前功能無關的修改，請人決定要不要 /matt-flow off']),
    '',
    '規矩：',
    `- 交棒：人這次啟動的 skill 整個做完（不是它一開始），或改程式碼被擋下時，就停下來，把下一步的指令（現在是 ${isByTicket ? NEXT_TICKET : nextOf(p)}）告訴人，然後結束這次回覆；由人輸入，不要自己往下做。`,
    '- 流程的 skill 只能照順序跑，跳步的會被擋下；要跳過一步，由人輸入 /matt-flow skip。',
    `- 除了下一步的指令和 /matt-flow，不要主動建議流程指令。沒有進行中的功能、或人問該怎麼辦時，可以點名 Matt 的入口：${WAYS_IN}，由人輸入。人輸入 /ask-matt 時，照 ask-matt 回答。`,
    '- 絕不繞過任何阻擋，包括改用 Bash 寫檔或 commit。',
  ].join('\n')
}

// Ends the feature for a subcommand and says what comes next.
async function closeFeature($: EngineInterface, isDone: boolean) {
  const line = `${await endFeature($, isDone)}${NEXT_FEATURE}`
  await save($)
  await refreshStatus($)

  return line
}

// `/matt-flow skip`: the step in the way counts as done without its artifact. A retro under way ran, so skipping it
// ends the feature done; one never started ends it aborted.
async function skipStep($: EngineInterface) {
  await reread($)
  const quiet = await quietLine($)
  if (quiet) return quiet
  const p = await read($, progress)
  const key = (await skipTarget($, p)) ?? 'grill'
  if (key === 'retro') {
    if (!isInRetro(p)) await update($, progress, q => mark(q, ['retro'], 'skipped'))

    return closeFeature($, isInRetro(p))
  }
  await startFeature($)
  await update($, progress, q => mark(q, [key], 'skipped'))
  const line = `↷ 跳過「${STEPS[key].title}」→ 下一步 ${nextOf(await read($, progress))}`
  await save($)
  await refreshStatus($)

  return line
}

// `/matt-flow end`: the person closes the feature, done once its retro is under way, else aborted.
async function stopFeature($: EngineInterface) {
  await reread($)
  const quiet = await quietLine($)
  if (quiet) return quiet
  const p = await read($, progress)
  if (p.feature === null) return `沒有進行中的功能 → 下一步 ${nextOf(p)}`

  return closeFeature($, isInRetro(p))
}

// `/matt-flow off` and `on`, for this project.
async function setOff($: EngineInterface, isOff: boolean) {
  await reread($)
  await update($, progress, p => ({ ...p, isOff }))
  await save($)
  await refreshStatus($)
  if (isOff) return '軌道在這個專案關掉了：不擋指令、程式碼和 commit，也不交棒。輸入 /matt-flow on 再打開'

  return (await quietLine($)) ?? `軌道打開了 → 下一步 ${nextOf(await read($, progress))}`
}

// Mid-build, the new level's steps up to its own building count as skipped, so the flow goes on from there.
async function setLevel($: EngineInterface, lv: Level) {
  await reread($)
  await update($, progress, p => {
    if (!isBuilding(p)) return { ...p, level: lv }
    const order = LEVELS[lv].steps
    const upTo = order.slice(0, order.findIndex(key => BUILD.includes(key)) + 1)

    return mark({ ...p, level: lv }, upTo.filter(key => !stateOf(p, key, true)), 'skipped')
  })
  await save($)
  await refreshStatus($)
}

// `/ask-matt` with the facts it routes on: the step, the steps skipped, what is locked, how long the project has been idle.
async function askMatt($: EngineInterface, key: StepKey) {
  const p = await read($, progress)
  const skipped = skippedOf(p)
  // A project the rail is quiet in locks nothing.
  const locks = (await isQuiet($)) ? [] : locksOf(p).map(lock => lock.action)
  const facts = [
    skipped.length > 0 ? `跳過了${titled(skipped)}` : '沒有跳過步驟',
    locks.length > 0 ? `現在會被擋：${locks.join('、')}` : '現在沒有會被擋的動作',
    ...idleFor(p, await $.clock.now()),
  ]
  // The command leads so it runs; a draft the person was writing follows it.
  const draft = (await $.prompt.read()).text
  await $.prompt.fill({
    text: `/ask-matt 我在 Matt 導航的「${LEVELS[p.level].name}」流程，卡在「${STEPS[key].title}」(${STEPS[key].command})。${facts.map(fact => `${fact}。`).join('')}我遇到的狀況是：${draft}`,
  })
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const root = await projectRoot($, e.cwd)
    home = root
    await load($, root)
    await $.command.register({
      name: 'matt-flow',
      description: '打開或關閉 Matt 導航；all 看所有專案，skip 跳過擋在前面的那一步，end 結束功能，off／on 關閉或打開這個專案的軌道',
      argumentHint: 'all | skip | end | off | on',
    })
    await refreshStatus($)

    return next(e)
  })

  on('command.run', { command: 'matt-flow' }, async ($, e) => {
    switch (e.args.trim()) {
      case '':
        break
      case 'all':
        return { text: await overview($) }
      case 'skip':
        return { text: await skipStep($) }
      case 'end':
        return { text: await stopFeature($) }
      case 'off':
        return { text: await setOff($, true) }
      case 'on':
        return { text: await setOff($, false) }
      default:
        return { text: '用法：/matt-flow 打開或關閉面板；/matt-flow all 看所有專案；/matt-flow skip、end、off、on' }
    }
    if ((await $.ui.panes()).some(pane => pane.id === PANE)) {
      await $.ui.close({ id: PANE })

      return { text: 'Matt 導航已關閉，再輸入 /matt-flow 就會打開。' }
    }
    await $.ui.open({ id: PANE, title: TITLE })

    return { text: 'Matt 導航已打開。' }
  })

  // Not `skill.prompt`: the managed security hook skips past user plugins there.
  // A skill the person typed as `/name`: a jump past the next step is dropped, saying why; the rest goes on.
  on('prompt.submit', async ($, e, next) => {
    await reread($)
    if (e.command) {
      const keys = stepsOf(e.command.name)
      const move = await judge($, keys, true)
      if (move && 'deny' in move) return { drop: move.deny }
      await noteRan($, keys, move, true)
    }
    const messages = await $.session.messages()
    const first = messages[0]?.text
    // Compacted, rewound or cleared: the rail went with what was dropped.
    if ((seen.head !== undefined && first !== seen.head) || messages.length < seen.count) sent = undefined
    // A conversation still empty when the rail went out: its first message is this one.
    seen = { head: seen.head ?? first, count: messages.length }
    const rail = await railPrompt($)
    if (rail === sent) return next(e)
    // A rail taken back says so: the old one stays in the conversation, still telling Claude to stop.
    const line = rail ?? 'matt-flow 軌道在這個專案停用了，先前的規矩不再適用。'
    sent = rail
    seen = { ...seen, head: first }

    return next({ ...e, context: [...(e.context ?? []), line] })
  })

  on('session.end', async ($, e, next) => {
    sent = undefined
    seen = { count: 0 }

    return next(e)
  })

  // A skill the model runs through the Skill tool: a jump is denied, the rest noted once it ran.
  // A subagent's moves nothing, only the main thread does.
  on('tool.call', { tool: 'Skill' }, async ($, e, next) => {
    if (e.agentId !== undefined) return next(e)
    const keys = stepsOf(e.skill)
    const move = await judge($, keys, false)
    if (move && 'deny' in move) return { deny: `${move.deny} ${HAND_OVER}` }
    const result = await next(e)
    if (result.deny === undefined && !result.isError) await noteRan($, keys, move, false)

    return result
  })

  on('turn.complete', async ($, e, next) => {
    // A subagent's turn ending is no hand-over: the person is waiting on the main thread.
    if (e.agentId !== undefined) return next(e)
    seen = { ...seen, count: (await $.session.messages()).length }
    const { context } = await $.session.usage()
    await update($, tokens, () => context.tokens ?? null)
    await reread($)
    const wasSetUp = await read($, isSetUp)
    await checkSetup($)
    if (!wasSetUp && !(await isQuiet($))) await passSetup($)
    await checkArtifacts($)
    await offer($)
    await refreshStatus($)
    const result = await next(e)
    if (suggestion !== undefined) {
      void $.prompt.suggest({ text: suggestion })
      suggestion = undefined
    }

    return result
  })

  on('tool.call', { tool: 'Edit' }, async ($, e, next) => {
    const locked = await codeGate($, e.file_path)

    return locked ? { deny: locked } : next(e)
  }).catch(($, e, next) => (next.called ? next(e) : mayBeCode(e.file_path) ? { deny: BROKEN } : next(e)))

  on('tool.call', { tool: 'Write' }, async ($, e, next) => {
    const locked = await codeGate($, e.file_path)

    return locked ? { deny: locked } : next(e)
  }).catch(($, e, next) => (next.called ? next(e) : mayBeCode(e.file_path) ? { deny: BROKEN } : next(e)))

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const locked = await commitGate($, e.command, e.agentId !== undefined)
    if (locked) return { deny: locked }
    // Naming never fails the commit itself: a git that cannot be asked names nothing.
    const root = await read($, project)
    const isNaming = e.agentId === undefined && GIT_COMMIT.test(e.command) && root !== null && (await mayName($))
    const before = isNaming && root !== null ? await headOf($, root).catch(() => undefined) : undefined
    const result = await next(e)
    if (before !== undefined && root !== null && result.deny === undefined && !result.isError) {
      await nameByCommit($, root, before).catch(() => undefined)
    }

    return result
  }).catch(($, e, next) => (next.called ? next(e) : GIT_COMMIT.test(e.command) ? { deny: BROKEN } : next(e)))

  on('tool.call', { tool: 'NotebookEdit' }, async ($, e, next) => {
    const locked = await codeGate($, e.notebook_path)

    return locked ? { deny: locked } : next(e)
  }).catch(($, e, next) => (next.called ? next(e) : mayBeCode(e.notebook_path) ? { deny: BROKEN } : next(e)))

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    const p = await read($, progress)
    const lv = p.level
    const setUp = await read($, isSetUp)
    const fill = await read($, tokens)
    const quiet = await quietLine($)
    const track = LEVELS[lv]
    const going = underWay(p)
    // The card is where the flow stands: the step under way, else the next one.
    const stand = going ?? nextStep(p, setUp)
    // Skip names the step it passes over, which need not be the card's.
    const skipping = quiet === undefined ? await skipTarget($, p) : undefined
    const count = track.steps.filter(key => ['passed', 'skipped'].includes(stateOf(p, key, setUp) ?? '')).length
    const width = Math.max(8, Math.min(24, (e.props.bodyColumns ?? 40) - 10))
    const filled = bar(count / track.steps.length, width)
    const zone = fill === null ? 0 : fill / SMART_ZONE
    const zoneColor = zone >= 1 ? 'error' : zone >= 0.8 ? 'warning' : 'success'

    return (
      <Box flexDirection="column" gap={1}>
        <Box justifyContent="space-between">
          <Text bold color="claude">
            ✦ Matt 導航
          </Text>
          <Text bold color="inverseText" backgroundColor="claude">
            {` 已完成 ${p.features} 個功能 `}
          </Text>
        </Box>

        <Box flexDirection="column">
          <Box gap={1} flexWrap="wrap">
            {ORDER.map(each => (
              <Button
                key={`level-${each}`}
                variant={each === lv ? 'primary' : undefined}
                dimColor={each !== lv}
                onPress={() => setLevel($, each)}
              >
                {`${LEVELS[each].icon} ${LEVELS[each].name}`}
              </Button>
            ))}
          </Box>
          <Text italic color="subtle">
            {track.goal}
          </Text>
        </Box>

        <Box flexDirection="column">
          <Text bold>{featureLine(p)}</Text>
          {quiet !== undefined && (
            <Text color="warning" wrap="wrap">
              {quiet}
            </Text>
          )}
        </Box>

        <Box gap={1}>
          <Text color="success">{'█'.repeat(filled)}</Text>
          <Text dimColor>{'░'.repeat(width - filled)}</Text>
          <Text bold>{`${count} / ${track.steps.length}`}</Text>
        </Box>

        <Box flexDirection="column">
          {track.steps.map((key, i) => {
            const step = STEPS[key]
            const state = stateOf(p, key, setUp)

            return key === stand ? (
              <Box
                key={key}
                flexDirection="column"
                borderStyle="round"
                borderColor="claude"
                paddingX={1}
              >
                <Text bold color="claude">
                  {key === going ? `▶ ${i + 1}. ${step.title}（進行中）` : `→ ${i + 1}. ${step.title}`}
                </Text>
                <Text bold color="suggestion">
                  {key === going ? `   ${step.criterion}之後：${nextOf(p)}` : `   ${step.command}`}
                </Text>
                <Text wrap="wrap">{step.what}</Text>
                <Text italic color="subtle" wrap="wrap">{`💡 ${step.tip}`}</Text>
                <Box gap={1} flexWrap="wrap" marginTop={1}>
                  <Button key="skip" hotkey="1" onPress={async () => $.ui.toast(await skipStep($))}>
                    {skipping ? `↷ 跳過「${STEPS[skipping].title}」` : '↷ 跳過'}
                  </Button>
                  <Button key="stuck" hotkey="2" dimColor onPress={() => askMatt($, key)}>
                    ? 我卡住了
                  </Button>
                </Box>
              </Box>
            ) : (
              <Box key={key} justifyContent="space-between" paddingX={1}>
                {state === 'passed' ? (
                  <Text color="success">{`✔ ${i + 1}. ${step.title}`}</Text>
                ) : state === 'skipped' ? (
                  <Text color="warning" dimColor>{`↷ ${i + 1}. ${step.title}（跳過）`}</Text>
                ) : (
                  <Text dimColor>{`○ ${i + 1}. ${step.title}`}</Text>
                )}
                <Text dimColor>{step.command}</Text>
              </Box>
            )
          })}
        </Box>

        {fill !== null && (
          <Box flexDirection="column">
            <Box gap={1}>
              <Text>🧠</Text>
              <Text color={zoneColor}>{'▮'.repeat(bar(zone, 10))}</Text>
              <Text dimColor>{'▯'.repeat(10 - bar(zone, 10))}</Text>
              <Text color={zoneColor}>{`${Math.round(fill / 1000)}k / ${SMART_ZONE / 1000}k`}</Text>
            </Box>
            {zone >= 0.8 && (
              <Text color="warning" wrap="wrap">
                對話快塞滿了：交棒時先 /compact
              </Text>
            )}
          </Box>
        )}

        {e.surface === 'terminal' && (
          <Text dimColor wrap="wrap">
            ctrl+x tab 進入面板：1 跳過，2 我卡住了
          </Text>
        )}
      </Box>
    )
  })
}
