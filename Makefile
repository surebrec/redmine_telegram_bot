SHELL := /bin/bash

restart: down build up
	echo "___Starting redmine bot___"

build:
	docker-compose -f infra/docker-compose.yml build --no-cache $(c)

up:
	docker-compose -f infra/docker-compose.yml up -d $(c)

down:
	docker-compose -f infra/docker-compose.yml down --rmi local $(c)

logs:
	docker-compose -f infra/docker-compose.yml logs $(c)