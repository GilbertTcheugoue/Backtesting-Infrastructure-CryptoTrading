from kafka import KafkaProducer, KafkaConsumer
import threading
import json
import logging
import psycopg2

logging.basicConfig(level=logging.INFO)
print("STARTING CONSUMER DATA PIPELINE")
KAFKA_BROKER_URL = "kafka:9092"

def connect_to_postgres_db():
    try:
        conn = psycopg2.connect(
            dbname="trading_data",
            user="postgres",
            password="password",
            host="postgres"
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return None

def create_db_if_not_exists():
    conn = connect_to_postgres_db()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS trading_data")
    conn.close()

def consume_messages():
    """
    Consume messages from the 'stock_data' topic in Kafka and insert them into a PostgreSQL database.

    Returns:
        None
    
    """
    try:
        consumer = KafkaConsumer(
            'stock_data',
            bootstrap_servers=['kafka:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logging.info("Kafka Consumer has started listening")

        # We now consume messages from Kafka and insert them into a PostgreSQL database
        conn = connect_to_postgres_db()
        cursor = conn.cursor()

        # check if connection is successful
        print(conn)

        for message in consumer:
            # Convert message.value to a JSON-formatted string with indentation for better readability
            formatted_message = json.dumps(message.value, indent=2, sort_keys=True)
            logging.info(f"Consumed message: {formatted_message}")
    except Exception as e:
        logging.error(f"Error in Kafka consumer: {e}")


def start_consumer():
    thread = threading.Thread(target=consume_messages)
    thread.daemon = True
    thread.start()

start_consumer()