name: "基礎 PRP 範本 v2 - 具備驗證迴圈的豐富上下文 (Base PRP Template v2 - Context-Rich with Validation Loops)"
description: |

## 目的 (Purpose)
針對 AI 代理人優化的範本，用於實作具有充足上下文和自我驗證功能的功能，以透過迭代優化實現可運行的程式碼。

## 核心原則 (Core Principles)
1. **上下文至上 (Context is King)**：包含所有必要的說明文件、範例和注意事項。
2. **驗證迴圈 (Validation Loops)**：提供 AI 可以執行並修復的可執行測試/Lint 檢查。
3. **資訊密集 (Information Dense)**：使用程式碼庫中的關鍵字和模式。
4. **漸進式成功 (Progressive Success)**：從簡單開始，驗證，然後增強。
5. **全局規則 (Global rules)**：務必遵守 `CLAUDE.md` 中的所有規則。

---

## 目標 (Goal)
[需要構建什麼 - 請具體說明最終狀態和期望]

## 為什麼 (Why)
- [業務價值和使用者影響]
- [與現有功能的整合]
- [這解決了什麼問題以及為誰解決]

## 內容 (What)
[使用者可見的行為和技術需求]

### 成功準則 (Success Criteria)
- [ ] [具體可衡量的結果]

## 所有需要的上下文 (All Needed Context)

### 說明文件與參考資料 (列出實作該功能所需的所有上下文)
```yaml
# 必讀 - 將這些內容包含在您的上下文視窗中
- url: [官方 API 文件 URL]
  why: [您需要的特定章節/方法]
  
- file: [path/to/example.py]
  why: [要遵循的模式，要避免的陷阱]
  
- doc: [函式庫文件 URL] 
  section: [關於常見陷阱的特定章節]
  critical: [防止常見錯誤的關鍵見解]

- docfile: [PRPs/ai_docs/file.md]
  why: [使用者已貼上到專案中的文件]

```

### 目前程式碼庫樹狀圖 (在專案根目錄執行 `tree`) 以獲取程式碼庫概覽
```bash

```

### 期望的程式碼庫樹狀圖 (包含要新增的檔案及其職責)
```bash

```

### 程式碼庫已知陷阱與函式庫特殊行為
```python
# 重要：[函式庫名稱] 需要 [特定設定]
# 範例：FastAPI 的端點需要非同步 (async) 函式
# 範例：此 ORM 不支援超過 1000 條記錄的批次插入
# 範例：我們使用 pydantic v2 並且...
```

## 實作藍圖 (Implementation Blueprint)

### 資料模型與結構 (Data models and structure)

建立核心資料模型，確保型別安全和一致性。
```python
範例：
 - ORM 模型
 - Pydantic 模型
 - Pydantic 綱要 (Schemas)
 - Pydantic 驗證器 (Validators)

```

### 任務列表 (按完成順序列出完成 PRP 所需執行的任務)

```yaml
任務 1:
修改 src/existing_module.py:
  - 尋找模式： "class OldImplementation"
  - 在包含 "def __init__" 的行之後插入
  - 保留現有的方法簽名 (Signatures)

建立 src/new_feature.py:
  - 鏡像模式來自： src/similar_feature.py
  - 修改類別名稱和核心邏輯
  - 保持錯誤處理模式相同

...(...)

任務 N:
...

```


### 每個任務所需的虛擬碼 (視需要新增到每個任務中)
```python

# 任務 1
# 帶有關鍵細節的虛擬碼 (不需要寫出完整程式碼)
async def new_feature(param: str) -> Result:
    # 模式：務必先驗證輸入 (參見 src/validators.py)
    validated = validate_input(param)  # 引發 ValidationError
    
    # 注意事項：此函式庫需要連線池 (Connection Pooling)
    async with get_connection() as conn:  # 參見 src/db/pool.py
        # 模式：使用現有的重試裝飾器 (Retry Decorator)
        @retry(attempts=3, backoff=exponential)
        async def _inner():
            # 重要：如果每秒請求數 >10，API 會回傳 429
            await rate_limiter.acquire()
            return await external_api.call(validated)
        
        result = await _inner()
    
    # 模式：標準化回應格式
    return format_response(result)  # 參見 src/utils/responses.py
```

### 整合點 (Integration Points)
```yaml
資料庫：
  - 遷移： 「將 'feature_enabled' 欄位新增至 users 資料表」
  - 索引： "CREATE INDEX idx_feature_lookup ON users(feature_id)"
  
設定：
  - 新增至： config/settings.py
  - 模式： "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"
  
路由：
  - 新增至： src/api/routes.py  
  - 模式： "router.include_router(feature_router, prefix='/feature')"
```

## 驗證迴圈 (Validation Loop)

### 第一層：語法與風格
```bash
# 首先執行這些 —— 在繼續之前修復任何錯誤
ruff check src/new_feature.py --fix  # 自動修復可修復的內容
mypy src/new_feature.py              # 型別檢查

# 預期：無錯誤。如果有錯誤，請閱讀錯誤訊息並修復。
```

### 第二層：單元測試 (為每個新功能/檔案/函式使用現有的測試模式)
```python
# 使用以下測試案例建立 test_new_feature.py：
def test_happy_path():
    """基本功能運作正常"""
    result = new_feature("valid_input")
    assert result.status == "success"

def test_validation_error():
    """無效輸入會引發 ValidationError"""
    with pytest.raises(ValidationError):
        new_feature("")

def test_external_api_timeout():
    """優雅地處理逾時"""
    with mock.patch('external_api.call', side_effect=TimeoutError):
        result = new_feature("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

```bash
# 執行並迭代直到通過：
uv run pytest test_new_feature.py -v
# 如果失敗：閱讀錯誤，了解根本原因，修復程式碼，重新執行 (切勿為了通過而使用 Mock)
```

### 第三層：整合測試 (Integration Test)
```bash
# 啟動服務
uv run python -m src.main --dev

# 測試端點
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# 預期：{"status": "success", "data": {...}}
# 如果出錯：檢查 logs/app.log 中的日誌以獲取堆疊追蹤 (Stack Trace)
```

## 最終驗證檢查表 (Final validation Checklist)
- [ ] 所有測試通過：`uv run pytest tests/ -v`
- [ ] 無 Lint 錯誤：`uv run ruff check src/`
- [ ] 無型別錯誤：`uv run mypy src/`
- [ ] 手動測試成功：[特定的 curl/命令]
- [ ] 優雅地處理錯誤情況
- [ ] 日誌資訊豐富但不冗長
- [ ] 如果需要，已更新說明文件

---

## 應避免的反模式 (Anti-Patterns to Avoid)
- ❌ 當現有模式可行時，不要建立新模式
- ❌ 不要因為「它應該可以運作」而跳過驗證
- ❌ 不要忽略失敗的測試 —— 修復它們
- ❌ 不要在非同步 (Async) 上下文中使用同步 (Sync) 函式
- ❌ 不要硬編碼 (Hardcode) 應作為設定的數值
- ❌ 不要擷取 (Catch) 所有異常 —— 請保持具體
