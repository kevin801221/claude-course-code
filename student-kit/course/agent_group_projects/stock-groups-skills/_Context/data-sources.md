# 資料來源與指標公式(給 agent 看的對照表)

> 三位分析師都從這份對照表拿「去哪抓、欄位叫什麼、公式怎麼算」。
> 原則:能免 API key 的優先;抓不到就標「資料缺漏」,不要捏造。

## 1. yfinance(基本面 + 技術面,免 API key)

```python
import yfinance as yf
t = yf.Ticker("NVDA")

info      = t.info          # dict:估值、利潤率、殖利率…
hist      = t.history(period="1y", interval="1d")  # DataFrame:OHLCV
fin       = t.financials    # 損益表(年)
qfin      = t.quarterly_financials
bs        = t.balance_sheet
cf        = t.cashflow
news      = t.news          # list:近期新聞(無 key 的 fallback)
```

### 基本面常用欄位(`info` 內)
| 概念 | key | 備註 |
|---|---|---|
| P/E | `trailingPE` / `forwardPE` | 可能為 None |
| P/B | `priceToBook` | |
| P/S | `priceToSalesTrailing12Months` | |
| EV/EBITDA | `enterpriseToEbitda` | |
| 殖利率 | `dividendYield` | 已是小數,顯示時 ×100 |
| 毛利率 | `grossMargins` | 小數 |
| 營業利益率 | `operatingMargins` | |
| 淨利率 | `profitMargins` | |
| ROE | `returnOnEquity` | |
| ROA | `returnOnAssets` | |
| 負債權益比 | `debtToEquity` | |
| 流動比 | `currentRatio` | |
| 自由現金流 | `freeCashflow` | |

> ⚠️ `info` 任一欄位都可能是 `None`。一律 `x = info.get(key)`,None 就標「N/A(資料缺漏)」。

## 2. Finnhub(新聞,需要 FINNHUB_API_KEY,可選)

```python
import os, requests, datetime as dt
key = os.environ.get("FINNHUB_API_KEY")
to_   = dt.date.today()
from_ = to_ - dt.timedelta(days=21)
url = "https://finnhub.io/api/v1/company-news"
params = {"symbol": "NVDA", "from": str(from_), "to": str(to_), "token": key}
articles = requests.get(url, params=params, timeout=20).json()
# 每篇:{"headline","summary","datetime"(epoch),"url","source"}
```

沒有 key → 改用 `yf.Ticker(sym).news`(欄位較少,有 `title`/`link`/`providerPublishTime`)。

## 3. 技術指標公式(用 pandas 手算,不必裝 TA 套件)

```python
# 移動平均
df["MA20"]  = df["Close"].rolling(20).mean()
df["MA60"]  = df["Close"].rolling(60).mean()
df["MA200"] = df["Close"].rolling(200).mean()   # 樣本不足 200 天就標「樣本不足」

# RSI(14)
delta = df["Close"].diff()
gain  = delta.clip(lower=0).rolling(14).mean()
loss  = (-delta.clip(upper=0)).rolling(14).mean()
rs    = gain / loss
df["RSI14"] = 100 - 100 / (1 + rs)

# MACD(12,26,9)
ema12 = df["Close"].ewm(span=12, adjust=False).mean()
ema26 = df["Close"].ewm(span=26, adjust=False).mean()
df["MACD"]   = ema12 - ema26
df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

# 布林通道(20, 2σ)
mid = df["Close"].rolling(20).mean()
std = df["Close"].rolling(20).std()
df["BB_up"], df["BB_low"] = mid + 2*std, mid - 2*std
```

## 4. 輸出路徑慣例

每檔研究一個資料夾:`Projects/<ticker>-<YYYY-MM-DD>/`,內含
`fundamentals.md`、`technicals.md`、`technicals_chart.png`、`news.md`、`research-note.md`,
以及覆查用的 `*_raw.json`。

## 5. 共同免責

每份輸出開頭都帶一行:
> 本文為 Claude Code 教學範例,非投資建議。數字含抓取日期,可能與最新狀況有時間差。
