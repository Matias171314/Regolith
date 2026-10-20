VENV = matrix
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MAIN = src/main.py

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build pygame

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-venv:
	rm -rf $(VENV)

.PHONY: venv install run debug clean clean-venv
