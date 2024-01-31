.PHONY: start test

watch:
	uvicorn app.main:app --host 0.0.0.0 --port 8010 --env-file app/local.env --log-level info --reload


test:
	python -m pytest --import-mode importlib -vv
