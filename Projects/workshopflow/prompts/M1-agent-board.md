# M1-agent-board

以下貼入互動式 Claude Code：

請幫我實作第一個 Claude Code Mod，名稱為 agent-board。我正在學習，請先做最小可用版本，並逐步說明。
先讀取已安裝的 plugin-authoring 技能、當前官方 Mods 文件與本機型別。核對 $.agent.list()、Pane、command、按鈕與重畫的真實 API，不要猜 API 名稱。若目前版本或帳號不支援 Mods，請停下回報具體缺少的能力，不要改做假畫面。
需求：
1. 註冊 /agent-board，開啟標題為 Agent Board 的 Pane。
2. 從 $.agent.list() 取得目前 session 可見的代理，顯示 name、description、status；缺少欄位顯示「未提供」。
3. 空清單顯示「目前沒有子代理」。不得硬編假角色、假完成率或假費用。
4. 加入「重新整理」按鈕；按下後重新取得清單並要求 UI 更新，不能只重畫舊資料。
5. Mod 僅讀取與繪製，不額外呼叫模型、不啟動代理、不修改工作或專案檔案。實作 Mod 所需檔案可建立於技能指定目錄。
6. 按目前官方 session dev-mods 流程建立 plugin manifest、hook 設定與實作入口；先檢查現有同名 Mod，避免覆蓋不相關修改。
7. 使用當前 CLI 支援的 plugin validate 驗證，回報實際命令、結果及尚未測到的項目。按官方提示載入，再確認 /plugin 的 Installed 清單與 /agent-board 是否可開啟。
最後回報：實際路徑、各檔用途、驗證結果、我接著應輸入什麼。若出現 no hooks module to load，檢查當次是否真的載入 hook 模組，不要把這行文字當作功能驗收成功。
