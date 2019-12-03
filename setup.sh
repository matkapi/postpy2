#!/bin/bash
set -ex
if ! [[ "$1" =~ ^(prod|)$ ]]; then
    echo "Parameter 1 must prod or empty for test"
    exit
fi
echo "removing old builds and dist ... "
rm -rf dist/* build/*
echo "building library ..."
python3 setup.py sdist bdist_wheel
if [[ "$1" = "" ]]; then
    echo "deploing on test.pypi.org ..."
    python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
fi

if [[ "$1" = "prod" ]]; then
    echo "deploing on pypi.org ..."
    python3 -m twine upload dist/*
fi