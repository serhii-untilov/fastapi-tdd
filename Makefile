.PHONY: freeze install dev migration-autogen-dev migrate-dev test model-test structure-test unit-test schema-test

SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

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
	source venv/bin/activate && pytest -v -s --color=yes 2>&1 | tee logs/test.log
model-test:
	source venv/bin/activate && pytest -v -m model --color=yes 2>&1 | tee logs/test.log
structure-test:
	source venv/bin/activate && pytest -v -m structure --color=yes 2>&1 | tee logs/test.log
unit-test: venv
	source venv/bin/activate && pytest -v -m unit --color=yes 2>&1 | tee logs/test.log
schema-test:
	source venv/bin/activate && pytest -v -m schema --color=yes 2>&1 | tee logs/test.log

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

