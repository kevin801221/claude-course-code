---
name: to-spec
description: Turn the current conversation into a formal spec (PRD) with problem statement, vertical slice seams, and user stories.
disable-model-invocation: true
---

# To Spec (Matt Pocock Skills Suite)

將當前對話 context 轉化為結構化的 PRD 規格文件（寫入 `SPEC.md` 或 issue tracker）：

## 必須包含章節

1. **Problem Statement**：從終端使用者視角出發的問題描述。
2. **Solution**：解決方案與預期價值。
3. **User Stories**：完整的 As an <actor>, I want <feature>, so that <benefit> 清單。
4. **Seams & Architectural Decisions**：測試接縫與架構決策（使用 `GLOSSARY.md` 中的專用名詞）。
