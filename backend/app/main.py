from app.api.v1 import portfolio
from app.routers import market
from fastapi import FastAPI

app = FastAPI(
    title="Quant Portfolio Tracker",
    version="1.0.0"
)

app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["Portfolio"])

app.include_router(market.router)