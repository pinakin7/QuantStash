from app.schemas.portfolio import PortfolioCreate
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_portfolio(portfolio: PortfolioCreate) -> dict[str, object]:
    return {"message": "Portfolio created", "portfolio": portfolio}
