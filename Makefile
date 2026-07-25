.PHONY: test eval demo validate
test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v
eval:
	PYTHONPATH=src python3 evals/run.py
demo:
	PYTHONPATH=src python3 -m workstation.demo
validate:
	python3 scripts/validate_blueprint.py

