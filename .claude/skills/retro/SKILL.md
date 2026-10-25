---
name: retro
description: Review session friction and token waste to fix the environment, rules, and configuration instead of patching prompts.
disable-model-invocation: true
---

# Session Retro (Matt Pocock Skills Suite)

落實「**修環境，不修程式（Fix the environment, not the code）**」哲學：

## 執行流程

1. **工作階段回顧**：
   - 識別本次 session 中模型反覆試錯、繞遠路、或做出錯誤假設的關鍵點。
   - 識別因讀取巨型二進位檔或快取所造成的 Token 浪費。

2. **產出環境處方簽**：
   - 更新 `.gitignore`：排除不必要的上下文噪音。
   - 強化 `.claude/rules/` 或 `CLAUDE.md`：將不可妥協的工程規範寫入，而非留在口頭。
   - 擴充 `GLOSSARY.md`：澄清任何產生歧義的領域專有名詞。
   - 新增 Hook：透過腳本硬性攔截特定違規操作。
