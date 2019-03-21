DOCKER_IMAGE = m2cgen

docker-test:
	docker run --rm -it -v "$$PWD":"/m2cgen" $(DOCKER_IMAGE)

docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-generate-examples:
	docker run --rm -it -v "$$PWD":"/m2cgen" $(DOCKER_IMAGE) bash -c "python setup.py develop && python tools/generate_code_examples.py generated_code_examples"
