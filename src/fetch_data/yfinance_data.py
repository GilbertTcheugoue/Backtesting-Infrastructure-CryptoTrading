import yfinance as yf
from confluent_kafka import Producer

def fetch_and_send_stock_data(symbol):
  # Fetch stock data
  stock = yf.Ticker(symbol)
  hist = stock.history(period="1d")  # For example, fetch today's data

  # Prepare data for sending to Kafka
  data = hist.iloc[0].to_dict()
  data['symbol'] = symbol  # Add the symbol to the data

  # Kafka configuration
  conf = {
    'bootstrap.servers': "localhost:9092"
  }  # Can be adjusted

  # Create Kafka producer
  producer = Producer(**conf)
  topic = 'stock_data'

  # Send data to Kafka
  producer.produce(topic, str(data).encode('utf-8'))
  producer.flush()

# Example usage
fetch_and_send_stock_data("AAPL")