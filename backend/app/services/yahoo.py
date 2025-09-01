
from datetime import date

import pandas as pd
import yfinance as yf
from app.models.dividend import DividendHistory
from app.models.price import PriceHistory


class YahooService:
    @staticmethod
    def fetch_prices(ticker: str, start: date, end: date) -> list[PriceHistory]:
        df = yf.download(ticker, start=start, end=end)
        
        # Handle empty dataframe
        if df.empty:
            return []
        
        prices = []
        for index, row in df.iterrows():
            try:
                # Extract values and ensure they are scalar
                open_val = row["Open"]
                high_val = row["High"]
                low_val = row["Low"]
                close_val = row["Close"]
                volume_val = row["Volume"]
                
                # Convert pandas objects to scalar values if needed
                if hasattr(open_val, 'item'):
                    open_val = open_val.item()
                if hasattr(high_val, 'item'):
                    high_val = high_val.item()
                if hasattr(low_val, 'item'):
                    low_val = low_val.item()
                if hasattr(close_val, 'item'):
                    close_val = close_val.item()
                if hasattr(volume_val, 'item'):
                    volume_val = volume_val.item()
                
                # Convert to appropriate types, handling NaN values
                open_float = float(open_val) if pd.notna(open_val) else None
                high_float = float(high_val) if pd.notna(high_val) else None
                low_float = float(low_val) if pd.notna(low_val) else None
                close_float = float(close_val) if pd.notna(close_val) else None
                volume_int = int(volume_val) if pd.notna(volume_val) else None
                
                price = PriceHistory(
                    ticker=ticker,
                    date=index.date(),
                    open=open_float,
                    high=high_float,
                    low=low_float,
                    close=close_float,
                    volume=volume_int,
                )
                prices.append(price)
            except Exception as e:
                # Log the error and skip this row
                print(f"Error processing price data for {ticker} on {index}: {e}")
                continue
        
        return prices

    @staticmethod
    def fetch_dividends(ticker: str, start: date, end: date) -> list[DividendHistory]:
        t = yf.Ticker(ticker)
        # Convert start and end to timezone-aware pandas.Timestamp for proper slicing
        start_ts = pd.Timestamp(start).tz_localize('UTC')
        end_ts = pd.Timestamp(end).tz_localize('UTC')
        divs = t.dividends.loc[start_ts:end_ts]
        
        # Handle empty series
        if divs.empty:
            return []
        
        dividends = []
        for index, value in divs.items():
            try:
                # Ensure we extract scalar values from pandas objects
                if hasattr(value, 'item'):
                    dividend_val = value.item()
                else:
                    dividend_val = value
                
                dividend = DividendHistory(
                    ticker=ticker,
                    date=index.date(),
                    dividend=float(dividend_val),
                )
                dividends.append(dividend)
            except Exception as e:
                # Log the error and skip this row
                print(f"Error processing dividend data for {ticker} on {index}: {e}")
                continue
        
        return dividends
