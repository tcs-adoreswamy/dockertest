#!/usr/bin/env bash
#------------------------------------------------------------------------------
# NOTE: This code was generated by a build tool using repo
# (the-container-store/Java-Docker-Project-Template#master).
#
# Changes to this file may cause incorrect behavior and will be lost if
# the code is regenerated. Please use the documentation provided
# in http://the-container-store.github.io/Gradle-Releaser/ to see
# how to regenerate this file based on your project settings.
#------------------------------------------------------------------------------
APP_NAME="dockertest2"

IMAGE=$APP_NAME
echo " building ${IMAGE}"
cd ..
pwd
docker build --force-rm -t $IMAGE "."

docker run --rm -p 8080:8501 $IMAGE $1 $2