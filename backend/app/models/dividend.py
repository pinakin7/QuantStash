from app.models.base import Base
from sqlalchemy import BigInteger, Column, Date, Float, ForeignKey, String, UniqueConstraint


class DividendHistory(Base):
    __tablename__ = "dividend_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticker = Column(String, ForeignKey("assets.ticker"), index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)

    dividend = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("ticker", "date", name="uq_ticker_date_dividend"),)
