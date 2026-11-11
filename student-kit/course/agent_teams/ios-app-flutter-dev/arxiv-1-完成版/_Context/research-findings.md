⚠️ 本文件僅供 App 功能設計參考,非醫療或心理治療建議;引用均標來源。

# 研究結論(researcher 產出,給 team lead 收斂進 app-spec.md)

> 研究先行的目的:讓 App 的功能設計**有依據**,而不是拍腦袋。
> 三節對應三個下游模組:第 1 節給 backend-owner、第 2 節給 breathing-owner、第 3 節給全員設計紅線。
> 每個結論後標「依據」:來源 + 連結 + 查證日期(2026-05-22)。拿不準的標「證據有限 / 仍有爭議」。

---

## 1. arXiv 抓取設定(給 backend-owner 依據)

### 1.1 該收哪些科技領域分類
**可落地建議值**:MVP 預設收 `cs.AI`(人工智慧)、`cs.LG`(機器學習)、`cs.CL`(計算語言學 / NLP)三類即可達成「最新科技論文」定位。若想擴大科技覆蓋面,**建議再加 `cs.CV`(電腦視覺)與 `cs.RO`(機器人)** 這兩個高熱度科技分類;統計類的 `stat.ML` 與 cs.LG 高度重疊,可選擇性納入。

- 各分類定義:
  - `cs.AI` — 涵蓋 AI 各領域,但**不含** Vision、Robotics、Machine Learning、Multiagent、Computation and Language(這些有各自分類)
  - `cs.LG` — 機器學習研究全面向(監督 / 非監督 / 強化學習 / bandit 等)
  - `cs.CL` — Computation and Language(計算語言學、NLP、語音處理)
  - `cs.CV` — 影像處理、電腦視覺、模式辨識、場景理解
  - `cs.RO` — Robotics
- **注意**:arXiv 一篇論文可同時掛多個分類,用 `cs.AI OR cs.LG OR cs.CL` 抓取時可能出現同一篇重複命中,backend 取「最新 5 篇」時應**依 arxivId 去重**再截斷。

> 依據:arXiv Category Taxonomy 官方分類表 https://arxiv.org/category_taxonomy ;Computer Science Subject Areas https://arxiv.org/corr/subjectclasses (查證 2026-05-22)。各分類「涵蓋 / 不含」描述為官方 taxonomy 原文。

### 1.2 API 端點與回傳格式
**可落地建議值**:
- 端點:`http://export.arxiv.org/api/query`(GET)
- 回傳格式:**Atom 1.0 XML**(不是 JSON),backend 需用 XML / Atom parser 解析(如 Python `feedparser`)
- 每筆 entry(`<entry>`)可解析的欄位:

| Atom 欄位 | 意義 | 對應 API 契約欄位 |
|---|---|---|
| `<title>` | 論文標題 | `papers[].title` |
| `<id>` | 摘要頁 URL(`http://arxiv.org/abs/<arxivId>`),可從中切出 arxivId | `papers[].arxivId` |
| `<published>` | v1 首次投稿日期 | (排序 / 顯示用) |
| `<updated>` | 取回版本的投稿日期 | (排序 / 顯示用) |
| `<summary>` | 摘要(abstract) | `papers[].summary`(或丟給 Gemini 再整理) |
| `<author><name>` | 作者(可多個) | `papers[].authors` |
| `<link>` | 最多 3 個 URL:摘要頁 / PDF /(可選)DOI | `papers[].link` |
| `<category>` | 分類(可多個) | (篩選 / 顯示用) |
| `<arxiv:primary_category>` | 主分類 | (顯示用) |
| `<arxiv:comment>` / `<arxiv:journal_ref>` / `<arxiv:doi>` | 作者註解 / 期刊出處 / DOI(若有) | (可選) |

> 依據:arXiv API User's Manual https://info.arxiv.org/help/api/user-manual.html ;arXiv API Basics https://info.arxiv.org/help/api/basics.html (查證 2026-05-22)。欄位名稱為手冊原文。

### 1.3 「最新 5 篇」排序:submittedDate vs lastUpdatedDate
**可落地建議值**:用 `sortBy=submittedDate&sortOrder=descending`,符合 app-spec 「每天抓最新投稿」定位。

- `submittedDate` — 依**首次投稿(v1)時間**排序;要的是「今天剛上架的新論文」就用這個。
- `lastUpdatedDate` — 依**最近一次改版時間**排序;會把舊論文因為小改版又浮上來,不適合「每日最新」場景。
- 完整 query 範例:
  ```
  http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=5
  ```
