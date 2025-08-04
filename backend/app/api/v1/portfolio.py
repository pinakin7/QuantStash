from app.schemas.portfolio import PortfolioCreate
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_portfolio(portfolio: PortfolioCreate) -> dict[str, str | PortfolioCreate]:
    return {"message": "Portfolio created", "portfolio": portfolio}
