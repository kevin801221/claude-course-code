# Claude Code：轉圈動畫（The Spinner）

Claude Code 轉圈動畫底下輪播的詞與提示。擷取自 `~/.local/share/claude/versions/2.1.121`。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/claude-spinner-verbs-and-tips.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/claude-spinner-verbs-and-tips.md)
>
> 下方的動詞是 Claude Code 介面上實際顯示的英文字，保留原文不翻譯。

## 轉圈動詞（Spinner words）

| # | Verb | # | Verb | # | Verb | # | Verb |
|---:|---|---:|---|---:|---|---:|---|
| 1 | Accomplishing | 48 | Discombobulating | 95 | Levitating | 142 | Sketching |
| 2 | Actioning | 49 | Doing | 96 | Lollygagging | 143 | Slithering |
| 3 | Actualizing | 50 | Doodling | 97 | Manifesting | 144 | Smooshing |
| 4 | Architecting | 51 | Drizzling | 98 | Marinating | 145 | Sock-hopping |
| 5 | Baking | 52 | Ebbing | 99 | Meandering | 146 | Spelunking |
| 6 | Beaming | 53 | Effecting | 100 | Metamorphosing | 147 | Spinning |
| 7 | Beboppin' | 54 | Elucidating | 101 | Misting | 148 | Sprouting |
| 8 | Befuddling | 55 | Embellishing | 102 | Moonwalking | 149 | Stewing |
| 9 | Billowing | 56 | Enchanting | 103 | Moseying | 150 | Sublimating |
| 10 | Blanching | 57 | Envisioning | 104 | Mulling | 151 | Swirling |
| 11 | Bloviating | 58 | Evaporating | 105 | Mustering | 152 | Swooping |
| 12 | Boogieing | 59 | Fermenting | 106 | Musing | 153 | Symbioting |
| 13 | Boondoggling | 60 | Fiddle-faddling | 107 | Nebulizing | 154 | Synthesizing |
| 14 | Booping | 61 | Finagling | 108 | Nesting | 155 | Tempering |
| 15 | Bootstrapping | 62 | Flambéing | 109 | Newspapering | 156 | Thinking |
| 16 | Brewing | 63 | Flibbertigibbeting | 110 | Noodling | 157 | Thundering |
| 17 | Bunning | 64 | Flowing | 111 | Nucleating | 158 | Tinkering |
| 18 | Burrowing | 65 | Flummoxing | 112 | Orbiting | 159 | Tomfoolering |
| 19 | Calculating | 66 | Fluttering | 113 | Orchestrating | 160 | Topsy-turvying |
| 20 | Canoodling | 67 | Forging | 114 | Osmosing | 161 | Transfiguring |
| 21 | Caramelizing | 68 | Forming | 115 | Perambulating | 162 | Transmuting |
| 22 | Cascading | 69 | Frolicking | 116 | Percolating | 163 | Twisting |
| 23 | Catapulting | 70 | Frosting | 117 | Perusing | 164 | Undulating |
| 24 | Cerebrating | 71 | Gallivanting | 118 | Philosophising | 165 | Unfurling |
| 25 | Channeling | 72 | Galloping | 119 | Photosynthesizing | 166 | Unravelling |
| 26 | Channelling | 73 | Garnishing | 120 | Pollinating | 167 | Vibing |
| 27 | Choreographing | 74 | Generating | 121 | Pondering | 168 | Waddling |
| 28 | Churning | 75 | Gesticulating | 122 | Pontificating | 169 | Wandering |
| 29 | Clauding | 76 | Germinating | 123 | Pouncing | 170 | Warping |
| 30 | Coalescing | 77 | Gitifying | 124 | Precipitating | 171 | Whatchamacalliting |
| 31 | Cogitating | 78 | Grooving | 125 | Prestidigitating | 172 | Whirlpooling |
| 32 | Combobulating | 79 | Gusting | 126 | Processing | 173 | Whirring |
| 33 | Composing | 80 | Harmonizing | 127 | Proofing | 174 | Whisking |
| 34 | Computing | 81 | Hashing | 128 | Propagating | 175 | Wibbling |
| 35 | Concocting | 82 | Hatching | 129 | Puttering | 176 | Working |
| 36 | Considering | 83 | Herding | 130 | Puzzling | 177 | Wrangling |
| 37 | Contemplating | 84 | Honking | 131 | Quantumizing | 178 | Zesting |
| 38 | Cooking | 85 | Hullaballooing | 132 | Razzle-dazzling | 179 | Zigzagging |
| 39 | Crafting | 86 | Hyperspacing | 133 | Razzmatazzing | | |
| 40 | Creating | 87 | Ideating | 134 | Recombobulating | | |
| 41 | Crunching | 88 | Imagining | 135 | Reticulating | | |
| 42 | Crystallizing | 89 | Improvising | 136 | Roosting | | |
| 43 | Cultivating | 90 | Incubating | 137 | Ruminating | | |
| 44 | Deciphering | 91 | Inferring | 138 | Sautéing | | |
| 45 | Deliberating | 92 | Infusing | 139 | Scampering | | |
| 46 | Determining | 93 | Ionizing | 140 | Schlepping | | |
| 47 | Dilly-dallying | 94 | Jitterbugging | 141 | Scurrying | | |

