---
name: cli-extension-sync
description: 兩個 Claude Code（IDE Extension ↔ CLI）之間的協作協議。Use when the user runs /sync, when handing off work between IDE-side coding and terminal-side review, or when updating .collab-sync.md.
---

# IDE Extension ↔ CLI 協作協議

這份 skill 提供「**IDE 寫 code、終端 review/commit**」這個雙 Claude 協作模式的標準協議。兩邊雖然都是 Claude Code，但角色刻意分開：

- **IDE Extension**（VS Code / JetBrains / Antigravity 等內裝的 Claude Code 擴充）：負責**寫 code**、跑測試、做局部修補。它「身在 codebase 內」，視野聚焦於檔案。
- **Claude Code CLI**（終端機跑 `claude` 指令）：負責 **review、commit、`/sync`**。它「身在 git 與 shell 旁邊」，視野是整個 repo 的 diff、history、工作流。

兩邊透過專案根目錄的 `.collab-sync.md` 同步狀態。

## 核心機制：同步檔案

所有的進度、狀態、審查請求都記錄在 `.collab-sync.md`。

如果該檔案不存在，**必須**先用 `references/sync_template.md` 建出空骨架。

## 工作流程：當 IDE Extension 完成一個 milestone 時

1. **更新 sync 檔**：Extension 把剛完成的工作摘要寫進 `.collab-sync.md` 的 `已完成任務` 區，並把下一步寫進 `Extension 的後續任務` 或 `CLI 的後續任務`。
2. **通知使用者**：「我完成了 X，請去終端跑 `/sync` 讓 CLI 端審查 + commit」。
3. （可選）標記 `待審查` 區。

## 工作流程：當 Claude Code CLI 收到 `/sync` 指令時

1. **讀同步檔**：`Read .collab-sync.md`，看 Extension 剛完成什麼、有什麼待審查項。如果使用者只是口頭說「Extension 完成了 X」，請自行先把這個狀態寫進 sync 檔。
2. **檢查改動**：跑 `git status` + `git diff`，盤點未 commit 的檔案。
3. **品質驗證**：
   - 對照 `CLAUDE.md` 的剛性規則（語言、技術棧、工作流程、禁忌條款）逐條檢查
   - Clean Code、模組化、Type Hinting（Python）
   - 後端依賴是不是用 `uv` 管的（禁 `pip install`、禁 `requirements.txt`）
   - Embedding 模型有沒有被偷偷換掉（必須是 `models/gemini-embedding-001`）
4. **反饋或 Commit**：
   - 有問題 → 在 sync 檔的 `反饋` 區記下，告訴使用者「轉交 Extension 修」，**不**做 commit
   - 沒問題 → 用 Conventional Commits 格式 commit（含 `Co-Authored-By` 行；commit message 為繁體中文）
5. **更新狀態**：把任務從 `待審查` 移到 `已完成任務`，並把下一步寫進 `Extension 的後續任務`。

## 工作流程：當 Claude Code CLI 自己完成一項任務時

1. **Commit**：自己驗證後直接 commit。
2. **更新同步檔**：把任務寫進 `已完成任務`。
3. **交接**：在 `Extension 的後續任務` 寫下一步要做什麼，讓使用者帶回 IDE 給 Extension 接手。

## 為什麼要這樣分？

「**寫 code 的不要自己 review 自己**」是這份協議的核心精神。即使兩邊都是 Claude Code，視角分離（IDE 內 vs 終端旁）就能讓 reviewer 看到 implementer 看不到的問題（commit boundary、規範遵守、跨檔影響）。這是「同人不同位」的協作策略。

如果你只跑單邊 Claude Code、不想要這個 ceremony，直接忽略這份 skill，省略 `.collab-sync.md` 也 OK。但對教學情境而言，這個拆分能讓學員清楚看到「實作」跟「審查」是兩個獨立思考活動。
