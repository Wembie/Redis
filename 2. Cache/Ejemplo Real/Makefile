#!/usr/bin/env make

install: composer

up:
	docker-compose up -d

down:
	docker-compose down


composer:
	docker-compose run --rm composer install --ignore-platform-reqs