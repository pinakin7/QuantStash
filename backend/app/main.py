from app.api.v1 import portfolio
from fastapi import FastAPI

app = FastAPI(
    title="Quant Portfolio Tracker",
    version="1.0.0"
)

app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["Portfolio"])
