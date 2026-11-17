"""抓價量起手腳本 —— technicals-analyst 會在這基礎上擴充。

教學範例,非投資建議。

用法:
    uv run python scripts/fetch_prices.py NVDA
    uv run python scripts/fetch_prices.py NVDA --period 1y

行為:
    - 用 yfinance 抓日線(免 API key)
    - 算 MA20 / MA60 / MA200、RSI14
    - 存 CSV 到 Projects/<ticker>-<today>/prices.csv
    - 印出最近 5 天摘要

刻意保持精簡:真正的指標分析、畫圖、報告由 technicals-analyst 接手。
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import pandas as pd
import yfinance as yf


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA60"] = df["Close"].rolling(60).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df["RSI14"] = 100 - 100 / (1 + gain / loss)
    return df


def main() -> None:
    ap = argparse.ArgumentParser(description="抓個股日線並算基本技術指標(教學範例)")
    ap.add_argument("ticker", help="股票代號,例如 NVDA")
    ap.add_argument("--period", default="1y", help="yfinance period,預設 1y")
    args = ap.parse_args()

    ticker = args.ticker.upper()
    hist = yf.Ticker(ticker).history(period=args.period, interval="1d")
    if hist.empty:
        raise SystemExit(f"抓不到 {ticker} 的資料(ticker 拼對了嗎?)—— 標為資料缺漏,不要捏造。")

    hist = add_indicators(hist)

    today = dt.date.today().isoformat()
    out_dir = Path(__file__).resolve().parent.parent / "Projects" / f"{ticker}-{today}"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "prices.csv"
    hist.to_csv(csv_path)

    print(f"已抓 {ticker} 共 {len(hist)} 個交易日 → {csv_path}")
    cols = ["Close", "MA20", "MA60", "RSI14"]
    print(hist[cols].tail().round(2).to_string())
    print("\n提醒:這只是起手資料。完整技術面分析交給 technicals-analyst。教學範例,非投資建議。")


if __name__ == "__main__":
    main()
