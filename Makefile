.PHONY: freeze install dev

freeze:
	pip freeze > requirements.txt
install:
	pip install -r requirements.txt
dev:
	uvicorn main:app --reload
