
from datetime import date

from app.db.session import get_db
from app.models.dividend import DividendHistory
from app.models.price import PriceHistory
from app.services.data_manager import DataManager
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/prices/{ticker}", response_model=list[dict])
def get_prices(
    ticker: str,
    start: date = Query(..., description="Start date YYYY-MM-DD"),  # noqa: B008
    end: date = Query(..., description="End date YYYY-MM-DD"),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> list[dict]:
    manager = DataManager(db)
    prices: list[PriceHistory] = manager.get_prices(ticker, start, end)
    return [
        {
            "date": p.date,
            "open": p.open,
            "high": p.high,
            "low": p.low,
            "close": p.close,
            "volume": p.volume,
        }
        for p in prices
    ]


@router.get("/dividends/{ticker}", response_model=list[dict])
def get_dividends(
    ticker: str,
    start: date = Query(..., description="Start date YYYY-MM-DD"),  # noqa: B008
    end: date = Query(..., description="End date YYYY-MM-DD"),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> list[dict]:
    manager = DataManager(db)
    divs: list[DividendHistory] = manager.get_dividends(ticker, start, end)
    return [
        {
            "date": d.date,
            "dividend": d.dividend,
        }
        for d in divs
    ]
