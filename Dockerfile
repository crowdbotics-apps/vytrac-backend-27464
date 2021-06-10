FROM ubuntu:bionic

ENV LANG C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
ARG SECRET_KEY
RUN apt-get update \
  && apt-get install -y python3-dev python3-pip libpq-dev curl \
  && apt-get clean all \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/webapp
COPY . .
RUN pip3 install --no-cache-dir -q pipenv && pipenv install --deploy --system
RUN python3 manage.py collectstatic --no-input
RUN adduser --disabled-password --gecos "" django
USER django
CMD waitress-serve --port=8000 my_app_18674.wsgi:application

#1) docker run -it --rm -v "$PWD":/django -w /django python:3 pip3 install --no-cache-dir -q pipenv && pipenv lock
#2) docker-compose up