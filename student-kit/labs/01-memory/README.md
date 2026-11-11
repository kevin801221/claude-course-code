# Lab 01：讓下一輪拿到正確資訊

講義 Part 08～09。先讀 [CLAUDE.md](../../CLAUDE.md)、[context pack](../../docs/context-pack.md) 與 [任務卡](../../docs/task-card.md)。

## 操作

1. 找出根 CLAUDE.md 裡的執行命令、資料格式與目前限制。
2. 讀 `.claude/rules/javascript.md`，區分專案常駐慣例與 paths 對應規則。
3. 把「幫我改善任務清單」改寫成 task card，至少有輸入、輸出、成功與停止條件。
4. 在新對話貼上 context pack，請 Claude 先指出需求缺口，不修改程式。
5. 最後用 [交接卡](../../docs/handoff-template.md) 寫下已確認與待處理事項。

## 驗收

另一位同學只讀你的任務卡與交接卡，就能知道要改哪個行為、跑什麼驗收、什麼不能假設。不要把一次性的需求塞進所有人的全域 CLAUDE.md。

課後可比較 [PRP 範本](../../resources/templates/context/README.md)：用在較大的需求，保留來源與不確定性。
