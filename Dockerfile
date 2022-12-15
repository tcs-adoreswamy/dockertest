# Cache the build dependencies to reduce build time
FROM python:3.11-alpine as dependencies
LABEL image="reference-python-app-dependencies"
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Build app and remove all non-production dependencies
FROM python:3.11-alpine as build
LABEL image="reference-python-app-build"
WORKDIR /app
COPY --from=dependencies /app/dependencies/ /app/dependencies/
COPY src/ ./src/
#RUN <BUILD_COMMAND>

# Copy only files necessary and set envionment variables 
FROM containerstore/python:3.11
ARG APP_BUILDTIME=UNSET
ARG APP_NAME="reference-python-app"
ARG APP_VERSION=0.0.0-0-0000000
ENV APP_BUILDTIME=$APP_BUILDTIME \
    APP_NAME=$APP_NAME \
    APP_VERSION=$APP_VERSION
LABEL image=$APP_NAME
LABEL image.created=$APP_BUILDTIME
LABEL image.version=$APP_VERSION
WORKDIR /app
COPY --from=build --chown=app:app /app/build /app/build
COPY --from=build --chown=app:app /app/dependencies/ /app/dependencies/
COPY --chown=app:app config/ /app/config/

USER app:app

HEALTHCHECK --retries=8 CMD curl --silent --fail http://localhost:8080/about?dockerfile || exit 1