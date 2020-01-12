DOCKER_IMAGE := m2cgen
DOCKER_RUN_ARGS := docker run --rm -it -v "$$PWD":"/m2cgen" $(DOCKER_IMAGE)


docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-test-all:
	$(DOCKER_RUN_ARGS)

docker-test-unit:
	$(DOCKER_RUN_ARGS) bash -c "pytest -v --fast tests/ --ignore=tests/e2e/"

docker-generate-examples:
	$(DOCKER_RUN_ARGS) bash -c "python3 setup.py develop && python3 tools/generate_code_examples.py generated_code_examples"

docker-flake8:
	$(DOCKER_RUN_ARGS) bash -c "flake8 ."

docker-shell:
	$(DOCKER_RUN_ARGS) bash

docker-pre-pr: docker-flake8 docker-test-all
