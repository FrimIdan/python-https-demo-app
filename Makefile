e_Y=\033[1;33m
C_C=\033[0;36m
C_M=\033[0;35m
C_R=\033[0;41m
C_N=\033[0m
SHELL=/bin/bash

# Project variables
BINARY_NAME ?= python-https-test
DOCKER_REGISTRY ?= idanfrim
VERSION ?= $(shell git rev-parse HEAD)
DOCKER_IMAGE ?= $(DOCKER_REGISTRY)/$(BINARY_NAME)
DOCKER_TAG ?= ${VERSION}

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help docker docker-push keys

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

.PHONY: docker
docker: ## Build Docker image
	@(echo "Building docker image ..." )
	@(docker build --file ./Dockerfile.client -t ${DOCKER_IMAGE}-client:${DOCKER_TAG} .)
	@(docker build --file ./Dockerfile.server -t ${DOCKER_IMAGE}-server:${DOCKER_TAG} .)

.PHONY: docker-push
docker-push: docker
	@echo "Publishing Docker image ..."
	@(docker push ${DOCKER_IMAGE}-client:${DOCKER_TAG})
	@(docker push ${DOCKER_IMAGE}-server:${DOCKER_TAG})

.PHONY: keys
keys:
	openssl req -x509 -nodes -newkey rsa:4096 -keyout /tmp/client.key -out /tmp/client.crt -days 365 -subj '/CN=python-https-server.default'
	openssl req -x509 -nodes -newkey rsa:4096 -keyout /tmp/server.key -out /tmp/server.crt -days 365 -subj '/CN=python-https-server.default'