- **提醒**:`max_results=5` 是抓 5 筆;若 1.1 要先去重,建議多抓一點(如 `max_results=15`)再去重截前 5 篇,避免去重後不足 5 篇。

> 依據:arXiv API User's Manual,sortBy 支援 `submittedDate` / `lastUpdatedDate`,差異為「初次投稿 vs 最近改版」https://info.arxiv.org/help/api/user-manual.html (查證 2026-05-22)。

### 1.4 取用速率限制 / 禮貌間隔
**可落地建議值**:**每次 request 間隔至少 3 秒**,且**同時只開 1 條連線**。MVP 每天只抓一次、量很小,務必遵守以免被限流(HTTP 429)。

- arXiv 官方 Terms of Use:對 legacy API(含本 API、OAI-PMH、RSS)要求「**每 3 秒不超過 1 次請求**」、單一連線。
- 限制是**以使用者掌控的所有機器為整體**計算,不可用多台機器繞過;有更高流量需求要聯絡 arXiv support。
- 落地做法:backend 連續呼叫時程式內**自帶 3 秒 delay**;本 App 每天 cron 跑一次、一次抓 5 篇,自然遠低於限制。

> 依據:Terms of Use for arXiv APIs https://info.arxiv.org/help/api/tou.html ;arXiv API User's Manual https://info.arxiv.org/help/api/user-manual.html (查證 2026-05-22)。

---

## 2. 閱讀疲勞與休息間隔(給 breathing-owner 依據)

### 2.1 連續閱讀累積多久提醒休息一次
**可落地建議值**:app-spec 預設的 **10 分鐘門檻是合理且偏保守的選擇**,可採用。它落在兩個常見參考之間:

- **20-20-20 法則**:每用螢幕 **20 分鐘**,看 **20 英尺(約 6 公尺)外** 的東西 **20 秒**。由驗光師 Jeffrey Anshel 於 1990 年代末提出,**美國眼科醫學會(AAO)與美國驗光協會(AOA)背書**作為減緩數位眼睛疲勞的方法。
- **證據限制(要誠實標註)**:此法則**目前缺乏同儕審查研究實證**;近期甚至有研究指出 20-20-20 對自覺症狀 / 閱讀速度 / 任務正確率**無顯著效果**,並建議「**每小時休息 5 分鐘**」這類較長休息可能更有效。→ 屬「**證據有限 / 仍有爭議**」。
- **對本 App 的取捨**:
  - 採 **10 分鐘**門檻 = 比 20 分鐘更早提醒、休息更頻繁,方向與「短而頻繁的休息」一致,作為 MVP 預設安全。
  - 提醒文案**不要宣稱療效**(因證據有限),定位為「溫和提醒你抬頭休息一下」。
  - 建議把門檻做成**可調 / 可關**,尊重使用者(呼應第 3 節紅線)。

> 依據:American Optometric Association / American Academy of Ophthalmology 對 20-20-20 的說明(NVISION 整理)https://www.nvisioncenters.com/education/20-20-20-rule/ ;質疑其實證、提出「每小時 5 分鐘」的近期研究討論 https://www.optometrytimes.com/view/deconstructing-20-20-20-rule-digital-eye-strain 、 https://www.sunshineoptometry.com/blog/new-study-challenges-the-effectiveness-of-the-20-20-20-rule-for-eye-strain (查證 2026-05-22)。

### 2.2 深呼吸的吸 / 吐節奏、做幾輪
**可落地建議值**:60 秒呼吸動畫建議用 **Box Breathing(4-4-4-4)**:**吸 4 秒 → 停 4 秒 → 吐 4 秒 → 停 4 秒**,一輪 16 秒,**做約 4 輪(約 64 秒)** 剛好對上 app-spec 的「60 秒呼吸動畫」。

- **Box Breathing(4-4-4-4)**:吸 / 停 / 吐 / 停各 4 秒;一輪 16 秒(約 3.75 次呼吸/分);初學建議做 4 輪。**節奏對稱、圓圈動畫好做**(四邊等長),適合「專注 / 回神」場景 → **本 App 首選**。
- **替代:4-7-8 呼吸**:吸 4 秒 → 停 7 秒 → 吐 8 秒;偏「放鬆 / 助眠」。初學做 4 輪,熟練可到 8 輪;**一次別超過 8 輪**(可能頭暈)。因 7 秒停氣對新手較難、且偏助眠,**不建議當 MVP 預設**。
- **動畫落地**:圓圈「放大=吸氣、維持=停、縮小=吐氣」;Box Breathing 四階段等長最容易用等速動畫表現。提示**溫和、可略過,不宣稱療效**。

