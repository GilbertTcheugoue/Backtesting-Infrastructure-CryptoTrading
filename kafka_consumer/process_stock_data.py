from kafka import KafkaProducer, KafkaConsumer
import threading
import json
import logging
import psycopg2

logging.basicConfig(level=logging.INFO)
print("STARTING CONSUMER DATA PIPELINE")
KAFKA_BROKER_URL = "kafka:9092"

def process_stock_data():
    """
    Insert stock data to into a PostgreSQL database.

    Returns:
        None
    
    """
