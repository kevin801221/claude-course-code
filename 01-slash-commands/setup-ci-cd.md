---
name: setup-ci-cd
description: 為品質保證建立 pre-commit hooks 與 GitHub Actions
---

# 建立 CI/CD 管線

依專案類型調整並建立完整的 DevOps 品質關卡：

1. **分析專案**：偵測使用的語言、框架、建置系統與現有工具
2. **設定 pre-commit hooks**，搭配該語言專屬工具：
   - 格式化：Prettier／Black／gofmt／rustfmt 等
   - Lint：ESLint／Ruff／golangci-lint／Clippy 等
   - 安全性：Bandit／gosec／cargo-audit／npm audit 等
   - 型別檢查：TypeScript／mypy／flow（如適用）
   - 測試：執行相關測試套件
3. **建立 GitHub Actions 工作流程**（.github/workflows/）：
   - 在 push／PR 時鏡射 pre-commit 檢查
   - 多版本／多平台矩陣（如適用）
   - 建置與測試驗證
   - 部署步驟（如有需要）
4. **驗證管線**：本機測試、建立測試用 PR、確認所有檢查都通過

使用免費／開放原始碼工具，尊重現有設定，並讓執行速度保持快速。

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/commands
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
