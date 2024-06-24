from confluent_kafka import Consumer, KafkaError
import json
import os
from dotenv import load_dotenv
import logging

import coloredlogs

coloredlogs.install()  # install a handler on the root logger

load_dotenv()
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9094")


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def create_kafka_consumer(topic_name, broker_url='localhost:9092', group_id_suffix='consumer'):
    """Creates and configures a Kafka Consumer with topic-specific group ID."""
    group_id = f"{topic_name}_{group_id_suffix}"  
    conf = {
        'bootstrap.servers': broker_url,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'  
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic_name])
    return consumer

def consume_messages(consumer):
    """Consumes messages from the Kafka topic and yields deserialized messages."""
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue  # No message available within timeout

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                continue
            else:
                print(f"Error while consuming message: {msg.error()}")
                continue  # Continue to next message

        yield json.loads(msg.value().decode('utf-8'))  # Deserialize the message


def create_and_consume_messages(topic_name, broker_url=KAFKA_BROKER_URL, group_id_suffix='consumer', timeout=1.0):
    """Creates a consumer, consumes messages, and processes them with a callback."""
    group_id = f"{topic_name}_{group_id_suffix}"
    conf = {
        'bootstrap.servers': broker_url,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'  # Start from beginning if no offset stored
    }

    try:
        consumer = Consumer(conf)
        consumer.subscribe([topic_name])

        logger.info(f"Consuming messages from topic '{topic_name}'")


        while True:
            msg = consumer.poll(timeout)

            if msg is None:
                continue  # No message available within timeout

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    logger.error(f"Error while consuming message: {msg.error()}")
                    continue  # Continue to next message

            message_value = json.loads(msg.value().decode('utf-8'))
            yield message_value  # Yield the deserialized message
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
