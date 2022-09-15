#!/bin/bash

set -e

if [[ $TEST == "API" ]]; then
  make flake8 isort-check test-api run-codecov generate-code-examples
fi

if [[ $TEST == "E2E" ]]; then
  python setup.py install
  rm -rfd m2cgen/
  pytest -v "-m=$LANG" "-k=not(xgboost_XGBClassifier and elixir and train_model_classification_binary2)" tests/e2e/
fi

if [[ $RELEASE == "true" ]]; then
  make package
fi
