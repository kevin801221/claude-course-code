# CLAUDE.md

此檔案在處理本儲存庫中的 Python 程式碼時，為 Claude Code 提供全面的指引。

## 核心開發理念 (Core Development Philosophy)

### KISS (保持簡單，大笨蛋)

簡單應是設計的關鍵目標。盡可能選擇直接的解決方案，而非複雜的方案。簡單的解決方案更易於理解、維護和除錯。

### YAGNI (你將不會需要它)

避免基於推測構建功能。僅在需要時才實作功能，而不是在您預期未來可能有用時實作。

### 設計原則

- **依賴反轉 (Dependency Inversion)**：高層級模組不應依賴低層級模組。兩者皆應依賴抽象。
- **開閉原則 (Open/Closed Principle)**：軟體實體應對擴充開放，但對修改封閉。
- **單一職責 (Single Responsibility)**：每個函式、類別和模組應只有一個清晰的目的。
- **儘早失敗 (Fail Fast)**：儘早檢查潛在錯誤，並在問題發生時立即拋出異常。

## 🧱 程式碼結構與模組化 (Code Structure & Modularity)

### 檔案與函式限制

- **單個檔案不得超過 500 行程式碼**。如果接近此限制，請將其拆分為模組進行重構。
- **函式應在 50 行以內**，具備單一且清晰的職責。
- **類別應在 100 行以內**，代表單一概念或實體。
- **將程式碼組織成清晰分離的模組**，並按功能或職責分組。
- **行長度上限為 100 個字元** (pyproject.toml 中的 ruff 規則)。
- **執行 Python 指令時務必使用虛擬環境** (venv_linux)，包括執行單元測試。

### 專案架構

遵循嚴格的垂直切片 (Vertical Slice) 架構，測試檔案與其測試的程式碼相鄰：

```
src/project/
    __init__.py
    main.py
    tests/
        test_main.py
    conftest.py

    # 核心模組
    database/
        __init__.py
        connection.py
        models.py
        tests/
            test_connection.py
            test_models.py

    auth/
        __init__.py
        authentication.py
        authorization.py
        tests/
            test_authentication.py
            test_authorization.py

    # 功能切片
    features/
        user_management/
            __init__.py
            handlers.py
            validators.py
            tests/
                test_handlers.py
                test_validators.py

        payment_processing/
            __init__.py
            processor.py
            gateway.py
            tests/
                test_processor.py
                test_gateway.py
```

## 🛠️ 開發環境

### UV 套件管理

本專案使用 UV 進行極速的 Python 套件與環境管理。

```bash
# 安裝 UV (如果尚未安裝)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 建立虛擬環境
uv venv

# 同步依賴項
uv sync

# 新增套件 ***切勿直接更新 PYPROJECT.toml 中的依賴項***
# 務必使用 UV ADD
uv add requests

# 新增開發依賴項
uv add --dev pytest ruff mypy

# 移除套件
uv remove requests

# 在環境中執行指令
uv run python script.py
uv run pytest
uv run ruff check .

# 安裝特定 Python 版本
uv python install 3.12
```

### 開發指令

```bash
# 執行所有測試
uv run pytest

# 執行特定測試並顯示詳細輸出
uv run pytest tests/test_module.py -v

# 執行測試並顯示覆蓋率
uv run pytest --cov=src --cov-report=html

# 格式化程式碼
uv run ruff format .

# 執行 Lint 檢查
uv run ruff check .

# 自動修復 Lint 問題
uv run ruff check --fix .

# 型別檢查
uv run mypy src/

# 執行 pre-commit 鉤子
uv run pre-commit run --all-files
```

## 📋 風格與慣例 (Style & Conventions)

### Python 風格指南

- **遵循 PEP8**，並具備以下特定選擇：
  - 行長度：100 個字元 (由 pyproject.toml 中的 Ruff 設定)
  - 字串使用雙引號
  - 在多行結構中使用尾隨逗號
