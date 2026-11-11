# Lab 05：Hook 是可獨立測試的程式

講義 Part 12。本包的 [guard.py](guard.py) 接收 PreToolUse stdin JSON，針對 Write/Edit 的 `.env*` 與 `secrets/` 路徑回傳拒絕決策。這是依 [官方 Hook 契約](https://code.claude.com/docs/en/hooks) 新寫的最小教學版。

## 先離線看結果

從 Repo 根目錄執行：

```bash
printf '%s' '{"tool_name":"Write","tool_input":{"file_path":".env.demo"}}' | python3 labs/05-hooks/guard.py
npm test
```

拒絕回應含 `hookSpecificOutput.permissionDecision: "deny"`。把路徑改為 `src/demo.mjs`，stdout 應為空；壞 JSON 回傳 2 並在 stderr 說明。

## 再於 Claude 載入

先讀 [settings.example.json](settings.example.json)，再從根目錄啟動：

```bash
claude --permission-mode manual --settings labs/05-hooks/settings.example.json
```

對話中請 Claude 用 Write 工具建立 `.env.demo`，內容只用 `DEMO=sample`；應看到 Hook 拒絕，檔案不應出現。再試用 Write 建立 `.outputs/hook-demo.txt`，確認一般路徑可進入正常權限流程。

## 驗收與限制

辨識「程序成功回傳 JSON」與「工具被允許」是兩件事。示範只涵蓋 Write/Edit 的字面路徑，**不涵蓋 Bash、其他工具、符號連結或完整防外洩**。不要用它代替作業系統隔離與產品權限。

未把 Hook 寫入全域設定。關閉本次 session，正常從根目錄重開即可回到根層設定；若你自己合併了 local/global hooks，須自行移除該項並重新確認。

講義同題原碼：[pomodoro](../../examples/lecture-mini-projects/pomodoro/README.md)，包含隔離 smoke test，先驗證再考慮啟用。
