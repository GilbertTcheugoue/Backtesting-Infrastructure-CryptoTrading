FROM base-image-gold:latest

# Set the working directory
WORKDIR /app

# update and install entr for file watching
# RUN apt-get update && apt-get install -y entr

# Update pip
# RUN pip install --upgrade pip

# Copy requirements.txt and install the required packages
# COPY ./requirements.txt /app/
# RUN pip install -r requirements.txt --no-cache-dir

# Copy your consumer script into the container
COPY ./kafka_consumer.py /app/

# Run the consumer script when the container starts
# CMD ["python", "kafka_consumer_db_inserter.py"]
CMD ["./scripts/wait-for-it.sh", "kafka:9092", "--", "ls", "*.py", "|", "entr", "-n", "-r", "python", "kafka_consumer.py"]
# CMD ls *.py | entr -n -r python kafka_consumer.py