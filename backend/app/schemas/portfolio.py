from pydantic import BaseModel


class PortfolioCreate(BaseModel):
    name: str
    holdings: dict[str, float]  # ticker -> price
