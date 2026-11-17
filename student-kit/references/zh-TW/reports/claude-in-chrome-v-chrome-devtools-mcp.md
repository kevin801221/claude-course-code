# 瀏覽器自動化 MCP 完整比較報告

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/claude-in-chrome-v-chrome-devtools-mcp.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/claude-in-chrome-v-chrome-devtools-mcp.md)

## 摘要

基於廣泛的研究，本文分析了你截圖中的兩個工具，再加上第三個主要競爭者。以下是完整拆解，協助你為自動化測試挑選最合適的選項。

---

## 1. 三位競爭者

### **A. Chrome DevTools MCP**（截圖 #1）
- **來源：** Google Chrome 官方團隊
- **發布：** 2025 年 9 月公開預覽
- **架構：** 建構在 Chrome DevTools Protocol（CDP）+ Puppeteer 之上
- **Token 用量：** 約 19.0k tokens（脈絡的 9.5%）
- **工具：** 6 大類共 26 個專用工具

### **B. Claude in Chrome**（截圖 #2）
- **來源：** Anthropic 官方擴充套件
- **發布：** Beta，逐步開放給所有付費方案（Pro、Max、Team、Enterprise）
- **架構：** 具備 computer-use 能力的瀏覽器擴充套件
- **Token 用量：** 約 15.4k tokens（脈絡的 7.7%）
- **工具：** 16 個工具，含 computer use 能力

### **C. Playwright MCP**（強力替代方案）
- **來源：** Microsoft（官方 + 社群實作）
- **架構：** 基於無障礙樹（accessibility tree）的自動化
- **Token 用量：** 約 13.7k tokens（脈絡的 6.8%）
- **工具：** 21 個工具

---

## 2. 詳細功能比較

| 功能 | Chrome DevTools MCP | Claude in Chrome | Playwright MCP |
|---------|---------------------|------------------|----------------|
| **主要用途** | 除錯與效能 | 一般瀏覽器自動化 | UI 測試與 E2E |
| **瀏覽器支援** | 僅 Chrome | 僅 Chrome | Chromium、Firefox、WebKit |
| **Token 效率** | 19.0k（9.5%） | 15.4k（7.7%） | 13.7k（6.8%） |
| **元素選取** | CSS/XPath 選擇器 | 視覺 + DOM | 無障礙樹（語意） |
| **效能追蹤** | ✅ 優異 | ❌ 無 | ⚠️ 有限 |
| **網路檢查** | ✅ 深度分析 | ⚠️ 基本 | ⚠️ 基本 |
| **Console 日誌** | ✅ 完整存取 | ✅ 完整存取 | ⚠️ 有限 |
| **跨瀏覽器** | ❌ 無 | ❌ 無 | ✅ 有 |
| **CI/CD 整合** | ✅ 優異 | ❌ 差（需登入） | ✅ 優異 |
| **Headless 模式** | ✅ 有 | ❌ 無 | ✅ 有 |
| **驗證** | 需設定 | 使用你的 session | 需設定 |
| **排程任務** | ❌ 無 | ✅ 有 | ❌ 無 |
| **費用** | 免費 | 需付費方案 | 免費 |
| **本機安裝** | 需要 Node.js | 瀏覽器擴充套件 | 需要 Node.js |

---

## 3. 工具拆解

### Chrome DevTools MCP（26 個工具）

```
輸入自動化 (8):        click, drag, fill, fill_form, handle_dialog,
                      hover, press_key, upload_file

導覽 (6):             close_page, list_pages, navigate_page,
                      new_page, select_page, wait_for

模擬 (2):             emulate, resize_page

效能 (3):             performance_analyze_insight,
                      performance_start_trace, performance_stop_trace

網路 (2):             get_network_request, list_network_requests

除錯 (5):             evaluate_script, get_console_message,
                      list_console_messages, take_screenshot,
                      take_snapshot
```

### Claude in Chrome（16 個工具）

```
瀏覽器控制:            navigate, read_page, find, computer
                      (click, type, scroll)

表單互動:              form_input, javascript_tool

媒體:                  upload_image, get_page_text, gif_creator

分頁管理:              tabs_context_mcp, tabs_create_mcp

開發:                  read_console_messages, read_network_requests

工具:                  shortcuts_list, shortcuts_execute,
                      resize_window, update_plan
```

