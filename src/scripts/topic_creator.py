# scripts/topic_creator.py
import logging
import os
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient, NewTopic

# Load environment variables
load_dotenv()
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9094")

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

def create_topics(topics, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS):
    """Creates Kafka topics if they don't exist."""
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
    fs = admin_client.create_topics(new_topics, operation_timeout=10)  # Add timeout

    # Wait for each operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            logger.info(f"Topic '{topic}' created (or already exists)")
        except Exception as e:
            logger.error(f"Failed to create topic '{topic}': {e}")
            # Handle error as needed, maybe exit with a non-zero status code

if __name__ == "__main__":
    # List the topics you need to create
    topics = ['stock_data', 'user_registrations', 'backtest_results']  

    create_topics(topics)  # Create the topics

