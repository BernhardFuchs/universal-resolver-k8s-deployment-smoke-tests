FROM python:3.8.3-buster

LABEL "name"="Smoke tests for Deployment of the Universal Resolver to a Kubernetes Cluster"
LABEL "maintainer"="Bernhard <bernhard.fuchs@danubetech.com>"
LABEL "version"="1.0.0"

LABEL "com.github.actions.name"="GitHub Action for testing a deployment of the Universal Resolver"
LABEL "com.github.actions.description"="Tests a deployment of the Universal Resolver to a Kubernetes cluster."
LABEL "com.github.actions.icon"="package"
LABEL "com.github.actions.color"="red"

RUN apt-get update && \
    apt-get upgrade -y

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./smoke-test.py .

ENV HOST=""
ENV CONFIG_FILE=""

CMD [ "sh", "-c", "python ./smoke-test.py -h ${HOST} -c ${CONFIG_FILE}" ]