.PHONY: check lint test unit_test it_test e2e_test chalice-deploy

export PYTHONPATH=$PYTHONPATH:$(PWD)
export STAGE = dev

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	$(PWD)/venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

test: unit_test lint

lint: venv
	venv/bin/flake8 app.py tests chalicelib

unit_test: venv
	venv/bin/py.test -vvvv -r sxX tests/unit

chalice-deploy:
	chalice deploy --stage $(STAGE)