### Playwright MCP（21 個工具）

```
導覽:                  navigate, goBack, goForward, reload

互動:                  click, fill, select, hover, press,
                      drag, uploadFile

元素查詢:              getElement, getElements, waitForSelector

斷言:                  assertVisible, assertText, assertTitle

頁面狀態:              screenshot, getAccessibilityTree,
                      evaluateScript

瀏覽器管理:            newPage, closePage
```

---

## 4. 自動化測試的使用情境分析

### **Chrome DevTools MCP 最適合：**

✅ **效能測試**
- 錄製含 Core Web Vitals 的效能追蹤
- 找出繪製瓶頸與版面位移
- 記憶體洩漏偵測與 CPU 分析

✅ **深度除錯**
- 網路請求檢查（header、payload、時序）
- Console 錯誤分析與堆疊追蹤
- 即時 DOM 檢查

✅ **CI/CD 管線**
- 支援 headless 執行
- 穩定、腳本式的自動化
- 不依賴驗證狀態

**理想工作流：** 「找出這個頁面為什麼慢」或「除錯這個 API 呼叫」

---

### **Claude in Chrome 最適合：**

✅ **輔助手動測試**
- 在你已登入帳號的狀態下測試
- 帶視覺脈絡的探索式測試
- 錄製可重播的工作流

✅ **快速驗證**
- 設計驗證（比對 Figma 與實際輸出）
- 抽查新功能
- 開發過程中讀取 console 錯誤

✅ **重複性瀏覽器任務**
- 排程自動檢查
- 多分頁工作流管理
- 從你錄製的動作中學習

**理想工作流：** 「檢查我的變更看起來對不對」或「用我的登入狀態測這個表單」

---

### **Playwright MCP 最適合：**

✅ **E2E 測試自動化**
- 跨瀏覽器測試（Chrome、Firefox、Safari）
- 產生可重用的測試腳本
- 產生 Page Object Model

✅ **可靠的 UI 測試**
- 無障礙樹 = 不會有脆弱的選擇器
- 確定性的互動
- 較不容易因 UI 變更而壞掉

✅ **CI/CD 整合**
- 管線可用的 headless 模式
- 從自然語言產生 Playwright 測試檔
- 與測試管理工具整合

**理想工作流：** 「為這個使用者流程寫 E2E 測試」或「跨瀏覽器測試這個」

---

## 5. Token 效率分析

| 工具 | Token 用量 | 佔脈絡比例 | 效率評等 |
|------|-------------|--------------|-------------------|
| Playwright MCP | 約 13.7k | 6.8% | ⭐⭐⭐⭐⭐ 最佳 |
| Claude in Chrome | 約 15.4k | 7.7% | ⭐⭐⭐⭐ 良好 |
| Chrome DevTools MCP | 約 19.0k | 9.5% | ⭐⭐⭐ 可接受 |

**影響：** 以 200k token 脈絡計算：

- Playwright 留下 186.3k tokens 給你的工作
- Claude in Chrome 留下 184.6k tokens
- Chrome DevTools 留下 181k tokens

Playwright 與 Chrome DevTools 之間約 5.3k token 的差距，在有大量程式碼脈絡的複雜 session 中可能很關鍵。

---

## 6. 安全考量

### Chrome DevTools MCP
- ✅ 預設使用隔離的瀏覽器設定檔
- ✅ 不依賴雲端
- ✅ 完全本機控制
- ⚠️ 遠端除錯埠的安全性（請使用隔離設定檔）

### Claude in Chrome
- ⚠️ 無防護措施時**攻擊成功率 23.6%**（加上防禦後降至 11.2%）
- ⚠️ 使用你真實的瀏覽器 session（cookie 曝險）
- ⚠️ 封鎖金融／成人／盜版網站
- ⚠️ 仍在 beta，有已知弱點

### Playwright MCP
- ✅ 隔離的瀏覽器脈絡
- ✅ 不依賴雲端
- ✅ 成熟的安全模型（Microsoft 支持）
- ✅ 能安全處理驗證

---

## 7. 安裝指令

### Chrome DevTools MCP

