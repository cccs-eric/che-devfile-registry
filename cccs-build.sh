#!/bin/bash

VERSION=$(cat VERSION)

./build.sh --registry cranalyticalplatform.azurecr.io --organization cccs --tag ${VERSION} --offline
if [ $? -ne 0 ]; then
	echo "Failed to build docker image"
	exit 1
fi
docker push cranalyticalplatform.azurecr.io/cccs/che-devfile-registry:${VERSION}

