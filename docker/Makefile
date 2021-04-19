# NEEDS INTEGRATION INTO SERVERLESS AWS

# This Makefile automatically builds the docker container and pushes
# the resulting image to the specified server.
#
# To run from the package top-level:
#
# $ sudo make -C docker DOCKERHOST=[server:port] build push
#
# The above one-liner can be included in a CI/CD pipeline project.

ARCH                := $$(uname -m)
NAME                := $(DOCKERHOST)/colorkeys
HASHLONG            := $$(git log -1 --pretty=%H --no-merges)
HASHSHORT           := $$(git log -1 --pretty=%h --no-merges)
TAG                 := $$(git describe --tags --abbrev=0)
IMGLONG             := ${NAME}:${TAG}-${HASHSHORT}-${ARCH}
IMGSHORT            := ${NAME}:${TAG}-${ARCH}
DEFAULT             := ${NAME}:default-${ARCH}
ENGCOMMON_BRANCH    := $(ENGCOMMON_BRANCH)

.PHONY: all
all: build push

build:
    @docker build --no-cache -t ${IMGLONG} --build-arg GIT_COMMIT=${HASHSHORT} --build-arg ENGCOMMON_BRANCH=${ENGCOMMON_BRANCH} --build-arg DOCKERHOST=${DOCKERHOST} .
    @docker tag ${IMGLONG} ${IMGSHORT}

push:
    @docker push ${IMGLONG}
    @docker push ${IMGSHORT}

default:
    @docker tag ${IMGLONG} ${DEFAULT}
    @docker push ${DEFAULT}
