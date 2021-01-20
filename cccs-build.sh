#!/bin/bash

VERSION=$(cat VERSION)
#REGISTRY=cranalyticalplatform.azurecr.io
REGISTRY=uchimera.azurecr.io

./build.sh --registry ${REGISTRY} --organization cccs --tag ${VERSION} --offline
if [ $? -ne 0 ]; then
	echo "Failed to build docker image"
	exit 1
fi
docker push ${REGISTRY}/cccs/che-devfile-registry:${VERSION}

