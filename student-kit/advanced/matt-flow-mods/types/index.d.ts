export type Level = 'beginner' | 'intermediate' | 'expert'

// A step with no state has not started; a started one is under way until the next one starts.
export type StepState = 'underWay' | 'passed' | 'skipped'

// A feature record: a feature as it ended, its skipped steps by their keys. An aborted one ended before its retro.
export type FeatureRecord = { name: string | null; since: number; end: number; skipped: string[]; isAborted?: true }

// One project's progress, kept across sessions under the project's root.
export type Progress = {
  level: Level
  // By step key. Building has started once the build step has a state.
  steps: Record<string, StepState>
  // The feature under way: `name` is its spec's folder once there is one, else the title of
  // its first commit while building; `since` when it started, so only artifacts written after it count.
  feature: { name: string | null; since: number } | null
  // Whether code-review has run since building started.
  isReviewed: boolean
  // Whether the person turned the rail off in this project.
  isOff: boolean
  // Features done (their retro ran) before this one.
  features: number
  // Their records since 0.5, the aborted too, oldest first.
  records: FeatureRecord[]
  // When the flow last moved on, null until it does after 0.5: how long the project has been idle.
  movedAt: number | null
}

declare module 'claude-code' {
  interface PluginState {
    'matt-flow': {
      // The project's root, the nearest set-up folder at or above the session's
      // working directory (else that directory): the key progress is stored under.
      project: string | null
      progress: Progress
      // Whether /setup-matt-pocock-skills has run in this project.
      isSetUp: boolean
      // Input tokens of the last response, null until one arrives.
      tokens: number | null
    }
  }
}
