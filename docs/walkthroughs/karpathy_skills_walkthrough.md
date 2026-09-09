# Karpathy Guidelines Walkthrough — 用一個 plugin 治 AI 的「自作主張」

> **對象**：受夠 AI「亂假設、過度設計、順手改一堆沒叫它改的東西」的工程師
> **形式**：講師現場帶 / 自學
> **時長**：45 分鐘
> **產出**：① 裝好 `andrej-karpathy-skills` plugin ② 講得出 4 原則、能現場示範「裝前 vs 裝後」AI 行為差 ③ 順便學會「一個最小 plugin 長怎樣」
> **核心方法**：不先講原則——先丟一個髒 diff（過度抽象 + 亂假設）讓學員痛，再裝 plugin 跑同一題，對比
> **跟現有教材的關係**：這份**雙用**——
> - 接 **Part 6 CLAUDE.md / 行為準則**：它就是「把好習慣寫成 Claude 看得懂的規則」的最佳真實範例
> - 接 **Part 11 Plugins**：它是**最乾淨的「最小 plugin」解剖標本**（1 個 skill + `plugin.json` + `marketplace.json`，沒有多餘東西）
> 跟 superpowers 的關係：兩個都在「管 Claude 的行為」，本份最後會講**怎麼共存、衝突時誰贏**。

---

## 開場（5 分鐘）：先看 AI 怎麼自作主張

別講原則。先給學員看這個真實情境（出自此 repo 的 `EXAMPLES.md`）：

**你說**：「加一個匯出使用者資料的功能。」

**AI 直接寫**（沒問任何問題）：

```python
def export_users(format='json'):
    users = User.query.all()                 # ← 假設「全部」使用者
    if format == 'json':
        with open('users.json','w') as f:    # ← 假設寫檔、假設路徑
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        ...                                   # ← 假設欄位、假設格式
```

它**一口氣替你做了 4 個沒問過的假設**：全部使用者？（隱私？）寫成檔案？（還是 API？）哪些欄位？（有敏感資料？）資料量多大？

> **教學金句**：「模型會替你做錯誤假設，然後一路往前衝、完全不檢查。」——這就是 Karpathy 那則貼文的原話，這個 plugin 就是來治這個的。

這 plugin 不是教 AI 寫得更炫，是教它**先停下來問**。

---

## 📁 它到底是什麼（先破除一個誤會）

GitHub 描述寫「a single CLAUDE.md file」，但 `multica-ai/andrej-karpathy-skills` 實際**是一個正式的 Claude Code plugin**，結構乾淨到剛好拿來當教材：

```
andrej-karpathy-skills/
├── .claude-plugin/
│   ├── plugin.json          ← plugin 本體宣告（指向 1 個 skill）
│   └── marketplace.json     ← 讓 /plugin install 找得到
├── skills/
│   └── karpathy-guidelines/
│       └── SKILL.md         ← 真正的內容：4 條行為原則
├── CLAUDE.md                ← 同樣 4 原則的 CLAUDE.md 版（手動貼用）
├── CURSOR.md / .cursor/     ← Cursor 版
├── EXAMPLES.md              ← 每條原則的「錯 vs 對」真實範例
└── README.md / README.zh.md
```

> **教學金句**：「同一套規則，它出三種包裝——plugin（自動觸發）、CLAUDE.md（手貼）、Cursor rule（換 IDE）。教學重點不是規則本身，是『一份知識怎麼包成不同載體』。」

來源：Andrej Karpathy 的 X 貼文（`x.com/karpathy/status/2015883857489522876`），把他對 LLM coding 通病的批評，蒸餾成 4 條可執行原則。

---

## 🔌 Phase 0：安裝（5 分鐘）

**方法 A：當 plugin 裝（推薦，會自動觸發）**

