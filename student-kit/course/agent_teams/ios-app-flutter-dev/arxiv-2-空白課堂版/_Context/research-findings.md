# 研究結論（researcher → team lead）

> ⚠️ 本文件中與健康相關的所有內容（閱讀疲勞間隔、呼吸節奏等）**僅供 App 功能設計參考，非醫療或心理治療建議**，不宣稱任何療效。使用者如有相關健康需求，請洽醫療專業人員。

---

## 主題一：arXiv 抓取設定（給 backend-owner）

### 1-1 API 端點與回傳格式

- **端點**：`http://export.arxiv.org/api/query`
- **回傳格式**：Atom 1.0 XML（`<feed>` 包 `<entry>`）
- **查詢參數**：
  | 參數 | 說明 | 備注 |
  |---|---|---|
  | `search_query` | 搜尋條件（`cat:cs.AI` 等）| 必填 |
  | `start` | 0-based 偏移 | 預設 0 |
  | `max_results` | 每次抓幾筆 | 預設 10，最大 2000/call |
  | `sortBy` | 排序欄位（見下節）| 預設 `relevance` |
  | `sortOrder` | `ascending` / `descending` | 配合 sortBy 用 |

**依據**：[arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)（arXiv 官方，長期維護）

---

### 1-2 Entry 主要欄位

| Atom XML 欄位 | 含義 |
|---|---|
| `<id>` | 論文 arXiv ID URL（如 `https://arxiv.org/abs/2405.XXXXX`）|
| `<title>` | 論文標題 |
| `<published>` | **第一版提交日期**（對應「原始投稿日」）|
| `<updated>` | **取回版本提交日期**（若非 v1 則與 published 不同）|
| `<summary>` | 摘要（Abstract）|
| `<author>` → `<name>` | 作者（可多個）|
| `<link>` | HTML 頁面 / PDF 連結 |
| `<arxiv:primary_category>` | 主分類（如 `cs.AI`）|
| `<category>` | 所有分類標籤（可多個）|
| `<arxiv:comment>` | 作者備注 |
| `<arxiv:doi>` | DOI（如有期刊收錄）|

**依據**：同上官方手冊

---

### 1-3 submittedDate vs lastUpdatedDate 差異與選用

| | `sortBy=submittedDate` | `sortBy=lastUpdatedDate` |
|---|---|---|
| 對應欄位 | `<published>`（v1 投稿日）| `<updated>`（最新版更新日）|
| 代表意義 | 論文**首次出現**在 arXiv 的日期 | 論文**最後修訂**的日期 |
| App 情境適合度 | ✅ **更適合「每日最新論文」**：確保抓到當日新送出的論文 | 較不適合：舊論文修訂也會出現 |

**結論**：「最新 5 篇」應用 `sortBy=submittedDate&sortOrder=descending`，再以 `max_results=5` 抓頭 5 筆。
若要保險，可加日期篩選：`submittedDate:[YYYYMMDD0000+TO+YYYYMMDD2359]`

**依據**：[arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)（官方文件）

---

### 1-4 建議收錄的 arXiv 分類

| 分類代碼 | 全名 | 說明 | 建議納入 |
|---|---|---|---|
| `cs.AI` | Artificial Intelligence | Expert Systems、知識表示、規劃、不確定性 AI | ✅ 核心 |
| `cs.LG` | Machine Learning | 監督/非監督/強化學習、Fairness、Explainability | ✅ 核心 |
| `cs.CL` | Computation and Language | NLP、LLM 相關 | ✅ 核心 |
| `cs.CV` | Computer Vision and Pattern Recognition | 影像識別、生成模型 | ✅ 推薦加入 |
| `cs.RO` | Robotics | 機器人、具身智能 | 選配（論文量較少）|
| `stat.ML` | Statistics – Machine Learning | 統計學 ML；自動 cross-list 至 cs.LG | ⚠️ 會重複：已含在 cs.LG 內，不必另加 |

**建議組合**（平衡廣度與相關性）：`cs.AI OR cs.LG OR cs.CL OR cs.CV`

查詢範例：
```
search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.CV&sortBy=submittedDate&sortOrder=descending&max_results=5
```

