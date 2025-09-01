
from datetime import date

from app.models.dividend import DividendHistory
from sqlalchemy.orm import Session


class DividendRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ticker: str, start: date, end: date) -> list[DividendHistory]:
        results = (
            self.db.query(DividendHistory)
            .filter(
                DividendHistory.ticker == ticker,
                DividendHistory.date >= start,
                DividendHistory.date <= end,
            )
            .all()
        )
        # Ensure the result is a list of DividendHistory instances
        return [r for r in results if isinstance(r, DividendHistory)]

    def add_many(self, dividends: list[DividendHistory]) -> None:
        # Use add_all instead of bulk_save_objects to properly handle auto-incrementing IDs
        if not dividends:
            return
        
        self.db.add_all(dividends)
        self.db.commit()
        
        # Refresh all objects to get their generated IDs
        for dividend in dividends:
            self.db.refresh(dividend)
