DOCKER_IMAGE = m2cgen

docker-test:
	docker run --rm -it -v "$$PWD":"/m2cgen" $(DOCKER_IMAGE)

docker-build:
	docker build -t $(DOCKER_IMAGE) .

