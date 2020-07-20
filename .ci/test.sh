#!/bin/bash

set -e

cd $BUILD_DIRECTORY

if [[ $TEST == "API" ]]; then
  flake8 .
  pytest -v tests/ --cov=m2cgen/ --ignore=tests/e2e/
  if [[ $TRAVIS == "true" ]]; then
    coveralls
  fi
fi

if [[ $TEST == "E2E" ]]; then
  python setup.py install
  rm -rfd m2cgen/
  pytest -v "-m=$LANG" tests/e2e/
fi
