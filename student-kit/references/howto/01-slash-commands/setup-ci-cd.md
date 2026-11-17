---
name: setup-ci-cd
description: 實現 pre-commit hooks 和 GitHub Actions 品質保障
---

# 設定 CI/CD 管線

根據專案型別實現完整的 DevOps 品質門禁：

1. **分析專案**：檢測語言、框架、建置系統和現有工具鏈
2. **設定 pre-commit hooks**，使用與語言匹配的工具：
   - 格式化：Prettier/Black/gofmt/rustfmt 等
   - 程式碼檢查：ESLint/Ruff/golangci-lint/Clippy 等
   - 安全：Bandit/gosec/cargo-audit/npm audit 等
   - 型別檢查：TypeScript/mypy/flow（如適用）
   - 測試：執行相關測試套件
3. **建立 GitHub Actions 工作流程**（`.github/workflows/`）：
   - 在 push/PR 時映象 pre-commit 檢查
   - 多版本/多平臺矩陣（如適用）
   - 建置和測試驗證
   - 部署步驟（如需要）
4. **驗證管線**：本地測試、建立測試 PR，確認所有檢查都透過

使用免費/開放原始碼工具。尊重已有設定。保持執行快速。
