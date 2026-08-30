.PHONY: freeze install dev migration-autogen-dev migrate-dev test test-model test-structure

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
	uvicorn main:app --reload
test:
	pytest -v --maxfail=0 -s
test-model:
	pytest -v --maxfail=0 -m model
test-structure:
	pytest -v --maxfail=0 -m structure


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
