# 測試指南

本文件說明 Claude How To 的測試架構。

## 總覽

本專案使用 GitHub Actions，在每次 push 與 pull request 時自動執行測試。測試涵蓋範圍包括：

- **單元測試**：使用 pytest 執行的 Python 測試
- **程式碼品質**：用 Ruff 進行 lint 與格式化
- **安全性**：用 Bandit 進行漏洞掃描
- **型別檢查**：用 mypy 進行靜態型別分析
- **建置驗證**：EPUB 產生測試

## 在本機執行測試

### 先備知識

```bash
# 安裝 uv（快速的 Python 套件管理工具）
pip install uv

# 或在 macOS 上用 Homebrew 安裝
brew install uv
```

### 設定環境

```bash
# 複製儲存庫
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# 建立虛擬環境
uv venv

# 啟用虛擬環境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安裝開發用相依套件
uv pip install -r requirements-dev.txt
```

### 執行測試

```bash
# 執行所有單元測試
pytest scripts/tests/ -v

# 執行測試並計算涵蓋率
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# 執行特定測試檔案
pytest scripts/tests/test_build_epub.py -v

# 執行特定測試函式
pytest scripts/tests/test_build_epub.py::test_function_name -v

# 以監看模式執行測試（需要 pytest-watch）
ptw scripts/tests/
```

### 執行 Lint

```bash
# 檢查程式碼格式
ruff format --check scripts/

# 自動修正格式問題
ruff format scripts/

# 執行 linter
ruff check scripts/

# 自動修正 linter 問題
ruff check --fix scripts/
```

### 執行安全性掃描

```bash
# 執行 Bandit 安全性掃描
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/

# 產生 JSON 報告
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/ -f json -o bandit-report.json
```

### 執行型別檢查

```bash
# 用 mypy 檢查型別
mypy scripts/ --ignore-missing-imports --no-implicit-optional
```

## GitHub Actions 工作流程

### 觸發時機

- **Push** 到 `main` 或 `develop` 分支（當 scripts 變更時）
- 對 `main` 發出 **Pull Request**（當 scripts 變更時）
- 手動觸發工作流程

### Job

#### 1. 單元測試（pytest）

- **執行環境**：Ubuntu 最新版
- **Python 版本**：3.10、3.11、3.12
- **執行內容**：
  - 從 `requirements-dev.txt` 安裝相依套件
  - 執行 pytest 並產生涵蓋率報告
  - 將涵蓋率上傳至 Codecov
  - 封存測試結果與涵蓋率 HTML

**結果**：只要有任何測試失敗，工作流程就會失敗（關鍵項目）

#### 2. 程式碼品質（Ruff）

- **執行環境**：Ubuntu 最新版
- **Python 版本**：3.11
- **執行內容**：
  - 用 `ruff format` 檢查程式碼格式
  - 用 `ruff check` 執行 linter
  - 回報問題但不會讓工作流程失敗

**結果**：不會擋下流程（僅顯示警告）

#### 3. 安全性掃描（Bandit）

- **執行環境**：Ubuntu 最新版
- **Python 版本**：3.11
- **執行內容**：
  - 掃描安全性漏洞
  - 產生 JSON 報告
  - 將報告以 artifact 形式上傳

**結果**：不會擋下流程（僅顯示警告）

#### 4. 型別檢查（mypy）

- **執行環境**：Ubuntu 最新版
- **Python 版本**：3.11
- **執行內容**：
  - 執行靜態型別分析
  - 回報型別不符
  - 協助提早抓出錯誤

**結果**：不會擋下流程（僅顯示警告）

#### 5. 建置 EPUB

- **執行環境**：Ubuntu 最新版
- **相依於**：pytest、lint、security（皆須通過）
- **執行內容**：
  - 用 `scripts/build_epub.py` 建置 EPUB 檔案
  - 驗證 EPUB 是否成功產生
  - 將 EPUB 以 artifact 形式上傳

**結果**：若建置失敗，工作流程就會失敗（關鍵項目）

#### 6. 摘要

- **執行環境**：Ubuntu 最新版
- **相依於**：所有其他 job
- **執行內容**：
  - 產生工作流程摘要
  - 列出所有 artifact
  - 回報整體狀態

## 撰寫測試

### 測試結構

測試應放在 `scripts/tests/` 目錄下，檔名格式為 `test_*.py`：

