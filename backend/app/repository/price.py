
from datetime import date

from app.models.price import PriceHistory
from sqlalchemy.orm import Session


class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ticker: str, start: date, end: date) -> list[PriceHistory]:
        results = (
            self.db.query(PriceHistory)
            .filter(
                PriceHistory.ticker == ticker,
                PriceHistory.date >= start,
                PriceHistory.date <= end,
            )
            .all()
        )
        # Ensure the result is a list of PriceHistory instances
        return [r for r in results if isinstance(r, PriceHistory)]

    def add_many(self, prices: list[PriceHistory]) -> None:
        # Use add_all instead of bulk_save_objects to properly handle auto-incrementing IDs
        if not prices:
            return
        
        self.db.add_all(prices)
        self.db.commit()
        
        # Refresh all objects to get their generated IDs
        for price in prices:
            self.db.refresh(price)
