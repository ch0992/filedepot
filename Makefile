# Makefile (placeholder)

.PHONY: all test lint run

all:
	@echo "Available targets: test, lint, run, build, up, down"

test:
	pytest

lint:
	flake8 .

run:
	@echo "Use docker-compose or kubectl to run each service."

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down