```
/plugin marketplace add multica-ai/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

> ⚠️ **這裡是 Part 11 最常考的卡點**：`andrej-karpathy-skills` 是 **plugin 名**、`karpathy-skills` 是 **marketplace id**——`install` 的格式永遠是 `<plugin>@<marketplace-id>`。兩個名字很像，學員一定會貼錯。看 `.claude-plugin/marketplace.json` 的 `id` 跟 `plugins[].name` 對照給他們看。

**方法 B：手動（不想裝 plugin）**

把 `skills/karpathy-guidelines/SKILL.md` 複製到你的 `~/.claude/skills/`，或把 `CLAUDE.md` 內容附到你專案的 CLAUDE.md 後面。

裝完**重啟 Claude Code**（不重啟不會生效——這是 Part 11 通用卡點）。

---

## 🧠 Phase 1：拆 4 原則 ⭐ 最詳細（配 EXAMPLES.md 真實對比）

`SKILL.md` 開宗明義一句 tradeoff：**「這些準則偏向謹慎勝過速度。瑣碎任務自己拿捏。」** 先講這句，學員才不會覺得「那不是很囉嗦」。

### 原則 1 · Think Before Coding（別假設、別藏困惑、攤開取捨）

| 規則 | 白話 |
|---|---|
| 明說假設，不確定就問 | 不要默默替使用者決定 |
| 有多種解讀就全列出 | 不要靜悄悄選一個 |
| 有更簡單做法就講 | 該頂回去就頂回去 |
| 有不懂就停 | 講清楚哪裡不懂、然後問 |

**真實對比**（EXAMPLES.md）：「make the search faster」——爛 AI 默默加 cache + index + async 200 行；好 AI 回「你說的快是：回應時間？吞吐量？體感速度？目前 ~500ms，哪個對你最重要？」

### 原則 2 · Simplicity First（解決問題的最少 code，零臆測）

- 沒叫的功能不要做
- 一次性 code 不要抽象
- 沒要求的「彈性/可設定」不要加
- 不可能發生的錯誤不要 handle
- **寫了 200 行但其實 50 行能解 → 重寫**
- 自問：「資深工程師會不會說這太複雜？」會 → 簡化

**真實對比**：「加個算折扣的 function」——爛 AI 端出 `ABC` + `Enum` + `Protocol` + 策略模式一大坨；好 AI 三行搞定。

### 原則 3 · Surgical Changes（只動你必須動的，只清你自己的爛攤）

- 不要「順手改善」旁邊的 code / 註解 / 格式
- 不要重構沒壞的東西
- 配合既有風格，就算你會用別的寫法
- 看到無關的死碼——**講出來，不要刪**
- 你的改動造成的孤兒（沒用到的 import/變數）才清；既有死碼別動
- 檢驗：**每一行改動都要能直接追到使用者的要求**

### 原則 4 · Goal-Driven Execution（先定成功標準，迴圈到驗證通過）

把任務翻成可驗證目標：

| 模糊任務 | 翻成可驗證目標 |
|---|---|
| 「加驗證」 | 「先寫無效輸入的測試，再讓它過」 |
| 「修這個 bug」 | 「先寫能重現的測試，再讓它過」 |
| 「重構 X」 | 「確保前後測試都綠」 |

多步驟任務先講簡短計畫：`1.[步驟]→驗證:[檢查]`。

> **教學金句**：「強的成功標準讓 AI 能自己 loop；弱的標準（『弄到能動』）只會逼它一直回來問你。」

---

## 📄 Phase 2：把它當「最小 plugin」解剖（Part 11 加碼，10 分鐘）

這個 repo 的 `plugin.json` 短到適合逐行講——對照 Part 11「plugin 結構」：

```json
{
  "name": "andrej-karpathy-skills",
  "skills": ["./skills/karpathy-guidelines"]   // ← plugin 就靠這行指向 skill
}
```

`marketplace.json` 同樣精簡：

```json
{
  "name": "karpathy-skills", "id": "karpathy-skills",   // ← install 用的是這個 id
  "plugins": [{ "name": "andrej-karpathy-skills", "source": "./" }]
}
```

> **教學金句**：「一個 plugin 最小可以多小？這個就是答案——一個 `plugin.json` 指向一個 `SKILL.md`，加一個 `marketplace.json` 讓人 install。Part 11 的 `plugins-from-zero-to-marketplace` 是『教你做』，這個是『真實世界乾淨範本』。」

帶課對照：

| 看哪個檔 | 對到 Part 11 哪個概念 |
|---|---|
| `.claude-plugin/plugin.json` 的 `skills` 欄 | plugin 怎麼綁 skill |
| `.claude-plugin/marketplace.json` 的 `id` vs `plugins[].name` | install 語法 `plugin@marketplace` 的由來 |
| `SKILL.md` 的 `description` | 為什麼這 skill 會在「寫/審/重構 code」時自動觸發 |

---

## ⚙️ Phase 3：跟你既有的 CLAUDE.md / superpowers 怎麼共存

學員一定會問：「我已經有 CLAUDE.md 規則、又裝了 superpowers，這個會不會打架？」

| 來源 | 角色 | 衝突時 |
|---|---|---|
| 使用者明確指示 / 專案 CLAUDE.md | 最高 | 永遠贏 |
| superpowers（process skills） | 決定「怎麼做事」（brainstorm→plan→TDD） | 次之 |
| **karpathy-guidelines** | 決定「下手前的心態」（別假設、別過度設計） | 與上面**互補不衝突** |
| 模型預設行為 | 最低 | 被上面覆蓋 |

> **教學金句**：「superpowers 給你『工作流程』，Karpathy 給你『動手前的紀律』——一個管步驟、一個管心態，疊著用不打架。真打架時，永遠是使用者明確指示說了算。」

---

## 整合 demo：同一題，裝前 vs 裝後（5 分鐘現場）

```
（裝前）你：加一個匯出使用者資料的功能
       Claude：直接寫一坨假設一堆的 code  ← 對照開場那段

