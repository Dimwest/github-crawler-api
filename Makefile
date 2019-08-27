.PHONY: check lint test unit_test it_test e2e_test chalice-deploy

export PYTHONPATH=$PYTHONPATH:$(PWD)
export STAGE = dev

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	$(PWD)/venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

check: unit_test lint

lint: venv
	venv/bin/flake8 app.py tests chalicelib fargate

it_test: venv
	venv/bin/py.test -vvvv -r sxX tests/integration

e2e_test: venv
	venv/bin/py.test -vvvv -r sxX tests/e2e

unit_test: venv
	venv/bin/py.test -vvvv -r sxX tests/unit

test: venv unit_test it_test e2e_test

chalice-deploy:
	chalice deploy --stage $(STAGE)
