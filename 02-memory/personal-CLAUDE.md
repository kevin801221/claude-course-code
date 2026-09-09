# 我的開發偏好

## 關於我
- **經驗年資**：8 年全端開發經驗
- **偏好語言**：TypeScript、Python
- **溝通風格**：直接、附帶範例
- **學習風格**：搭配程式碼的視覺化圖表

## 程式碼偏好

### 錯誤處理
我偏好用 try-catch 區塊做明確的錯誤處理，並附上有意義的錯誤訊息。
避免使用籠統的錯誤。務必記錄錯誤以利除錯。

### 註解
註解要說明「為什麼」，而不是「做了什麼」。程式碼本身應該不言自明。
註解應該解釋商業邏輯或不明顯的決策。

### 測試
我偏好 TDD（測試驅動開發）。
先寫測試，再寫實作。
專注在行為，而不是實作細節。

### 架構
我偏好模組化、鬆散耦合的設計。
用依賴注入來提升可測試性。
關注點分離（Controller、Service、Repository）。

## 除錯偏好
- 用 `[DEBUG]` 前綴搭配 console.log
- 附上上下文：函式名稱、相關變數
- 有堆疊追蹤時就使用
- 日誌一律附上時間戳記

## 溝通方式
- 用圖表解釋複雜概念
- 先給出具體範例，再解釋理論
- 附上修改前 / 修改後的程式碼片段
- 最後總結重點

## 專案組織
我的專案組織方式如下：
```
project/
  ├── src/
  │   ├── api/
  │   ├── services/
  │   ├── models/
  │   └── utils/
  ├── tests/
  ├── docs/
  └── docker/
```

## 工具
- **IDE**：VS Code，搭配 vim 鍵盤綁定
- **終端機**：Zsh 搭配 Oh-My-Zsh
- **格式化**：Prettier（每行 100 字元）
- **Linter**：ESLint，使用 airbnb 設定
- **測試框架**：Jest 搭配 React Testing Library

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/memory
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
