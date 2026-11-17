# 研究量到 5 秒，PM 可以承諾產品 5 秒內告警嗎？

你是設備監控產品的工程師，一筆溫度讀值突然衝高，下一秒又回到正常；另一段資料則持續升溫。這次先用相同的合成溫度資料比較三個濾波器，再以 PM 的身分把可追查的實測結果接進產品需求文件（PRD）與工作範圍說明（SoW）。

## 在自己的電腦跑一次

請預先備妥 Python 3.10 以上、CMake 3.20 以上（含 CTest），及 C++17 編譯器。macOS 可使用 Apple Clang。這個練習只用 Python 標準函式庫與本機的編譯工具，解壓後可離線操作，毋須登入 Claude 或 GitHub。

從解壓後的 `claude-code-student-kit/` 開終端機，依序執行：

```sh
cd realtek/cases/autosearch-prd
python3 --version
cmake --version
python3 -m workshop demo --offline --out outputs/lecture
```

終端會依序顯示 B 研究、C 獨立草稿、C 連結 B 證據、變更提案、檢核，最後列出七份產物。重跑時請選一個新的目錄，例如 `outputs/lecture-2`，並將下文的路徑一起換掉。

若已可使用 Claude Code，也可以在**同一個實驗目錄**開啟 `claude`，輸入 `/workshop-bc outputs/lecture-2`。這是同一套離線程式的選用入口；Claude 對話本身需要既有的登入與連線。

## 交出三個能查證的答案

1. **哪個濾波器把一個尖峰判成告警？** 打開 `outputs/lecture/b/research-report.md` 與 `outputs/lecture/b/metrics.csv`。在 eval 的 spike 情境，近五筆移動平均 SMA 在第 122 秒首次誤報；EMA 與 Median 各為零次。另找 sustained_rise，比較三者的偵測延遲。
2. **REQ-004 要填多少秒？** 從 `outputs/lecture/c/linked/versions/v1/traceability.md` 找到 REQ-004，回查 `outputs/lecture/b/evidence.json` 的 B-E041 與它指向的 CSV 列。SMA 在這次合成持續升溫資料測得 **5 秒**，競品資料標示 **10 秒**，使用者希望 **5 秒**。到同目錄的 `prd.md`、`open-questions.md` 看產品負責人尚需解決的問題。延遲上限仍為「待驗證」，對應的產品驗收是 AT-006。
3. **供應商提出多感測器需求，v1 有沒有跟著改？** 打開 `outputs/lecture/c/linked/changes/CR-001.md`、`project.json`（在 `c/linked/`）及 `versions/v1/sow.md`。AT-007 描述 A 升溫時只有 A 告警，AT-008 描述舊格式 CSV 仍可當作單感測器資料。提案狀態為 `proposed`，目前版本為 `v1`。由產品負責人決定是否接受變更、納入下版工作範圍。

**可貼給 Claude Code 的 prompt**

```text
讀取本次 outputs/lecture 的產物。用數據回答 SMA 何時誤報，再從 REQ-004 追到一筆研究測量，列出證據 ID、CSV 路徑、實測值，以及 PRD 裡仍待確認的門檻。最後查 CR-001，告訴我多感測器與舊格式各對應哪一個驗收 ID、提案狀態與目前版本。只讀取這些檔案。
```

離線班也可以用文字編輯器直接查相同的檔案。比較 `c/standalone/versions/v1/prd.md` 與 `c/linked/versions/v1/prd.md`，就能看到研究證據包如何影響草稿寫入的參考值。

## 在本機驗證工作坊

下列指令同樣在實驗目錄執行。C++ 測試驗證濾波與告警行為；Python 測試涵蓋資料重生、證據追溯、檔案異動、變更流程與離線整合。

```sh
cmake -S b_research -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
python3 -m unittest discover -s tests -v
```

預期 CTest 通過 8 項，Python 通過 46 項。確認這次的 `outputs/lecture/c/linked/review.md` 記錄結構檢核結果；產品驗收與語意審查在文件中另列狀態。

## 來源與取用方式

[回到簡報的工作坊操作頁](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_bc_run)。離線課堂版源自 Kevin Luo 的[私人教案 repo](https://github.com/kevin801221/autosearch-PRD-claudecode/tree/f0e10cef442c46cef9eebda4831225374cc4fbd7)，取用版本為 `f0e10cef442c46cef9eebda4831225374cc4fbd7`。程式、測試、模板與合成資料已隨學生包提供。教案的兩項證據引用收錄於[本機的合成案例假設](fixtures/c/notes/classroom-assumptions.md)。