- **函式簽名與類別屬性務必使用型別提示 (Type hints)**
- **使用 `ruff format` 進行格式化** (比 Black 更快的替代方案)
- **使用 `pydantic` v2** 進行資料驗證與設定管理

### Docstring 標準

為所有公開函式、類別和模組使用 Google 風格的 Docstrings：

```python
def calculate_discount(
    price: Decimal,
    discount_percent: float,
    min_amount: Decimal = Decimal("0.01")
) -> Decimal:
    """
    計算產品的折扣價格。

    參數 (Args):
        price: 產品原價
        discount_percent: 折扣百分比 (0-100)
        min_amount: 允許的最低最終價格

    回傳 (Returns):
        套用折扣後的最終價格

    引發 (Raises):
        ValueError: 如果 discount_percent 不在 0 到 100 之間
        ValueError: 如果最終價格低於 min_amount

    範例 (Example):
        >>> calculate_discount(Decimal("100"), 20)
        Decimal('80.00')
    """
```

### 命名慣例

- **變數與函式**：`snake_case`
- **類別**：`PascalCase`
- **常量**：`UPPER_SNAKE_CASE`
- **私有屬性/方法**：`_leading_underscore`
- **型別別名**：`PascalCase`
- **列舉 (Enum) 值**：`UPPER_SNAKE_CASE`

## 🧪 測試策略 (Testing Strategy)

### 測試驅動開發 (TDD)

1. **先寫測試** —— 在實作前定義預期行為。
2. **觀察失敗** —— 確保測試確實測試了某些內容。
3. **編寫最小程式碼** —— 剛好足以讓測試通過。
4. **重構** —— 改進程式碼，同時保持測試通過。
5. **重複** —— 一次處理一個測試。

### 測試最佳實踐

```python
# 務必使用 pytest fixtures 進行設定
import pytest
from datetime import datetime

@pytest.fixture
def sample_user():
    """提供一個用於測試的範例使用者。"""
    return User(
        id=123,
        name="測試使用者",
        email="test@example.com",
        created_at=datetime.now()
    )

# 使用具備描述性的測試名稱
def test_user_can_update_email_when_valid(sample_user):
    """測試使用者在使用有效輸入時可以更新郵件。"""
    new_email = "newemail@example.com"
    sample_user.update_email(new_email)
    assert sample_user.email == new_email

# 測試邊緣情況與錯誤條件
def test_user_update_email_fails_with_invalid_format(sample_user):
    """測試無效的郵件格式會被拒絕。"""
    with pytest.raises(ValidationError) as exc_info:
        sample_user.update_email("not-an-email")
    assert "Invalid email format" in str(exc_info.value)
```

### 測試組織

- 單元測試：隔離測試個別函式/方法。
- 整合測試：測試組件之間的互動。
- 端到端 (E2E) 測試：測試完整的使用者工作流。
- 將測試檔案與其測試的程式碼放在一起。
- 使用 `conftest.py` 共享 fixtures。
- 目標是 80% 以上的程式碼覆蓋率，但重點放在關鍵路徑。

## 🚨 錯誤處理 (Error Handling)

### 異常 (Exception) 最佳實踐

```python
# 為您的領域建立自訂異常
class PaymentError(Exception):
    """支付相關錯誤的基礎異常。"""
    pass

class InsufficientFundsError(PaymentError):
    """當帳戶餘額不足時引發。"""
    def __init__(self, required: Decimal, available: Decimal):
        self.required = required
        self.available = available
        super().__init__(
            f"餘額不足：需要 {required}，目前可用 {available}"
        )

# 使用具體的異常處理
try:
    process_payment(amount)
except InsufficientFundsError as e:
    logger.warning(f"支付失敗：{e}")
    return PaymentResult(success=False, reason="insufficient_funds")
except PaymentError as e:
    logger.error(f"支付錯誤：{e}")
    return PaymentResult(success=False, reason="payment_error")

# 使用內容管理員 (Context Managers) 進行資源管理
from contextlib import contextmanager

@contextmanager
def database_transaction():
    """為資料庫操作提供事務作用域。"""
    conn = get_connection()
    trans = conn.begin_transaction()
    try:
        yield conn
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    finally:
        conn.close()
```

