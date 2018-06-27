.PHONY: test apidoc test-functions

help:	## Help to run
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:	## Build docker container
	docker build -t information-retrival .

dev:	## run docker container in dev mode
	docker run -it -p 5000:5000 -v $(shell pwd):/home/ubuntu information-retrival /bin/bash

push:	## push image to registry
	docker push registry.gitlab.com/datarisk/palantir/conda-cv

pull:	## pull image to registry
	docker pull registry.gitlab.com/datarisk/palantir/conda-cv
