FROM python:3.9

# Set the working directory
WORKDIR /code

# Copy requirements file
ADD ./requirements.txt /code/requirements.txt

# update and install entr for file watching
RUN apt-get update && apt-get install -y entr

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app files
ADD ./app /code/app

# Copy the wait-for-it.sh script
ADD ./scripts/wait-for-it.sh /code/wait-for-it.sh

# Copy start_and_watch.sh script
# ADD ./start_and_watch.sh /code/start_and_watch.sh

# Make script executable
# RUN chmod +x ./start_and_watch.sh

# Use start_and_watch.sh to start the app and handle restarts on files changes
# CMD ["./start_and_watch.sh"]

CMD ["./wait-for-it.sh", "kafka:9092", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]