### 記錄 (Logging) 策略

```python
import logging
from functools import wraps

# 配置結構化記錄
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 記錄函式的進入與退出，以便除錯
def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"進入 {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"成功退出 {func.__name__}")
            return result
        except Exception as e:
            logger.exception(f"{func.__name__} 中發生錯誤：{e}")
            raise
    return wrapper
```

## 🔧 配置管理 (Configuration Management)

### 環境變數與設定

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """具備驗證功能的應用程式設定。"""
    app_name: str = "我的應用"
    debug: bool = False
    database_url: str
    redis_url: str = "redis://localhost:6379"
    api_key: str
    max_connections: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """獲取快取的設定實例。"""
    return Settings()

# 使用方式
settings = get_settings()
```

## 🏗️ 資料模型與驗證 (Data Models and Validation)

### 遵循 Pydantic v2 嚴格標準的範例模型

```python
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class ProductBase(BaseModel):
    """具備通用欄位的基礎產品模型。"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category: str
    tags: List[str] = []

    @validator('price')
    def validate_price(cls, v):
        if v > Decimal('1000000'):
            raise ValueError('價格不可超過 1,000,000')
        return v

    class Config:
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }

class ProductCreate(ProductBase):
    """建立新產品的模型。"""
    pass

class ProductUpdate(BaseModel):
    """更新產品的模型 —— 所有欄位皆為選填。"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class Product(ProductBase):
    """具備資料庫欄位的完整產品模型。"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True  # 啟用 ORM 模式
```

## 🔄 Git 工作流

### 分支策略

- `main` —— 生產就緒的程式碼。
- `develop` —— 功能整合分支。
- `feature/*` —— 新功能。
- `fix/*` —— Bug 修復。
- `docs/*` —— 文件更新。
- `refactor/*` —— 程式碼重構。
- `test/*` —— 新增或修復測試。

### Commit 訊息格式

Commit 訊息中切勿包含「Claude Code」或「由 Claude Code 編寫」等字樣。

```
<類型>(<範圍>): <主旨>

<本文>

<腳註>
```
類型：feat, fix, docs, style, refactor, test, chore

範例：
```
feat(auth): 新增雙重驗證 (2FA)

- 實作 TOTP 生成與驗證
- 為驗證器應用程式新增 QR Code 生成
- 更新使用者模型以包含 2FA 欄位

結束 #123
```

## 🗄️ 資料庫命名標準

### 實體特定主鍵 (Entity-Specific Primary Keys)
所有資料庫資料表均使用實體特定主鍵，以保持清晰與一致性：

```sql
-- ✅ 標準化：實體特定主鍵
sessions.session_id UUID PRIMARY KEY
leads.lead_id UUID PRIMARY KEY
messages.message_id UUID PRIMARY KEY
daily_metrics.daily_metric_id UUID PRIMARY KEY
agencies.agency_id UUID PRIMARY KEY
```

### 欄位命名慣例

```sql
-- 主鍵：{實體}_id
session_id, lead_id, message_id

-- 外鍵：{被引用實體}_id
session_id REFERENCES sessions(session_id)
agency_id REFERENCES agencies(agency_id)

-- 時間戳記：{動作}_at
created_at, updated_at, started_at, expires_at

-- 布林值：is_{狀態}
is_connected, is_active, is_qualified

-- 計數：{實體}_count
message_count, lead_count, notification_count

-- 持續時間：{屬性}_{單位}
duration_seconds, timeout_minutes
```

### Repository 模式自動推導

增強型的 `BaseRepository` 會自動推導資料表名稱與主鍵：

```python
# ✅ 標準化：基於慣例的 Repositories
class LeadRepository(BaseRepository[Lead]):
    def __init__(self):
        super().__init__()  # 自動推導為 "leads" 與 "lead_id"

class SessionRepository(BaseRepository[AvatarSession]):
    def __init__(self):
        super().__init__()  # 自動推導為 "sessions" 與 "session_id"
```

**優點**：

- ✅ 自我描述的架構 (Schema)。
- ✅ 清晰的外鍵關係。
- ✅ 消除 Repository 方法覆寫。
- ✅ 與實體命名模式一致。

### 模型與資料庫對齊

模型欄位應與資料庫欄位完全一致，以消除欄位映射的複雜性：

```python
# ✅ 標準化：模型與資料庫完全一致
class Lead(BaseModel):
    lead_id: UUID = Field(default_factory=uuid4)  # 與資料庫欄位匹配
    session_id: UUID                               # 與資料庫欄位匹配
    agency_id: str                                 # 與資料庫欄位匹配
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        alias_generator=None  # 使用確切的欄位名稱
    )
```

### API 路由標準

```python
# ✅ 標準化：具備一致參數命名的 RESTful 路由
router = APIRouter(prefix="/api/v1/leads", tags=["leads"])

@router.get("/{lead_id}")           # GET /api/v1/leads/{lead_id}
@router.put("/{lead_id}")           # PUT /api/v1/leads/{lead_id}
@router.delete("/{lead_id}")        # DELETE /api/v1/leads/{lead_id}

# 子資源 (Sub-resources)
@router.get("/{lead_id}/messages")  # GET /api/v1/leads/{lead_id}/messages
@router.get("/agency/{agency_id}")  # GET /api/v1/leads/agency/{agency_id}
```

關於完整的命名標準，請參閱 [NAMING_CONVENTIONS.md](./NAMING_CONVENTIONS.md)。

## 📝 文件標準

### 程式碼文件

- 每個模組都應有一個 Docstring 說明其用途。
- 公開函式必須具備完整的 Docstrings。
- 複雜邏輯應包含以 `# Reason:` 為前綴的行內註解。
- 保持 `README.md` 更新，包含設定說明與範例。
- 維護 `CHANGELOG.md` 以記錄版本歷史。

### API 文件

```python
from fastapi import APIRouter, HTTPException, status
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get(
    "/",
    response_model=List[Product],
    summary="列出所有產品",
    description="檢索所有啟動產品的分頁列表"
)
async def list_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None
) -> List[Product]:
    """
    檢索具備選用過濾條件的產品。

    - **skip**: 要跳過的產品數量 (用於分頁)
    - **limit**: 要回傳的最大產品數量
    - **category**: 按產品類別過濾
    """
    # 此處為實作內容
```

## 🚀 效能考量 (Performance Considerations)

### 優化指引

- 在優化前進行分析 (Profile) —— 使用 `cProfile` 或 `py-spy`。
- 對昂貴的計算使用 `lru_cache`。
- 對大型數據集優先選擇生成器 (Generators)。
- 對 I/O 密集型操作使用 `asyncio`。
- 對 CPU 密集型任務考慮使用 `multiprocessing`。
- 適當快取資料庫查詢。

### 優化範例

```python
from functools import lru_cache
import asyncio
from typing import AsyncIterator

@lru_cache(maxsize=1000)
def expensive_calculation(n: int) -> int:
    """快取昂貴計算的結果。"""
    # 此處為複雜計算內容
    return result

async def process_large_dataset() -> AsyncIterator[dict]:
    """處理大型數據集而無需全部加載至記憶體。"""
    async with aiofiles.open('large_file.json', mode='r') as f:
        async for line in f:
            data = json.loads(line)
            # 處理並產生 (Yield) 每個項目
            yield process_item(data)
```

## 🛡️ 安全性最佳實踐

### 安全指引

- 切勿提交機密資訊 —— 使用環境變數。
- 使用 Pydantic 驗證所有使用者輸入。
- 對資料庫操作使用參數化查詢。
- 為 API 實作速率限制 (Rate limiting)。
- 使用 `uv` 保持依賴項更新。
- 為所有外部通訊使用 HTTPS。
- 實作正確的身分驗證與授權。

### 安全實作範例

```python
from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """使用 bcrypt 對密碼進行雜湊。"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼與其雜湊值是否匹配。"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_secure_token(length: int = 32) -> str:
    """生成加密安全的隨機 Token。"""
    return secrets.token_urlsafe(length)
