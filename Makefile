DOCKER_IMAGE := m2cgen
DOCKER_RUN_ARGS := docker run --rm -it -v "$$PWD":"/m2cgen" $(DOCKER_IMAGE)


docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-test-all:
	$(DOCKER_RUN_ARGS)

docker-test-unit:
	$(DOCKER_RUN_ARGS) bash -c "pytest -v --fast tests/ --ignore=tests/e2e/"

docker-generate-examples:
	$(DOCKER_RUN_ARGS) bash -c "python setup.py develop && python tools/generate_code_examples.py generated_code_examples"

docker-lint:
	$(DOCKER_RUN_ARGS) bash -c "flake8 . && isort . --check-only"

docker-shell:
	$(DOCKER_RUN_ARGS) bash

docker-pre-pr: docker-lint docker-test-all
