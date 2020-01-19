#!/bin/bash

set -e

cd $TRAVIS_BUILD_DIR

if [[ $TEST == "API" ]]; then
  flake8 .
  pytest -v tests/ --cov=m2cgen/ --ignore=tests/e2e/
  coveralls
fi

if [[ $TEST == "E2E" ]]; then
  python setup.py install
  rm -rfd m2cgen/
  pytest -v --capture=no "-m=$LANG" tests/e2e/
fi
