from abc import ABC, abstractmethod
from datetime import date

import pandas as pd


class MarketDataProvider(ABC):
    """Abstract interface for any market data provider."""

    @abstractmethod
    def get_price_history(
        self, ticker: str, start: date, end: date
    ) -> pd.DataFrame:
        """Fetch historical price data (OHLCV)."""

    @abstractmethod
    def get_dividends(
        self, ticker: str, start: date, end: date
    ) -> pd.DataFrame:
        """Fetch dividend/distribution history."""