（重啟、裝 plugin 後）你：加一個匯出使用者資料的功能
       Claude：先問——全部還是篩選過？檔案還是 API？哪些欄位（隱私）？
              「最簡做法是一個回傳分頁 JSON 的 API endpoint，要走檔案的話我需要更多資訊。你要哪種？」
```

> 這個對比是整堂的高潮——**同一句話、同一個模型，行為天差地別**。學員當場決定回去裝。

---

## 常見問題 / FAQ

**Q：這跟我自己在 CLAUDE.md 寫「不要過度設計」差在哪？**
A：差在「自動觸發 + 有 EXAMPLES 校準」。skill 的 `description` 讓它在寫/審/重構時自動上場；EXAMPLES.md 給模型具體的「錯長這樣、對長這樣」，比你一句「別過度設計」精準得多。

**Q：會不會每件小事都被它囉嗦反問？**
A：SKILL.md 第一句就寫了 tradeoff：偏謹慎勝過速度，**瑣碎任務用 judgment**。真的太囉嗦就在當下說「這個直接做不用問」，使用者明確指示永遠覆蓋它。

**Q：`multica-ai` 跟原作者關係？**
A：核心內容源自 Andrej Karpathy 的 X 貼文、由社群整理（`marketplace.json` owner 標 `forrestchang`）。`multica-ai` 是其中一個流通版本，內含中文 `README.zh.md`。教學用功能一致。

**Q：只想要 Cursor 不用 Claude Code？**
A：repo 內有 `CURSOR.md` + `.cursor/rules/`，同一套 4 原則的 Cursor 版。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `/plugin install` 找不到 | marketplace 沒先 add | 先 `/plugin marketplace add multica-ai/andrej-karpathy-skills` |
| `install` 一直失敗 | 把 plugin 名跟 marketplace id 貼反 | 格式是 `andrej-karpathy-skills@karpathy-skills`（`<plugin>@<marketplace-id>`） |
| 裝了沒感覺 | 沒重啟 Claude Code | 退出再進 |
| 它對每件小事都反問 | 沒講 tradeoff 那句 | 帶課先講「偏謹慎、瑣碎任務自己拿捏」；現場太囉嗦就明確指示 |
| 跟既有 CLAUDE.md 規則疑似衝突 | 不清楚優先序 | 看 Phase 3 表：使用者明確指示 > superpowers > 本 skill > 預設 |
| 學員以為它「只是一個 CLAUDE.md」 | 被 GitHub 描述誤導 | 給看 `.claude-plugin/` + `skills/`，它是正式 plugin |

---

## 講師私房筆記

### 教學順序心法

- **死守「先痛後藥」**：開場那段髒 code 一定要先給，學員痛了才有動機。先講 4 原則學員會放空。
- Phase 2「最小 plugin 解剖」是 Part 11 的隱藏彩蛋——**講 plugin 結構時很多範例太複雜，這個 1 skill 的乾淨到能逐行講**，拿它當 Part 11 的入門標本比自製範例好。
- 4 原則不用平均用力，**原則 1（別假設）+ 原則 3（外科手術式改動）**最戳痛點，多花時間；原則 2/4 帶過。

### 故意踩坑（比口頭講有效）

- **裝前先跑一次**「加匯出功能」讓 Claude 自作主張一坨 → 全班看它假設多離譜 → 重啟裝 plugin → 同一句再跑。對比張力是整堂最高點，不要省。
- 故意把 install 指令的 `@` 兩邊貼反，讓它報錯，再講 `<plugin>@<marketplace-id>`——學員回去 100% 會貼反，先讓他看一次。

### 不同學員角色推薦

| 角色 | 對哪段最有共鳴 | 建議 |
|---|---|---|
| 被 AI 生成 PR 搞煩的 reviewer | 原則 3 外科手術式改動 | 接進團隊 CLAUDE.md，減少無關 diff |
| 新手 vibe coder | 原則 1 + 2 | 先裝這個再開始用 AI 寫東西 |
| 想學做 plugin 的人 | Phase 2 | 拿這個當「最小 plugin」模板改 |
| 已重度用 superpowers | Phase 3 | 理解兩者分工、疊著用 |

### Kevin 親自驗證的真實狀況

- ✅ `gh api` 拉過真實結構：確認是 `plugin.json` + `marketplace.json` + 1 個 `skills/karpathy-guidelines/SKILL.md`，不是單一 CLAUDE.md。
- ✅ EXAMPLES.md 的「export user data」「make search faster」「discount 過度抽象」都是真實 before/after，可直接當投影片素材。
- ⚠️ GitHub 一句話描述會誤導學員以為「只是個 CLAUDE.md」——務必當場打開 `.claude-plugin/` 反證。
- ⚠️ `<plugin>@<marketplace-id>` 兩個名字太像，我自己第一次也差點貼反，這個坑必踩給學員看。

---

## 一句話總結

> **Karpathy Guidelines = 一個最小 plugin，治 AI 四個老毛病：亂假設、過度設計、順手亂改、沒有成功標準。教學雙用——它是 Part 6『把紀律寫成規則』的範本，也是 Part 11『最小 plugin 長怎樣』的乾淨標本。先給髒 code 痛一下，再裝藥對比，學員回去自己會裝。**

---

## 進階閱讀

- 🔗 GitHub: `github.com/multica-ai/andrej-karpathy-skills`（含 `README.zh.md` 中文版、`EXAMPLES.md` 投影片素材）
- 🔗 來源貼文：`x.com/karpathy/status/2015883857489522876`
- 🔗 [`Projects/plugins-from-zero-to-marketplace/README.md`](../../Projects/plugins-from-zero-to-marketplace/README.md) — 自己做 plugin（對照「乾淨範本 vs 從零做」）
- 🔗 [`gitnexus_walkthrough.md`](gitnexus_walkthrough.md) — 同梯新增的進階工具教材
- 🔗 [`course_12hr_walkthrough.md`](course_12hr_walkthrough.md) — 這份插在 Hour 4（Part 6）尾或 Hour 10（Part 11）

---

_Last updated: 2026-05-16_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：gitnexus_walkthrough.md、course_12hr_walkthrough.md、anthropics_marketplace_skills_walkthrough.md_
_對應 PPT：Part 6 CLAUDE.md / 行為準則 ＋ Part 11 Plugins（最小 plugin 解剖）_
