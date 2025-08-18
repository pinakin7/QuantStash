# backend/app/data/yahoo.py
from datetime import date

import pandas as pd
import yfinance as yf
from app.api.v1.data.base import MarketDataProvider


class YahooFinanceProvider(MarketDataProvider):
    """Yahoo Finance data provider using yfinance."""

    def get_price_history(self, ticker: str, start: date, end: date) -> pd.DataFrame:
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(start=start, end=end, auto_adjust=False)
        df.reset_index(inplace=True)
        df = df.rename(columns=str.lower)  # standardize column names
        return df[["date", "open", "high", "low", "close", "volume"]]

    def get_dividends(self, ticker: str, start: date, end: date) -> pd.DataFrame:
        ticker_obj = yf.Ticker(ticker)
        dividends = ticker_obj.dividends
        if dividends.empty:
            return pd.DataFrame(columns=["date", "dividend"])
        # Ensure start and end are strings in the correct format
        start_str = pd.to_datetime(start).strftime("%Y-%m-%d")
        end_str = pd.to_datetime(end).strftime("%Y-%m-%d")
        df = dividends.loc[start_str:end_str].reset_index()
        df.columns = ["date", "dividend"]
        return df
