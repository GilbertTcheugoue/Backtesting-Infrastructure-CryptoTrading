from kafka import KafkaProducer
import json
import pandas as pd

# Kafka broker URL
KAFKA_BROKER_URL = "localhost:9092"  

# Create a KafkaProducer instance
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# define DataFrame 
data = {
    "Date": ["2023-06-20", "2023-06-21", "2023-06-22", "2023-06-23", "2023-06-26"],
    "Open": [15.99, 15.66, 14.30, 13.64, 13.87],
    "High": [16.889999, 15.755000, 14.440000, 14.140000, 14.420000],
    "Low": [15.58, 14.37, 13.86, 13.56, 13.83],
    "Close": [15.79, 14.64, 14.05, 14.03, 13.94],
    "Adj Close": [15.79, 14.64, 14.05, 14.03, 13.94],
    "Volume": [81335000, 97885000, 103461000, 74640600, 50679900]
}
df = pd.DataFrame(data)

def send_stock_data_to_kafka(df):
    """
    Sends stock data from DataFrame to Kafka topic 'stock_data'.
    
    Args:
        df (pd.DataFrame): DataFrame containing stock data.
    """
    for index, row in df.iterrows():
        # Convert each row to a dictionary
        data = {
            "Date": row["Date"],
            "Open": row["Open"],
            "High": row["High"],
            "Low": row["Low"],
            "Close": row["Close"],
            "Adj Close": row["Adj Close"],
            "Volume": row["Volume"]
        }
        
        # Send the data to Kafka
        producer.send('stock_data', value=data)
        producer.flush()  # Ensure all messages are sent

        print(f"Sent message to Kafka: {data}")

# Example usage
send_stock_data_to_kafka(df)
