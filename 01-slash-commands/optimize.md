---
description: 分析程式碼的效能問題並提出最佳化建議
---

# 程式碼最佳化

依優先順序審查所提供的程式碼，找出以下問題：

1. **效能瓶頸** — 找出 O(n²) 運算、低效率的迴圈
2. **記憶體洩漏** — 找出未釋放的資源、循環參照
3. **演算法改善** — 建議更好的演算法或資料結構
4. **快取機會** — 找出重複的運算
5. **並行問題** — 找出競態條件或執行緒相關問題

回應請依以下格式呈現：
- 問題嚴重程度（Critical／High／Medium／Low）
- 程式碼中的位置
- 說明
- 建議修正方式與程式碼範例

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/commands
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
