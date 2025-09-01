# scripts/fetch_demo.py
from datetime import date

from app.data.yahoo import YahooFinanceProvider

if __name__ == "__main__":
    provider = YahooFinanceProvider()
    prices = provider.get_price_history("AAPL", date(2020, 1, 1), date(2021, 1, 1))
    dividends = provider.get_dividends("AAPL", date(2020, 1, 1), date(2021, 1, 1))

    print("Price history sample:")
    print(prices.head())
    print("\nDividends sample:")
    print(dividends.head())
