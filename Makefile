.PHONY: run-dev down clean build up build-api build-pipeline run test test_db create_trading_database

# Makefile for managing PostgreSQL users in Docker

POSTGRES_CONTAINER := postgres  # Adjust if your container name is different
POSTGRES_USER := airflow

create-superuser:
	docker compose exec -it $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -c "\
	CREATE USER postgres WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD 'billna1';"

drop-user:
	docker compose exec -it $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -c "DROP USER postgres;"

# Create a database trading data
create-db:
	docker compose exec -it $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -c "CREATE DATABASE trading_data;"

# Drop the trading data database
drop-db:
	docker compose exec -it $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -c "DROP DATABASE IF EXISTS trading_data;"

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

create_trading_database:
	docker compose exec -u postgres postgres psql postgres -c "CREATE DATABASE trading_data;"

build-base-image:
	docker build -t base-image-gold -f Dockerfile.base .

build-base-image-restart:
	make build-base-image
	make build-all
	make run