```python
# scripts/tests/test_example.py
import pytest
from scripts.example_module import some_function

def test_basic_functionality():
    """測試 some_function 是否正常運作。"""
    result = some_function("input")
    assert result == "expected_output"

def test_error_handling():
    """測試 some_function 是否能妥善處理錯誤。"""
    with pytest.raises(ValueError):
        some_function("invalid_input")

@pytest.mark.asyncio
async def test_async_function():
    """測試非同步函式。"""
    result = await async_function()
    assert result is not None
```

### 測試最佳實踐

- **使用描述性名稱**：`test_function_returns_correct_value()`
- **每個測試一個斷言**（盡可能）：更容易除錯失敗案例
- **使用 fixture** 來重複使用設定：參見 `scripts/tests/conftest.py`
- **模擬（mock）外部服務**：使用 `unittest.mock` 或 `pytest-mock`
- **測試邊界情況**：空輸入、None 值、錯誤
- **保持測試快速**：避免使用 sleep() 與外部 I/O
- **使用 pytest 標記**：慢速測試用 `@pytest.mark.slow`

### Fixture

常用的 fixture 定義在 `scripts/tests/conftest.py` 中：

```python
# 在測試中使用 fixture
def test_something(tmp_path):
    """tmp_path fixture 提供一個暫存目錄。"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

## 涵蓋率報告

### 本機涵蓋率

```bash
# 產生涵蓋率報告
pytest scripts/tests/ --cov=scripts --cov-report=html

# 在瀏覽器中開啟涵蓋率報告
open htmlcov/index.html
```

### 涵蓋率目標

- **最低涵蓋率**：80%
- **分支涵蓋率**：已啟用
- **重點區域**：核心功能與錯誤路徑

## Pre-commit Hooks

本專案使用 pre-commit hooks，在 commit 前自動執行檢查：

```bash
# 安裝 pre-commit hooks
pre-commit install

# 手動執行 hooks
pre-commit run --all-files

# 跳過某次 commit 的 hooks（不建議）
git commit --no-verify
```

`.pre-commit-config.yaml` 中設定的 hooks：
- Ruff 格式化工具
- Ruff linter
- Bandit 安全性掃描工具
- YAML 驗證
- 檔案大小檢查
- 合併衝突偵測

## 疑難排解

### 測試在本機通過，但在 CI 上失敗

常見原因：
1. **Python 版本差異**：CI 使用 3.10、3.11、3.12
2. **缺少相依套件**：更新 `requirements-dev.txt`
3. **平台差異**：路徑分隔符號、環境變數
4. **不穩定測試**：依賴時序或執行順序的測試

解決方式：
```bash
# 用相同的 Python 版本測試
uv python install 3.10 3.11 3.12

# 用乾淨的環境測試
rm -rf .venv
uv venv
uv pip install -r requirements-dev.txt
pytest scripts/tests/
```

### Bandit 回報誤判

有些安全性警告可能是誤判。可在 `pyproject.toml` 中設定：

```toml
[tool.bandit]
exclude_dirs = ["scripts/tests"]
skips = ["B101"]  # 跳過 assert_used 警告
```

### 型別檢查過於嚴格

針對特定檔案放寬型別檢查：

```python
# 加在檔案開頭
# type: ignore

# 或加在特定行
some_dynamic_code()  # type: ignore
```

## 持續整合最佳實踐

1. **保持測試快速**：每個測試應在 1 秒內完成
2. **不要測試外部 API**：模擬外部服務
3. **獨立測試**：每個測試都應該互不依賴
4. **使用清楚的斷言**：用 `assert x == 5` 而非 `assert x`
5. **處理非同步測試**：使用 `@pytest.mark.asyncio`
6. **產生報告**：涵蓋率、安全性、型別檢查

## 資源

- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 貢獻測試

提交 PR 時：

1. **撰寫測試**，涵蓋新功能
2. **在本機執行測試**：`pytest scripts/tests/ -v`
3. **檢查涵蓋率**：`pytest scripts/tests/ --cov=scripts`
4. **執行 lint**：`ruff check scripts/`
5. **安全性掃描**：`bandit -r scripts/ --exclude scripts/tests/`
6. 若測試有變更，**請更新文件**

所有 PR 都必須包含測試！🧪

---

若有測試相關的問題，請開一個 GitHub Issue 或討論。
