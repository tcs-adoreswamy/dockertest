# Cache the build dependencies to reduce build time
FROM python:3.9.15
EXPOSE 8501
LABEL image="reference-python-app-dependencies"
WORKDIR /Reference-Python-App
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/streamlit/streamlit-example.git .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]





# # Build app and remove all non-production dependencies
# FROM python:3.11-alpine as build
# LABEL image="reference-python-app-build"
# WORKDIR /app
# COPY --from=dependencies /app/dependencies/ /app/dependencies/
# COPY src/ ./src/
# #RUN <BUILD_COMMAND>

# # Copy only files necessary and set envionment variables 
# FROM containerstore/python:3.11
# ARG APP_BUILDTIME=UNSET
# ARG APP_NAME="reference-python-app"
# ARG APP_VERSION=0.0.0-0-0000000
# ENV APP_BUILDTIME=$APP_BUILDTIME \
#     APP_NAME=$APP_NAME \
#     APP_VERSION=$APP_VERSION
# LABEL image=$APP_NAME
# LABEL image.created=$APP_BUILDTIME
# LABEL image.version=$APP_VERSION
# WORKDIR /app
# COPY --from=build --chown=app:app /app/build /app/build
# COPY --from=build --chown=app:app /app/dependencies/ /app/dependencies/
# COPY --chown=app:app config/ /app/config/

# USER app:app

# HEALTHCHECK --retries=8 CMD curl --silent --fail http://localhost:8080/about?dockerfile || exit 1