```

## 🔍 除錯工具

### 除錯指令

```bash
# 使用 ipdb 進行互動式除錯
uv add --dev ipdb
# 新增中斷點： import ipdb; ipdb.set_trace()

# 記憶體分析
uv add --dev memory-profiler
uv run python -m memory_profiler script.py

# 行分析 (Line profiling)
uv add --dev line-profiler
# 為函式新增 @profile 裝飾器

# 使用 Rich Traceback 進行除錯
uv add --dev rich
# 在程式碼中： from rich.traceback import install; install()
```

## 📊 監控與觀測性 (Observability)

### 結構化記錄

```python
import structlog

logger = structlog.get_logger()

# 帶有上下文的記錄
logger.info(
    "payment_processed",
    user_id=user.id,
    amount=amount,
    currency="USD",
    processing_time=processing_time
)
```

## 📚 實用資源

### 核心工具

- UV 文件： https://github.com/astral-sh/uv
- Ruff： https://github.com/astral-sh/ruff
- Pytest： https://docs.pytest.org/
- Pydantic： https://docs.pydantic.dev/
- FastAPI： https://fastapi.tiangolo.com/

### Python 最佳實踐

- PEP 8： https://pep8.org/
- PEP 484 (型別提示)： https://www.python.org/dev/peps/pep-0484/
- Python 進階指南 (Hitchhiker's Guide)： https://docs.python-guide.org/

## ⚠️ 重要註記

- **切勿假設或猜測** —— 疑有疑惑，請詢問以獲得澄清。
- **在使用前務必驗證檔案路徑與模組名稱**。
- **新增模式或依賴項時，保持 CLAUDE.md 更新**。
- **測試您的程式碼** —— 沒有測試的功能是不完整的。
- **記錄您的決策** —— 未來的開發人員 (包括您自己) 會感謝您的。

## 🔍 搜尋指令要求

**重要**：務必使用 `rg` (ripgrep) 代替傳統的 `grep` 與 `find` 指令：

```bash
# ❌ 不要使用 grep
grep -r "pattern" .

# ✅ 使用 rg 代替
rg "pattern"

# ❌ 不要配合名稱使用 find
find . -name "*.py"

# ✅ 使用 rg 配合檔案過濾
rg --files | rg "\.py$"
# 或
rg --files -g "*.py"
```

**強制執行規則**：

```
(
    r"^grep\b(?!.*\|)",
    "使用 'rg' (ripgrep) 代替 'grep' 以獲得更好的效能與功能",
),
(
    r"^find\s+\S+\s+-name\b",
    "使用 'rg --files | rg pattern' 或 'rg --files -g pattern' 代替 'find -name' 以獲得更好的效能",
),
```

## 🚀 GitHub Flow 工作流摘要

main (受保護) ←── PR ←── feature/您的功能
↓ ↑
部署開發環境 (development)

### 每日工作流：

1. `git checkout main && git pull origin main`
2. `git checkout -b feature/new-feature`
3. 進行變更 + 測試
4. `git push origin feature/new-feature`
5. 建立 PR → 審查 → 合併至 main

---

_此文件是一份活指南。隨著專案演進與新模式的出現，請及時更新。_
