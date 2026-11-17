# Q5．怎麼把團隊偏好的 Mermaid 圖做成共用 Skill？

團隊指定主要流程要用淡紫底、深紫字；補件後仍須回到資料檢查。這題把標準放進專案 Skill，再請 Claude Code 用同一套規則畫圖。課堂包包含可直接比較的兩份原始碼與兩張圖。

| 起點 | 套用團隊色後的參考成品 |
| --- | --- |
| [原始 Mermaid](examples/simple.mmd) · [原始 PNG](examples/simple.png) | [團隊色 Mermaid](examples/team-application.mmd) · [團隊色 PNG](examples/team-application.png) |

## 1．把團隊色留在專案裡

從學生 ZIP 的根目錄執行：

```sh
cd realtek/cases/mermaid-design
claude
```

這個資料夾已帶有 Claude Code 的[設計 Skill](.claude/skills/mermaid-design/SKILL.md)和 [PNG Skill](.claude/skills/mermaid-png/SKILL.md)。在這裡開新會話即可使用；如有專案信任提示，先確認內容。貼入：

```text
/mermaid-design 把本專案的團隊圖表標準寫進 .claude/skills/mermaid-design/SKILL.md，並同步更新它的 assets/product-flow.mmd：主要流程 classDef main 使用填色 #E8E2FA、外框 #8373AD、文字 #2C1D50。從 examples/simple.mmd 另存為 work/approval.mmd，只改 main 的配色，保留所有標籤、判斷、箭頭及補件回路。這一步交付更新後的 Skill 和 .mmd。
```

[SKILL.md](.claude/skills/mermaid-design/SKILL.md) 負責說明「何時用、要檢查什麼」，[風格樣板](.claude/skills/mermaid-design/assets/product-flow.mmd) 則保存可直接沿用的樣式。請打開兩個檔案確認色碼。這個專案的 `.claude/skills/mermaid-design/` 整個資料夾可隨其他專案版控。

## 2．輸出並讀圖

需要 Node.js、[Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) 的 `mmdc`，以及可由該 CLI 使用的 Puppeteer／Chrome。全數安裝後可離線渲染；Claude 對話則需可用的模型服務。先執行 `mmdc --version` 確認工具已在 PATH。

```sh
node .claude/skills/mermaid-png/scripts/export.mjs work/approval.mmd --out work/rendered-approval --formats png --width 760
```

打開 `work/rendered-approval.png`，從「資料齊全？」分別走「齊全」和「缺件」。缺件要經過「補齊資料」再回到同一個檢查；主管拒絕要到「通知拒絕結果」。確認六個節點、六條有向邊及四個分支標籤都保留。

**不使用 Claude 也可驗證**　在同一資料夾直接渲染包內已套用團隊色的參考解答：

```sh
node .claude/skills/mermaid-png/scripts/export.mjs examples/team-application.mmd --out work/reference --formats png --width 760
```

若電腦只有瀏覽器，可先開啟本頁的兩張隨包 PNG，再用文字編輯器比對 .mmd 中的 `classDef main`。

**教材來源**　兩個技能、原始圖、風格樣板與本機渲染器取自講師的 [mermaid-design](https://github.com/kevin801221/mermaid-design/tree/bd9216ed6cc45b03ea86bf498138d6b7ba9d5594)，沿用 [MIT 授權](LICENSE)。課堂包將共用資源放在各 Skill 資料夾內，另附 team-application 圖供比對。
