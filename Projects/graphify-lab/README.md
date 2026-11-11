# Graphify：從工單提交追到通知

**課堂問題：工單沒有 email 時，也能建立嗎？會不會寄出通知？** 先用五個 Python 檔產生關係圖，再讀原始碼、跑測試回答。圖可以告訴你有哪些呼叫；只有實際的輸入與測試，才告訴你某一次有沒有走到通知分支。

**先備：** Python 3.10+、[uv](https://docs.astral.sh/uv/getting-started/installation/)。基礎建圖、更新與驗收不需要 Claude 帳號或 API key。文件語意分析才需要可用的 Claude Code session 與模型用量。以下用 `python3`；Windows 可換成 `py -3`。一次只貼一個步驟。

## 1. 安裝指定版本（投影片 02/12）

如果已下載學生 repo，不必再 clone。從 repo 根目錄開始：

```sh
cd Projects/graphify-lab
python3 --version
uv --version
uv tool install graphifyy==0.9.103
graphify --help
```

套件叫 **graphifyy**，指令叫 **graphify**。help 應列出 extract、query、path。若已有其他版本，不必換掉：將下方每個 `graphify …` 命令改寫成 `uvx --from graphifyy==0.9.103 graphify …`。找不到剛安裝的指令，執行 `uv tool update-shell` 後重開終端機。

## 2. 準備五個檔案（03/12）

```sh
python3 prepare.py graphify-demo
python3 checks/check_tickets.py baseline graphify-demo
cd graphify-demo
python3 -c "from app import submit_ticket; print(submit_ticket('Refund','learner@example.test'))"
```

這會建立投影片使用的固定五檔版本，方便全班比較同一份來源與輸出。初版驗收應顯示 4 tests、OK，示範呼叫會印出工單 dict。若要練習從 prompt 生成，可另外開空白目錄，最後和 [starter](starter/) 比對。prepare 不覆寫已有目錄。

| 問題 | 先打開的檔案 |
|---|---|
| 從哪裡提交？ | [app.py](starter/app.py)，submit_ticket 是入口 |
| 誰協調驗證、儲存、通知？ | [service.py](starter/service.py)，create_ticket 依序呼叫三個協作者 |
| 哪裡決定接受什麼輸入？ | [validation.py](starter/validation.py) |
| 怎樣模擬儲存與通知？ | [repository.py](starter/repository.py)、[notification.py](starter/notification.py)，不寫 DB 或寄信 |

後續命令都在剛建立的 **graphify-demo/** 執行；不要從全班教材 repo 根目錄掃描。

## 3. 安裝專案 Skill（04/12，Claude Code 路線）

```sh
graphify install --project
```

先檢查 `.claude/skills/graphify/SKILL.md`、`CLAUDE.md` 和 `.claude/settings.json`，再開 `claude`。這一步會將專案指引與 hooks 寫入練習目錄。只走 CLI 可跳過。接下來的 shell 命令請在終端機執行；以斜線起頭的提示才是貼進 Claude Code。

## 4. 建圖與開圖（05–06/12）

```sh
graphify extract . --code-only
graphify cluster-only . --no-label
python3 -m http.server 8000 --bind 127.0.0.1
```

開啟 [本機 graph.html](http://127.0.0.1:8000/graphify-out/graph.html)，搜尋 create_ticket，再點節點看來源。展示完在終端機按 Ctrl+C；若 8000 被佔用可改 8001。也可直接用瀏覽器開本機 HTML。檢查 `graphify-out/graph.json`、`graph.html` 和 `GRAPH_REPORT.md` 都存在。群集編號與數量不作驗收標準。

## 5. 查範圍與來源（07/12）

```sh
graphify query "create_ticket"
graphify explain "create_ticket()"
```

初版的 create_ticket 定義在 service.py。在 explain 結果中找出 submit_ticket 的呼叫，再到 service.py 確認 validate_ticket、save_ticket、send_notification 的次序與參數。

## 6. 用 path 驗證連線（08/12）

```sh
graphify path "submit_ticket()" "send_notification()"
```

初版應出現兩跳：submit_ticket() → create_ticket() → send_notification()。注意 create_ticket 還有其他相鄰節點，不代表每個節點都是這條最短路徑上的一站。

## 7. 改一段程式，再查圖（09/12）

用教學提供的 [小修改](exercises/notification-update.py.txt) 替換**練習副本**中的 notification.py。它加上 format_message，保留 send_notification。下列命令都在 graphify-demo：

```sh
python3 -c "from shutil import copyfile; copyfile('../exercises/notification-update.py.txt','notification.py')"
graphify update .
graphify explain "format_message()"
graphify path "send_notification()" "format_message()"
graphify cluster-only . --no-label
```

驗收：format_message 的來源在 notification.py，新方法真的被 send_notification 呼叫；舊的提交→通知路徑仍可查到。程式增量更新不等於重新理解 Markdown。

## 8. 加入 PM 規格、匯出筆記（10/12）

```sh
python3 -c "from pathlib import Path; from shutil import copyfile; Path('docs').mkdir(exist_ok=True); copyfile('../docs/ticket-flow.md','docs/ticket-flow.md')"
```

讀 [docs/ticket-flow.md](docs/ticket-flow.md)，它寫的是新需求，初版還沒做到。在 Claude Code 的專案 session 輸入：

```text
/graphify . --update
```

然後請它：「把工單規格連回程式，指出直接從文件讀到的規則、由模型推論的關係，以及尚未確認的地方。」語意抽取結果會隨模型而異。沒有模型帳號時，仍可直接對照規格與來源；此時匯出的只有 code graph，不要宣稱圖已經讀過文件。

回到終端機：

```sh
graphify export obsidian
```

用 Obsidian 的「Open folder as vault」打開 `graphify-out/obsidian/`，確認存在 Markdown 筆記與 graph.canvas。

## 9. 做需求變更與驗收（11–12/12）

先用 [調查提示與比較表](exercises/investigate.md) 提出影響分析。**改程式前**執行：

```sh
python3 ../checks/check_tickets.py acceptance .
```

這時舊版應在 missing email 案例失敗；複製步驟 7 的變更不會讓這個新需求自動過關。按規格修改練習副本，再執行同一條命令，所有案例應通過。測試會直接觀察儲存與通知的呼叫次數。最後重跑 `graphify update .` 與步驟 6 的 path，解釋「圖有這條線、某次呼叫卻不通知」如何同時成立。

想看一個可通過的答案？回上一層，另外建一個目錄，不會覆蓋你的作業：

```sh
cd ..
python3 prepare.py --solution graphify-answer
python3 checks/check_tickets.py acceptance graphify-answer
```

[答案的 service.py](reference/service.py) 與 [validation.py](reference/validation.py) 是唯二需要替換的檔案。驗收比對來源、規格與真實測試；不要用節點數或節省 token 的宣傳數字打分。

套件來源：[Graphify 0.9.103](https://pypi.org/project/graphifyy/0.9.103/)；[上游專案](https://github.com/Graphify-Labs/graphify)。
