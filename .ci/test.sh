#!/bin/bash

set -e

if [[ $TEST == "API" ]]; then
  flake8 .
  isort . --check-only
  pytest -v tests/ --cov=m2cgen/ --cov-report=xml:coverage.xml --ignore=tests/e2e/
  curl -Os https://uploader.codecov.io/latest/linux/codecov
  chmod +x codecov
  ./codecov -f coverage.xml -Z
fi

if [[ $TEST == "E2E" ]]; then
  python setup.py install
  rm -rfd m2cgen/
  pytest -v "-m=$LANG" tests/e2e/
fi

if [[ $RELEASE == "true" ]]; then
  python setup.py bdist_wheel --plat-name=any --python-tag=py3
  python setup.py sdist
fi