> 依據:Box Breathing 4-4-4-4(一輪 16 秒、約 3.75 breaths/min、建議 4 輪)與 4-7-8(吸4停7吐8、4–8 輪、勿超過 8 輪)比較 https://www.oxalife.com/post/box-breathing-vs-4-7-8-breathing 、 https://boxbreathingexercise.com/box-breathing-vs-4-7-8/ ;4-7-8 出處 Andrew Weil 整合醫學中心 https://awcim.arizona.edu/health_hub/awcimagazine/just_breathe_using_breathwork_for_wellbeing.html (查證 2026-05-22)。註:呼吸法的臨床效益**證據強度不一**,本 App 僅作休息引導,非治療。

---

## 3. 「資訊餵食」App 不該用的成長駭客做法(給全員設計紅線)

**核心原則**:本 App 定位是「每天讀完一份就好、讀久了提醒休息」的**有界限、尊重時間**的閱讀器,**刻意不採用以下「黏著度 / 成長駭客」暗黑模式(dark patterns)**。暗黑模式由 UX 設計師 Harry Brignull 於 2010 年命名,指「刻意設計來誘導使用者做出非其最佳利益選擇」的手法。

| 該避免的做法 | 為什麼有害 | 本 App 的對策 |
|---|---|---|
| **無限滑(infinite scroll)** | 移除自然停止點,靠「間歇性增強(同賭場拉霸原理)+ Zeigarnik 未完成效應 + 多巴胺迴圈」讓人停不下來;發明者 Aza Raskin 本人都公開後悔。 | 每日報告**固定 5 篇、有明確結尾**;讀完就是讀完,不續抓、不自動載入更多。 |
| **紅點 / badge 焦慮** | 用未讀數字 / 紅點製造「不點開不安」,驅動強迫性開啟。 | **不用未讀紅點**;最多顯示「今天有新報告」中性提示,不堆積數字。 |
| **罪惡感推播 / confirmshaming** | 用「你已經 3 天沒讀了」「確定要錯過嗎」等羞辱 / 罪惡感文案綁架使用者。 | 文案保持中性鼓勵;**MVP 不做推播**(用 app 內計時提醒),不用罪惡感字眼。 |
| **自動播放 / 個人化無限餵食** | 與無限滑同列為「成癮性設計」,助長強迫使用(歐盟 2026 對 TikTok 的初步認定即點名 infinite scroll / autoplay / push / 個人化推薦)。 | 報告每日全使用者**共用、非個人化**(已在 app-spec MVP 邊界);無自動播放。 |

**為什麼這對產品也好(不只是道德)**:暗黑模式雖短期拉高停留時間,卻帶來**成癮、疲勞、後悔**,長期**侵蝕信任**;被揭露時常引發公關反彈,重建信任遠難於一開始就誠實設計。本 App 的休息提醒(第 2 節)本身就是「反成癮」訴求,**設計上必須前後一致**——不能一邊提醒休息、一邊用黏著手法把人留住。

> 依據:Dark patterns 定義與 confirmshaming https://www.scalablepath.com/ui-ux-design/dark-pattern-examples ;UX Dark Patterns 與社群成癮 https://www.designorate.com/ux-dark-patterns-and-social-media-addiction/ ;infinite scroll 心理機制與 Aza Raskin 後悔、Center for Humane Technology「Time Well Spent」https://www.humanetech.com/the-cht-perspective ;歐盟對成癮性設計(infinite scroll / autoplay / push)的監管動向 https://www.fairpatterns.ai/post/dark-patterns-social-media-gaming-and-e-commerce (查證 2026-05-22)。

---

## 給 team lead 的收斂提示(對應 app-spec.md「研究結論」四欄)
1. **arXiv 領域與排序**:預設 `cs.AI / cs.LG / cs.CL`(可加 `cs.CV / cs.RO`),`sortBy=submittedDate&sortOrder=descending`,抓取後依 arxivId 去重再取前 5;間隔 3 秒、單連線。
2. **閱讀提醒間隔**:10 分鐘門檻合理(介於 20-20-20 與「每小時 5 分鐘」之間),但實證有限 → 不宣稱療效、做成可調可關。
3. **呼吸節奏**:Box Breathing 4-4-4-4(吸4停4吐4停4),約 4 輪 ≈ 64 秒,對齊 60 秒動畫;溫和可略過。
4. **設計紅線**:不做無限滑 / 紅點 / 罪惡感推播 / 自動播放;每日固定 5 篇有結尾、非個人化、無未讀數字。
