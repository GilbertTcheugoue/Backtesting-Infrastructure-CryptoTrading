from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models import Base, Fact_StockPrices, Dim_Assets, Dim_Date
import yfinance as yf
from datetime import datetime

# Database Connection Setup
DATABASE_URL = "postgresql://postgres:billna1@localhost:5432/trading_data"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


# Define the Top 5 Stock Companies
top_5_stocks = [
  {"ticker": "AAPL", "name": "Apple Inc.", "type": "Stock"},
  {"ticker": "MSFT", "name": "Microsoft Corporation", "type": "Stock"},
  {"ticker": "GOOGL", "name": "Alphabet Inc.", "type": "Stock"},
  {"ticker": "AMZN", "name": "Amazon.com, Inc.", "type": "Stock"},
  {"ticker": "Meta", "name": "Meta Platforms, Inc.", "type": "Stock"}
]

# Create or Update Assets in the Database
for stock in top_5_stocks:
  try:
    # Check if the asset already exists
    asset = session.query(Dim_Assets).filter_by(TickerSymbol=stock["ticker"]).one()
  except NoResultFound:
    # If not, create a new asset with AssetType
    asset = Dim_Assets(TickerSymbol=stock["ticker"], AssetName=stock["name"], AssetType=stock["type"])
    session.add(asset)
session.commit()  # Commit once after adding all new assets

# Fetch and Save Stock Data
for stock in top_5_stocks:
  ticker = stock["ticker"]
  stock_data = yf.Ticker(ticker)
  hist = stock_data.history(period="1d")
  
  # Get the AssetID
  asset = session.query(Dim_Assets).filter_by(TickerSymbol=ticker).one()
  asset_id = asset.AssetID
  
  for index, row in hist.iterrows():
    # Convert date to DateKey format
    date_key = int(index.strftime('%Y%m%d'))
    # Check if the date exists in Dim_Date, if not, create a new date entry
    date_entry = session.query(Dim_Date).filter_by(DateKey=date_key).first()
    if not date_entry:
      date_entry = Dim_Date(DateKey=date_key, Date=index.date(), Year=index.year, Quarter=index.quarter, Month=index.month, Day=index.day)
      session.add(date_entry)
      session.commit()
    
    # Convert NumPy types to native Python types using .item()
    stock_price = Fact_StockPrices(
      DateKey=date_key,
      AssetID=asset_id,
      Open=row['Open'].item(),
      High=row['High'].item(),
      Low=row['Low'].item(),
      Close=row['Close'].item()
    )
    session.add(stock_price)
  session.commit()

session.close()