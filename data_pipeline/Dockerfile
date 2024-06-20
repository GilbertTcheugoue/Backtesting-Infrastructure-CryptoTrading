FROM python:3.9-alpine

# Install Kafka and psycopg2 dependencies
RUN pip install kafka-python psycopg2-binary

# Copy your consumer script into the container
COPY ./kafka_consumer_db_inserter.py /app/

# Set the working directory
WORKDIR /app

# Run the consumer script when the container starts
CMD ["python", "kafka_consumer_db_inserter.py"]