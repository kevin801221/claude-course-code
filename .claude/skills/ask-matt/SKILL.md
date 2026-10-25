---
name: ask-matt
description: Ask which skill or flow fits your engineering situation. A router over Matt Pocock's engineering skills suite.
disable-model-invocation: true
---

# Ask Matt

You don't remember every skill, so ask.

A **flow** is a path through Matt Pocock's engineering skills. Most paths run along one **main flow**, and two **on-ramps** merge onto it.

## The main flow: idea → ship

1. **`/grill-with-docs`** — Sharpen the idea by interview. Start here when you have a codebase: it retains what it learns in `GLOSSARY.md` (formerly `CONTEXT.md`) and ADRs.
2. **Branch — can you settle every question in conversation?**
   - If a question needs a runnable answer, detour through **`/prototype`** bridged by **`/handoff`**.
3. **Branch — is this a multi-session build?**
   - **Yes** → **`/to-spec`** (turn the conversation into a PRD/spec), then **`/to-tickets`** to split it into vertical-slice tickets with explicit **blocking edges (Ticket Graph)**.
   - Then kick off **`/implement-spec`** (or **`/implement`**), dispatching unblocked tasks in parallel across sub-agents.
4. **Review & Ship**:
   - Run **`/code-review`** (two-axis: Standards + Spec).
   - Generate an evidence-backed PR with **`/pr`** (featuring Mermaid diagrams, test proof, and One-Way vs Two-Way Door classification).
5. **Session Closeout**:
   - Run **`/retro`** to review token waste and friction points, fixing the environment rather than adding brittle prompts.
