
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
        self.db.bulk_save_objects(dividends)
        self.db.commit()
