VENV = matrix
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MAIN = src/main.py

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build pygame ruff

run:
	$(PYTHON) $(MAIN)

format:
	$(PYTHON) -m ruff check --select I --fix src
	$(PYTHON) -m ruff format src

check:
	$(PYTHON) -m ruff check src
	$(PYTHON) -m ruff format --check src

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-venv:
	rm -rf $(VENV)

.PHONY: venv install run format check debug clean clean-venv
