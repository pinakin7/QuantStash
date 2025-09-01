
from datetime import date

from app.models.asset import Asset, AssetType
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

    def _ensure_asset_exists(self, ticker: str) -> None:
        """Ensure the asset exists in the database, create if it doesn't"""
        existing = self.db.query(Asset).filter(Asset.ticker == ticker).first()
        if not existing:
            # Create a basic asset record
            asset = Asset(
                ticker=ticker,
                name=f"{ticker} Stock",  # Generic name
                type=AssetType.STOCK,  # Assume stock by default
                inception_date=None
            )
            self.db.add(asset)
            self.db.commit()

    def get_prices(self, ticker: str, start: date, end: date) -> list[PriceHistory]:
        print(f"Getting prices for {ticker} from {start} to {end}")
        # Ensure asset exists before fetching prices
        self._ensure_asset_exists(ticker)
        print("Asset exists")
        cached = self.price_repo.get(ticker, start, end)
        print(f"Cached prices: {cached}")
        if isinstance(cached, list) \
            and all(isinstance(item, PriceHistory) for item in cached) \
                and cached:
            return cached

        fresh = YahooService.fetch_prices(ticker, start, end)
        if not isinstance(fresh, list) or not all(isinstance(item, PriceHistory) for item in fresh):
            fresh = []
        
        if fresh:
            self.price_repo.add_many(fresh)
        
        return fresh

    def get_dividends(self, ticker: str, start: date, end: date) -> list[DividendHistory]:
        # Ensure asset exists before fetching dividends
        self._ensure_asset_exists(ticker)
        
        cached = self.dividend_repo.get(ticker, start, end)
        if isinstance(cached, list) \
            and all(isinstance(item, DividendHistory) for item in cached) \
                and cached:
            return cached

        fresh = YahooService.fetch_dividends(ticker, start, end)
        if not isinstance(fresh, list) \
            or not all(isinstance(item, DividendHistory) for item in fresh):
            fresh = []
        
        if fresh:
            self.dividend_repo.add_many(fresh)
        
        return fresh