**依據**：[arXiv Category Taxonomy](https://arxiv.org/category_taxonomy)（官方分類頁，2024 仍有效）

---

### 1-5 速率限制與禮貌間隔

- arXiv **沒有嚴格的 hard rate limit**，但官方文件明確建議：
  > "In cases where the API needs to be called multiple times in a row, we encourage you to play nice and incorporate a **3 second delay** in your code."
- 超量使用（burst）可能收到 HTTP 503，應實作 **exponential backoff**。
- 建議加 descriptive `User-Agent` header（例如 `arxiv-reader-app/1.0`）。
- 本 App 是**每天跑一次**的 daily job，不會連續呼叫，實際上遠低於限制，但仍應在 scheduler 的每次 HTTP 請求之間保留 ≥ 3 秒的間隔以示尊重。

**依據**：
- [arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)（官方）
- [arXiv API forum – rate limit discussion](https://groups.google.com/a/arxiv.org/g/api/c/ycq8giRdZsQ)（2022，社群討論）

---

## 主題二：閱讀疲勞與休息間隔（給 breathing-owner）

> ⚠️ 以下為 App 功能設計參考，非醫療建議。

### 2-1 連續閱讀幾分鐘後提醒休息？

| 依據來源 | 建議間隔 | 適用情境 |
|---|---|---|
| **20-20-20 法則**（美國視光學協會 AAO 推薦）| 每 **20 分鐘** 看 20 英尺外 20 秒 | 眼睛肌肉放鬆 |
| **Pomodoro Technique** | 每 **25 分鐘** 工作後休息 5 分鐘 | 專注力與生產力 |
| **ScienceDirect 研究**（2025，近工作視力眼疲勞研究）| 30 分鐘工作 / 5 分鐘休息 最能降低眼睛疲勞 | 眼疲勞症狀最小化 |
| **神經科學建議**（general cognitive fatigue）| 每 **50–60 分鐘** 休息 5–10 分鐘 | 整體認知疲勞回復 |

**「預設 10 分鐘」是否有依據？**
→ 證據有限。10 分鐘比 20-20-20 的 20 分鐘更保守（提醒更頻繁），算安全選項，但缺乏明確研究支撐這個具體數字。**20 分鐘**更有文獻依據（AAO、多項研究），且不會讓用戶覺得過於打擾。

**建議預設值**：**20 分鐘**（與 20-20-20 法則對齊，有依據、易解釋）。可讓用戶自調（10 / 20 / 30 分鐘）。

**依據**：
- [20-20-20 Rule – Healthline](https://www.healthline.com/health/eye-health/20-20-20-rule)（2023）
- [Impact of break schedules on digital eye strain – ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0014483525002349)（2025）
- [How Often Should You Take Screen Breaks – Lookaway Blog](https://lookaway.com/blog/2026/04/22/how-often-should-you-take-screen-breaks-a-simple-schedule-that-works/)（2026）

---

### 2-2 呼吸節奏：吸 / 吐幾秒？一次做幾輪？

> ⚠️ 以下為 App 功能設計參考，非醫療建議。

#### 兩種主流技法比較

| 技法 | 節奏 | 一輪時長 | 60 秒可做幾輪 | 適合情境 |
|---|---|---|---|---|
| **Box Breathing（盒式呼吸）** | 吸 4 秒 → 屏 4 秒 → 呼 4 秒 → 屏 4 秒 | **16 秒** | **約 3–4 輪** | 專注、冷靜、壓力管理（美國海豹部隊使用）|
| **4-7-8 Breathing**（Weil 醫師設計）| 吸 4 秒 → 屏 7 秒 → 呼 8 秒 | **19 秒** | **約 3 輪（57 秒）**| 焦慮、助眠、放鬆 |

**60 秒閱讀休息動畫的建議方案**：

選用 **Box Breathing（4-4-4-4）**：
- 16 秒 × 3 輪 = **48 秒**，剩餘 12 秒可用於引導文字、過渡動畫
- 若調整為 4 秒 × 3 段（吸/呼/呼）= 12 秒/輪，可做 5 輪（精簡版，去掉屏氣，適合初學者）
- 參考研究（PubMed 2025）：Box breathing 在心血管回復上優於其他節奏

**最終建議動畫設計**（60 秒 session）：
1. 0–2 秒：「深呼吸一下」提示文字
2. 3–50 秒：Box Breathing 動畫，**3 輪** × 16 秒（吸 4→屏 4→呼 4→屏 4）
3. 51–60 秒：「很好，繼續閱讀吧！」收尾

**依據**：
- [Box Breathing vs 4-7-8 – Longevity Technology](https://longevity.technology/news/box-breathing-vs-4-7-8-which-technique-is-better/)（2024）
- [Comparing Square, 4-7-8, 6bpm breathing – PubMed](https://pubmed.ncbi.nlm.nih.gov/39864026/)（2025，對照研究）
- [Box Breathing 60-second reset – D. Brown Management](https://dbmteam.com/insights/box-breathing-the-60-second-mental-reset-tool/)

---

## 主題三：「資訊餵食」App 設計紅線（給全員）

### 3-1 無限滑動（Infinite Scroll）

**為什麼該避免**：
- 移除天然的「停止點」—— 頁底是讓大腦重新評估「繼續嗎？」的自然時機
- 研究顯示：無限滑動對青少年及成人均引發**焦慮、疲勞、罪惡感、壓力**
- 類似吃角子老虎機的「可變比例增強」：每次滑動可能有驚喜，大腦因此上癮

**我們的 App 設計原則**：
- ✅ 呈現**固定 5 篇**論文清單（有頂也有底）
- ✅ 使用者讀完一篇後需明確點擊「下一篇」，不要自動推薦

**依據**：
- [The Scroll Trap – The Brink](https://www.thebrink.me/the-scroll-trap-how-infinite-feeds-hijack-your-brain-like-a-slot-machine/)
- [Infinite Scroll – Freedom.to](https://freedom.to/blog/infinite-scroll/)（含用戶行為研究）
- [Infinite Scrolling, Finite Satisfaction – arXiv](https://arxiv.org/html/2408.09601v1)（2024 學術論文）

---

### 3-2 紅點 / Badge 焦慮（Notification Badges）

**為什麼該避免**：
- 紅色 badge 數字觸發神經系統的「緊急感」—— 與真實緊急狀況的神經反應相似
- 導致用戶**即使不想打開 App 也強迫點擊清零**（強迫行為）
- 設計師 Aza Raskin（無限滾軸發明者）本人公開後悔，並倡導 humane design

**我們的 App 設計原則**：
- ✅ 不顯示未讀 badge 數字
- ✅ 若有推播，僅用**中性描述**（「今日論文已更新」），不用數字或驚嘆號
- ✅ 不設「連續閱讀天數（streak）」計數，避免引發罪惡感

**依據**：
- [Dark Pattern Directory – Card Catalog for Life](https://cardcatalogforlife.substack.com/p/the-dark-pattern-directory-14-manipulation)
- [Dark Patterns and Addictive Designs – Weizenbaum Journal](https://ojs.weizenbaum-institut.de/index.php/wjds/article/view/5_3_2/189)（同儕審查，2023）

---

### 3-3 罪惡感推播與強迫回訪

**為什麼該避免**：
- 「你已 3 天未閱讀論文！」→ 製造罪惡感，而非真實需求
- 此類推播短期提升開啟率，長期導致用戶反感並關閉通知或解除安裝
- **Attention-Capture Damaging Patterns**：學術研究已將此類設計定性為有害 UI 模式

**我們的 App 設計原則**：
- ✅ 推播僅在**用戶設定的時間**出現（可選擇不推播）
- ✅ 內容為「今日有 5 篇新論文」（資訊性），不用情緒化語言
- ✅ **不追蹤閱讀 streak**，不因未閱讀而發送任何通知

**依據**：
- [Attention-Capture Damaging Patterns – CEUR-WS](https://ceur-ws.org/Vol-3957/SOCIALIZE-paper07.pdf)（2024 學術論文）
- [Dark Patterns and Addictive Designs – Weizenbaum Journal](https://ojs.weizenbaum-institut.de/index.php/wjds/article/view/5_3_2/189)

---

## 給 team lead 的可落地預設值建議

> 以下數字可直接抄入 `app-spec.md`，標明「來自研究」即可。

### arXiv 後端設定

| 項目 | 建議值 | 依據強度 |
|---|---|---|
| **領域清單** | `cs.AI, cs.LG, cs.CL, cs.CV` | 強（官方分類）|
| **查詢語法** | `cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.CV` | 強 |
| **排序欄位** | `sortBy=submittedDate` | 強（首選「最新投稿」）|
| **排序方向** | `sortOrder=descending` | 強 |
| **每次取幾筆** | `max_results=5` | 設計決策 |
| **API 禮貌間隔** | **≥ 3 秒**（本 App 每日一次，可設 0，但多 call 時要遵守）| 強（官方規範）|
| **User-Agent** | `arxiv-reader-app/1.0` | 推薦（官方建議）|
| **失敗處理** | HTTP 503 → exponential backoff（min 3 秒）| 官方建議 |

### 閱讀提醒設定

| 項目 | 建議預設值 | 可調範圍 | 依據強度 |
|---|---|---|---|
| **閱讀累積提醒時間** | **20 分鐘** | 10 / 20 / 30 分鐘 | 中強（20-20-20 法則）|

### 呼吸動畫設定

| 項目 | 建議值 | 依據強度 |
|---|---|---|
| **呼吸法** | Box Breathing（4-4-4-4）| 強（有對照研究）|
| **吸氣** | 4 秒 | 強 |
| **屏氣（吸後）** | 4 秒 | 強 |
| **呼氣** | 4 秒 | 強 |
| **屏氣（呼後）** | 4 秒 | 強 |
| **一輪時長** | 16 秒 | 計算 |
| **60 秒 session 輪數** | **3 輪**（48 秒動畫 + 12 秒引導文字）| 強 |

### 設計紅線（全員遵守）

| 禁止項目 | 替代做法 |
|---|---|
| 無限滾軸 | 固定 5 篇，有頂有底 |
| 紅點 badge 計數 | 無 badge，或僅顯示「新」文字標籤 |
| 罪惡感推播（「X 天未讀」）| 僅在用戶設定時間推「今日論文已更新」 |
| 連續閱讀 streak | 不實作 streak 功能 |
| 自動播放下一篇 | 需用戶明確點擊 |

---

*研究完成時間：2026-05-23*
*researcher：研究先行，不含任何 App 程式碼。*
