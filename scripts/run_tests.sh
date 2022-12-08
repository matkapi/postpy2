#!/bin/bash
cd "$(dirname "$0")/.."

# stop python from writing .pyc files
export PYTHONDONTWRITEBYTECODE=true


if [[ -f venv/bin/activate ]]; then
    . venv/bin/activate
fi
pip install -r requirements.txt
pip install -r requirements-dev.txt

python -m black .
vulture --min-confidence 80 ./postpy2
python -m pytest --cov=./postpy2 --cov-fail-under=80
