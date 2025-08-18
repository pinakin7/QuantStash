from app.models.asset import Asset, AssetType
from sqlalchemy.orm import Session


class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ticker: str) -> Asset | None:
        return self.db.query(Asset).filter(Asset.ticker == ticker).first()

    def add(self, ticker: str, name: str | None, type_: AssetType) -> Asset:
        asset = Asset(ticker=ticker, name=name, type=type_)
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset
