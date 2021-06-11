FROM ubuntu:bionic

ENV LANG C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
ARG SECRET_KEY

RUN apt-get update \
  && apt-get install -y python3.7-dev python3-pip libpq-dev curl \
  && apt-get clean all \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/webapp
COPY . .
RUN pip3 install --no-cache-dir -q 'pipenv==2018.11.26' && pipenv install --deploy --system
RUN python3 manage.py collectstatic --no-input

RUN adduser --disabled-password --gecos "" django
USER django

CMD waitress-serve --port=$PORT vytrac_backend_27464.wsgi:application
