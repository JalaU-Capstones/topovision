# ======================================================
# TopoVision Makefile — Development Automation
# Python 3.11 / Ubuntu / Fish-compatible
# ======================================================

# --- VARIABLES ---
PYTHON := python
SRC := src
VENV := .venv
PYTHONPATH := $(SRC)
ACTIVATE := source $(VENV)/bin/activate

# --- COMMAND SHORTCUTS ---
RUN = PYTHONPATH=$(SRC) $(PYTHON)
PIP = $(VENV)/bin/pip
BLACK = $(VENV)/bin/black
ISORT = $(VENV)/bin/isort
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
PYTEST = $(VENV)/bin/pytest
PRECOMMIT = $(VENV)/bin/pre-commit

# ======================================================
# 🧩 PROJECT COMMANDS
# ======================================================

.PHONY: help run lint typecheck test check clean install

help:
	@echo "🧭 Available commands:"
	@echo "  make run          - Run the TopoVision application"
	@echo "  make lint         - Format & lint code with Black, isort, and Flake8"
	@echo "  make typecheck    - Run MyPy static type checking"
	@echo "  make test         - Run tests using pytest"
	@echo "  make check        - Run all pre-commit checks (lint, mypy, etc.)"
	@echo "  make clean        - Remove cache, build, and temporary files"
	@echo "  make install      - Install dependencies into virtual environment"

# ======================================================
# 🏃 EXECUTION
# ======================================================

run:
	@echo "🚀 Running TopoVision..."
	$(RUN) -m topovision.app

# ======================================================
# 🧼 CODE QUALITY
# ======================================================

lint:
	@echo "✨ Running Black, isort, and Flake8..."
	$(BLACK) $(SRC)
	$(ISORT) $(SRC)
	$(FLAKE8) $(SRC)

typecheck:
	@echo "🔍 Running MyPy type checking..."
	$(MYPY) $(SRC)

# ======================================================
# 🧪 TESTING
# ======================================================

test:
	@echo "🧩 Running pytest..."
	$(PYTEST) -v --maxfail=1 --disable-warnings

check:
	@echo "🔎 Running pre-commit hooks on all files..."
	$(PRECOMMIT) run --all-files

# ======================================================
# ⚙️ ENVIRONMENT MANAGEMENT
# ======================================================

install:
	@echo "📦 Installing dependencies..."
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	$(PRECOMMIT) install

# ======================================================
# 🧹 CLEANUP
# ======================================================

clean:
	@echo "🧼 Cleaning up..."
	rm -rf __pycache__ */__pycache__ */*/__pycache__ .pytest_cache .mypy_cache .coverage .venv build dist *.egg-info
	find . -type f -name '*.pyc' -delete
