.PHONY: run-dev down clean build up

run:
	make down
	make up

run-dev:
	fastapi dev api/main.py

build:
	docker compose build
	make up

up:
	docker compose up -d

down:
	docker compose down

clean:
	make down
	docker volume rm $(shell docker volume ls -qf dangling=true)
	docker rmi $(shell docker images -qf dangling=true)