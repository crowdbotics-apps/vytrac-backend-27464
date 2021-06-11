#FROM ubuntu:bionic
FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

RUN pip install pipenv
RUN mkdir /opt/webapp
WORKDIR /opt/webapp
COPY . .
#COPY /opt/webapp
RUN python3 -m pipenv install --skip-lock --deploy --system
RUN adduser --disabled-password --gecos "" django
USER django

ENV LANG C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
ARG SECRET_KEY


#RUN apt-get update && apt-get install -y --no-install-recommends \
#        tzdata \
#        python3-setuptools \
#        python3-pip \
#        python3-dev \
#        python3-venv \
#        git \
#        && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y --no-install-recommends \
#		libbluetooth-dev \
#		tk-dev \
#		uuid-dev \
#	&& rm -rf /var/lib/apt/lists/*
RUN python3 manage.py collectstatic --no-input




CMD waitress-serve --port=8000 delicate_hall_24106.wsgi:application
#CMD gunicorn cfehome.wsgi:application --bind 0.0.0.0:8000
#https://stackoverflow.com/questions/28668180/cant-install-pip-packages-inside-a-docker-container-with-ubuntu
#docker build --network=host -t image_name .
