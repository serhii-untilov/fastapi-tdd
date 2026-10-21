.PHONY: freeze install dev migration-autogen-dev migrate-dev test model-test structure-test unit-test schema-test

COMMENT ?="update"
REVISION ?= head

# Project maintenance

freeze:
	pip freeze > requirements.txt
install:
	pip install -r requirements.txt

# Development

db:
	docker compose up -d dev-db
up:
	docker compose up -d
dev: up
	uvicorn app.main:app --reload
test:
	pytest -v -s
model-test:
	pytest -v -m model
structure-test:
	pytest -v -m structure
unit-test:
	pytest -v -m unit
schema-test:
	pytest -v -m schema


# Alembic migrations

check: db
	alembic -n dev_db check
current: db
	alembic -n dev_db current
heads: db
	alembic -n dev_db heads
history: db
	alembic -n dev_db history
revision: db
	alembic -n dev_db revision -m $(COMMENT)
autogenerate: db
	alembic -n dev_db revision --autogenerate -m $(COMMENT)
upgrade: db
	alembic -n dev_db upgrade $(REVISION)
downgrade: db
	alembic -n dev_db downgrade -1
downgrade-base: db
	alembic -n dev_db downgrade base
