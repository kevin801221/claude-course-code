# 4-Agent ML pipeline：把交接做成可檢查的產物

對應講義 Part 18。`source-agents/` 原樣保留完成版的四個代理；它們只供檢視，未放進 `.claude/agents/`，不會自動執行下載或訓練。

## 先做 20 分鐘空跑

1. 建立自己的新練習目錄，先閱讀下表，不要安裝 ML 套件。
2. 用 `/agents` 建立同名四個代理，工具先只給讀取與寫入；Bash 等實際執行時再加入。
3. 請主對話按順序委派四個代理，各自只寫「準備接收什麼、檢查什麼、交付什麼」的 Markdown，不抓資料、不訓練。
4. 故意拿掉 `data.yaml` 欄位，檢查 training-runner 是否回報缺漏，不能跳過。
5. 用另一個 session 只讀交接文件，確認能知道下一步與停止條件。

| 階段 | 輸入 | 必須交付 |
|---|---|---|
| data-hunter | 經確認的資料集版本 | 圖片/標註清單、原始 `data.yaml`、來源與授權 |
| bbox-labeler | 原始檔案與類別表 | 合法標註、split 統計、訓練用 `data.yaml` |
| training-runner | 驗證通過的 dataset | 訓練參數/估時、實際紀錄、`best.pt` |
| inference-runner | `best.pt` 與 test split | 視覺化、實際 mAP、摘要 |

可貼給 Claude：

```text
請把這份四階段 wafer pipeline 做成空跑練習。
只寫 01-intake.md、02-validation.md、03-training-plan.md、04-evaluation-plan.md，
不安裝、不下載、不呼叫外部 API、不訓練。
每個階段列出輸入、檢查、輸出與缺少輸入時的處理，並由主對話依依賴順序委派。
```

## 真訓練前要先知道

- 這是主對話依序委派 sub-agents；相依階段不能全部同時執行。
- 來源 agent 中的 Roboflow workspace、版本、類別數與硬體參數是原案例預設，不保證外部服務仍有同版資料；不要自動改成最新版。
- `bbox-labeler` 的六類範例要以下載資料的類別表為準；原準備腳本另有單一 Donut 類別設定，兩者不能混用。
- 原 training-runner 有「估時後等 GO」的流程，保留為長時間運算的教學例子；估時常數是示意，不能保證每台 Mac 一樣快。
- 原範例的輸出路徑是完整專案的 `Projects/2026-001-mvp/`，只複製 agent 不會自動得到所需資料或程式。
- mAP 與十張圖片必須來自實際執行；空跑報告不能填成實測成績。

## 完整來源

- [學生空白模板](https://github.com/kevin801221/claude-course-code/tree/475fe057ed234f836ff3eb06f4c5eecad9e36332/agent_group_projects/computer-vision-wafer-template)
- [完成版與腳本](https://github.com/kevin801221/claude-course-code/tree/475fe057ed234f836ff3eb06f4c5eecad9e36332/agent_group_projects/computer-vision-wafer-detection)
- [只教建立 agents 的 demo](https://github.com/kevin801221/claude-course-code/tree/475fe057ed234f836ff3eb06f4c5eecad9e36332/agent_group_projects/computer-vision-wafer-agents-detection-demo)

驗收：空跑版本能解釋四段依賴；真訓練版本需另交資料版本、split、訓練日誌、模型與實際評估。此精華包未執行 ML 訓練。