## 提示（Tips）

| ID | 內容 |
|---|---|
| new-user-warmup | 從小功能或 bug 修正開始，請 Claude 先提出計畫，並驗證它建議的編輯 |
| default-permission-mode-config | 用 /config 變更你的預設權限模式（包含 Plan 模式） |
| git-worktrees | 用 git worktree 平行跑多個 Claude session。 |
| color-when-multi-clauding | 同時開多個 Claude session？用 /color 和 /rename 一眼就能分辨。 |
| memory-command | 用 /memory 檢視與管理 Claude 記憶 |
| theme-command | 用 /theme 變更色彩主題 |
| colorterm-truecolor | 試試設定環境變數 COLORTERM=truecolor 取得更豐富的顏色 |
| powershell-tool-env | 設定 CLAUDE_CODE_USE_POWERSHELL_TOOL=1 以啟用 PowerShell 工具（預覽版） |
| status-line | 用 /statusline 設定顯示在輸入框下方的自訂狀態列 |
| prompt-queue | Claude 工作時按 Enter 可以把後續訊息排進佇列。 |
| enter-to-steer-in-relatime | Claude 工作時傳訊息給它，可以即時引導它的方向 |
| todo-list | 處理複雜任務時請 Claude 建立待辦清單，以追蹤進度並保持方向 |
| ide-upsell-external-terminal | 把 Claude 接到你的 IDE · /ide |
| install-github-app | 執行 /install-github-app，就能直接在你的 Github issue 與 PR 裡標記 @claude |
| install-slack-app | 執行 /install-slack-app 以在 Slack 中使用 Claude |
| permissions | 用 /permissions 預先核准與預先拒絕 bash、edit 與 MCP 工具 |
| drag-and-drop-images | 你知道可以把圖片檔拖放進終端機嗎？ |
| paste-images-mac | 用 control+v（不是 cmd+v！）把圖片貼進 Claude Code |
| double-esc | 連按兩下 esc 可把對話倒回先前的時間點 |
| double-esc-code-restore | 連按兩下 esc 可把程式碼與／或對話倒回先前的時間點 |
| continue | 執行 claude --continue 或 claude --resume 以接續對話 |
| rename-conversation | 用 /rename 為你的對話命名，之後在 /resume 裡比較好找 |
| custom-commands | 在專案的 .claude/skills/ 加入 .md 檔即可建立 skill；放在 ~/.claude/skills/ 則適用於任何專案 |
| custom-agents | 用 /agents 針對特定任務最佳化。例如：軟體架構師、程式碼撰寫者、程式碼審查者 |
| agent-flag | 用 --agent <agent_name> 直接與某個子代理開始對話 |
| desktop-app | 用 Claude 桌面 App 在本機或遠端執行 Claude Code：clau.de/desktop |
| web-app | 在雲端執行任務，同時在本機繼續寫程式 · clau.de/web |
| voice-mode | 用 /voice 啟用按住說話的語音聽寫 |
| no-flicker | 試試無閃爍繪製，現在也支援滑鼠 · /tui fullscreen |
| team-artifacts | 從 team-discovery 狀態浮現團隊 artifact 建議 |
| plan-mode-for-complex-tasks | 在做出變更前，用 Plan 模式為複雜請求做準備。按 &lt;cycle-mode key&gt; |
| terminal-setup | 執行 /terminal-setup 以啟用便利的終端機整合，例如 Option+Enter 換行等 |
| shift-enter | 按 Option+Enter（Apple Terminal）或 Shift+Enter 送出多行訊息 |
| shift-enter-setup | 執行 /terminal-setup 以啟用 Option+Enter（Apple Terminal）或 Shift+Enter 換行 |
| vscode-command-install | 開啟命令面板（Cmd+Shift+P）並執行 "Shell Command: Install '&lt;editor&gt;' command in PATH" 以啟用 IDE 整合 |
| shift-tab | 按 &lt;cycle-mode key&gt; 切換聊天模式 |
| image-paste | 用 &lt;image-paste key&gt; 貼上圖片 |
| desktop-shortcut | 用 &lt;suggested shortcut&gt; 在 Claude Code Desktop 接續你的 session |
| remote-control | 透過 remote control 把這個 session 配對到你的手機 |
| push-notif | 長時間任務完成時讓手機提醒你 —— 在 &lt;settings menu&gt; 啟用推播通知 |
| opusplan-mode-reminder | 你的預設模型設定是 Opus Plan 模式。按 &lt;cycle-mode key&gt; |
| frontend-design-plugin | 在處理 HTML/CSS？安裝 frontend-design 外掛 |
