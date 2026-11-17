# Stage 2 — LLM Wiki（這裡等你動手）

> 這個資料夾是 **Stage 2 的家**。完成 Stage 1（普通 RAG）後再進來。

## 你會在這裡做什麼？

跟 Claude Code Extension + CLI 一起，把專案根目錄那份 [`llm-wiki.md`](../llm-wiki.md)（Pattern 描述文件）變成**這個專案實際可用的 LLM Wiki**。

跟 Stage 1 不一樣的地方：
- Stage 1 是「**寫程式**」——蓋 Python 後端 + Next.js 前端。
- Stage 2 是「**寫提示**」——共創一份 `CLAUDE.md` schema，讓 Claude Code CLI 變成這份知識庫的維護者。沒有資料庫、沒有向量、沒有 Python，只有 Markdown + YAML。

## 起手式 Prompt

打開 Claude Code Extension，輸入：

```
請讀取專案根目錄的 llm-wiki.md，那是一份高層的 pattern 描述。
請跟我一起用這個 pattern 來實例化 wiki-project/ 這個資料夾：

1. 先讀完 llm-wiki.md，跟我討論 3 個關鍵設計決策
   （例如：我們的 raw/ 要放什麼類型的文件？wiki/ 的目錄要不要分 entities/concepts/sources/synthesis？）
2. 確認方向後，幫我在 wiki-project/CLAUDE.md 寫一份「給 Claude Code CLI 看的 schema」
3. 完成後更新 .collab-sync.md，交給 Claude Code CLI Review。
```

## 預期成果

完成 Stage 2 後，這個資料夾會長成：

```
wiki-project/
├── CLAUDE.md          ← 你跟 Claude Code Extension 共創的 schema（Stage 2 的核心成果）
├── raw/               ← 你自己丟原始文件進來
│   ├── article-1.md
│   ├── paper-2.pdf
│   └── ...
└── wiki/              ← Claude Code CLI 維護的知識庫
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── concepts/
    ├── entities/
    ├── sources/
    └── synthesis/
```

每次新增 `raw/` 文件後，告訴 Claude Code CLI「**幫我 ingest**」，它就會自動更新 `wiki/` 裡的相關頁面。

## 教學重點

讀完 `llm-wiki.md` 第 7–14 段時要特別停下來體會：
> _「LLM 不是在 query 時才重新發現知識，而是把知識編譯一次後持續維護。Wiki 是一個會持續累積的工件。」_

這跟 Stage 1 的 RAG（每次 query 都要從頭撈 chunks）有根本性的差異。

完成這個 stage 後再進 Stage 3，看 LangChain 怎麼把這兩種哲學自動化。
