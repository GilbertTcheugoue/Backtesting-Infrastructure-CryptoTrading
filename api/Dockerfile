# 
FROM python:3.9

# 
WORKDIR /code

# 
ADD ./requirements.txt /code/requirements.txt

# Update the system and install entr application
RUN apt-get update && apt-get install -y entr

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
ADD ./app /code/app

# make the script start.sh executable
COPY ./watch_and_restart.sh /code/watch_and_restart.sh
RUN chmod +x ./watch_and_restart.sh

COPY ./start.sh /code/start.sh
RUN chmod +x ./start.sh
# 
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
# CMD ls app/*.py | entr -n -r ./start.sh

CMD ./watch_and_restart.sh