from confluent_kafka import Producer, Consumer
import json
import socket  # For getting hostname
import os
from dotenv import load_dotenv

load_dotenv()
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9094")

# Kafka Configuration
def create_kafka_producer(broker_url=KAFKA_BROKER_URL, extra_config=None):
    """Creates and configures a Kafka Producer."""
    conf = {
        'bootstrap.servers': broker_url,
        'client.id': socket.gethostname(),
        'acks': 'all',
        'retries': 3,
        'batch.size': 16384,
        'linger.ms': 100,
    }
    if extra_config:
        conf.update(extra_config)  # Allow overriding default config
    return Producer(conf)

def send_message_to_kafka(producer, topic_name, message, key=None):
    """Sends a JSON-serialized message to the specified Kafka topic."""
    try:
        producer.produce(topic_name, key=key, value=json.dumps(message).encode('utf-8'))
        producer.flush()  # Ensure message delivery
    except Exception as e:
        print(f"Error producing message: {e}")

def create_kafka_consumer(broker_url=KAFKA_BROKER_URL, group_id="backtest_results_consumer_group", extra_config=None):
    """Creates and configures a Kafka Consumer."""
    conf = {
        'bootstrap.servers': broker_url,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }
    if extra_config:
        conf.update(extra_config)
    return Consumer(conf)

def consume_messages(consumer, topic_name):
    """Consumes messages from the specified Kafka topic and yields the message value as a dictionary."""
    consumer.subscribe([topic_name])
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            yield json.loads(msg.value())
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()