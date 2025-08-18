
from datetime import date

from app.models.dividend import DividendHistory
from app.models.price import PriceHistory
from app.repository.dividends import DividendRepository
from app.repository.price import PriceRepository
from app.services.yahoo import YahooService
from sqlalchemy.orm import Session


class DataManager:
    def __init__(self, db: Session):
        self.price_repo = PriceRepository(db)
        self.dividend_repo = DividendRepository(db)
        self.db = db

    def get_prices(self, ticker: str, start: date, end: date) -> list[PriceHistory]:
        cached = self.price_repo.get(ticker, start, end)
        if isinstance(cached, list) \
            and all(isinstance(item, PriceHistory) for item in cached) \
                and cached:
            return cached

        fresh = YahooService.fetch_prices(ticker, start, end)
        if not isinstance(fresh, list) or not all(isinstance(item, PriceHistory) for item in fresh):
            fresh = []
        self.price_repo.add_many(fresh)
        return fresh

    def get_dividends(self, ticker: str, start: date, end: date) -> list[DividendHistory]:
        cached = self.dividend_repo.get(ticker, start, end)
        if isinstance(cached, list) \
            and all(isinstance(item, DividendHistory) for item in cached) \
                and cached:
            return cached

        fresh = YahooService.fetch_dividends(ticker, start, end)
        if not isinstance(fresh, list) \
            or not all(isinstance(item, DividendHistory) for item in fresh):
            fresh = []
        self.dividend_repo.add_many(fresh)
        return fresh
