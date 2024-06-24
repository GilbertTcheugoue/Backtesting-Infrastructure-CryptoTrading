.PHONY: run-dev down clean build up build-api build-pipeline run

build-all:
	docker compose build

run:
	make down
	make up

run-dev:
	fastapi dev api/main.py

build-api:
	docker compose build api
	make up

build-pipeline:
	docker compose build data-pipeline
	make up

up:
	docker compose up -d

down:
	docker compose down

test:
	pytest -v -s tests
	
clean:
	make down
	docker volume rm $(shell docker volume ls -qf dangling=true)
	docker rmi $(shell docker images -qf dangling=true)

test_db:
	@for i in `seq 1 5`; do \
		if (docker compose exec postgres sh -c 'psql -U postgres -c "select 1;"' 2>&1 > /dev/null) then break; \
		else echo "postgres initializing..."; sleep 5; fi \
	done
	docker compose exec postgres sh -c 'psql -U postgres -c "drop database if exists tests;" && psql -U postgres -c "create database tests;"'