```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

### Claude in Chrome

```
從 Chrome Web Store 安裝（需要 Pro/Max/Team/Enterprise 方案）
```

### Playwright MCP（推薦）

```bash
# 先安裝瀏覽器
npx playwright install

# 再加進 Claude Code（user 範圍 = 所有專案）
claude mcp add playwright -s user -- npx @playwright/mcp@latest
```

---

## 8. 建議

### **針對你的自動化測試工作流：**

#### 🥇 **主要工具：Playwright MCP**

**用於：** 日常 E2E 測試、跨瀏覽器驗證、產生測試腳本

**理由：**
- token 用量最低（留更多脈絡給你的程式碼）
- 跨瀏覽器支援（Chrome、Firefox、Safari）
- 無障礙樹取徑 = 選擇器更可靠
- 優異的 CI/CD 整合
- 能產生真正的 Playwright 測試檔
- 免費，不需訂閱

#### 🥈 **次要工具：Chrome DevTools MCP**

**用於：** 效能除錯、網路分析、Core Web Vitals

**理由：**
- 在效能追蹤與除錯上無可匹敵
- 深度網路請求檢查
- Google 官方工具，長期支援
- 當你需要回答「為什麼這麼慢？」時不可或缺

#### 🥉 **視情況：Claude in Chrome**

**用於：** 登入狀態下的快速手動驗證、探索式測試、設計驗證

**理由：**
- 適合開發過程中的快速視覺檢查
- 能讀取你的登入狀態
- 對「這看起來對嗎？」的驗證很有用
- CI/CD 或正式測試自動化請略過

---

## 9. 建議的設定

```bash
# 同時安裝 Playwright 與 Chrome DevTools MCP
npx playwright install
claude mcp add playwright -s user -- npx @playwright/mcp@latest
claude mcp add chrome-devtools -s user -- npx chrome-devtools-mcp@latest
```

### 建議的工作流

```
1. 開發        → Claude Code（終端機）
2. 測試        → Playwright MCP（E2E、跨瀏覽器）
3. 除錯        → Chrome DevTools MCP（效能、網路）
4. 驗證        → Claude in Chrome（快速視覺檢查）
5. CI/CD      → Playwright MCP（headless、自動化）
```

---

## 10. 最終結論

| 如果你需要… | 用這個 |
|----------------|----------|
| 跨瀏覽器 E2E 測試 | **Playwright MCP** |
| 效能分析 | **Chrome DevTools MCP** |
| 網路除錯 | **Chrome DevTools MCP** |
| 快速視覺驗證 | **Claude in Chrome** |
| CI/CD 自動化 | **Playwright MCP** |
| 產生測試腳本 | **Playwright MCP** |
| 最低 token 用量 | **Playwright MCP** |
| 登入狀態下的測試 | **Claude in Chrome** |
| Console 日誌除錯 | **Chrome DevTools MCP** |

### **一句話建議：**

**同時安裝 Playwright MCP 與 Chrome DevTools MCP。** 把 Playwright 當主要測試工具（token 效率更好、跨瀏覽器、更適合 E2E）。需要深度效能分析或網路除錯時用 Chrome DevTools。Claude in Chrome 只在你需要登入 session 做快速手動驗證時使用。

---

## 資料來源

- [Chrome DevTools MCP - GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Anthropic - Piloting Claude in Chrome](https://claude.com/blog/claude-for-chrome)
- [Claude in Chrome Help Center](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome)
- [Playwright MCP - GitHub](https://github.com/microsoft/playwright-mcp)
- [Simon Willison - Using Playwright MCP with Claude Code](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)
- [Testomat.io - Playwright MCP Claude Code](https://testomat.io/blog/playwright-mcp-claude-code/)
- [MCP Integration Guide - Scrapeless](https://www.scrapeless.com/en/blog/mcp-integration-guide)
- [Chrome DevTools MCP Guide - Vladimir Siedykh](https://vladimirsiedykh.com/blog/chrome-devtools-mcp-ai-browser-debugging-complete-guide-2025)
- [Addy Osmani - Give your AI eyes](https://addyosmani.com/blog/devtools-mcp/)

---

*本報告由 Claude Code 使用 Opus 4.5 模型於 2025 年 12 月 19 日產生。*
