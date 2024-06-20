FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Update and install entr
RUN apk update && apk add entr

# Update pip
RUN pip install --upgrade pip

# Copy requirements.txt and install the required packages
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

# Copy your consumer script into the container
COPY ./kafka_consumer_db_inserter.py /app/

# Run the consumer script when the container starts
# CMD ["python", "kafka_consumer_db_inserter.py"]
CMD ls *.py | entr -n -r python kafka_consumer_db_inserter.py