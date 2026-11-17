# Course Review

課堂用的本機只讀審查 Skill，依任務卡與來源程式回報可重現的問題。使用方式見上層 [Lab 07](../README.md)。不含 Hooks、MCP 或需登入的第三方整合，不自動修改檔案或發布評論。

This teaching plugin packages a single review skill for local Claude Code sessions. Start Claude from the student kit root with the plugin directory flag, then invoke the namespaced review command with the files you want to inspect. The skill asks for concrete evidence, distinguishes static findings from executed checks, and does not publish comments or change source files. Model access depends on your own Claude account.
