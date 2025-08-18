
from datetime import date

import pandas as pd
import yfinance as yf
from app.models.dividend import DividendHistory
from app.models.price import PriceHistory


class YahooService:
    @staticmethod
    def fetch_prices(ticker: str, start: date, end: date) -> list[PriceHistory]:
        df = yf.download(ticker, start=start, end=end)
        return [
            PriceHistory(
                ticker=ticker,
                date=index.date(),
                open=row["Open"],
                high=row["High"],
                low=row["Low"],
                close=row["Close"],
                volume=row["Volume"],
            )
            for index, row in df.iterrows()
        ]

    @staticmethod
    def fetch_dividends(ticker: str, start: date, end: date) -> list[DividendHistory]:
        t = yf.Ticker(ticker)
        # Convert start and end to string in ISO format for proper slicing
        # Convert start and end to pandas.Timestamp for proper slicing
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end)
        divs = t.dividends.loc[start_ts:end_ts]
        return [
            DividendHistory(
                ticker=ticker,
                date=index.date(),
                dividend=float(value),
            )
            for index, value in divs.items()
        ]
