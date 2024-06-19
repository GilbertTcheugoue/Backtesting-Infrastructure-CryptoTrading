FROM python:3.9

WORKDIR /code

ADD ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y entr

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app and scripts directories
ADD ./app /code/app
ADD ./scripts /code/scripts

# Make scripts executable (within the scripts directory)
RUN chmod +x ./scripts/watch_and_restart.sh
RUN chmod +x ./scripts/start.sh

# Use watch_and_restart.sh to start the app and handle restarts
CMD ["./scripts/watch_and_restart.sh"]
