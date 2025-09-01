import enum

from app.models.base import Base
from sqlalchemy import Column, Date, Enum, String


class AssetType(enum.Enum):
    STOCK = "stock"
    ETF = "etf"

class Asset(Base):
    __tablename__ = "assets"

    ticker = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    type = Column(Enum(AssetType), nullable=False)
    inception_date = Column(Date, nullable=True)
