FROM ubuntu:bionic
ENV LANG C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
ARG SECRET_KEY


RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


#  && apt-get install -y python3.8 -dev python3-pip libpq-dev curl \
#  && apt-get clean all \

WORKDIR /opt/webapp
COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install pipenv
#RUN pipenv install --deploy --system
RUN pipenv install --skip-lock --system --dev
RUN python3 manage.py collectstatic --no-input

RUN adduser --disabled-password --gecos "" django
USER django

CMD waitress-serve --port=8000 delicate_hall_24106.wsgi:application
#CMD gunicorn cfehome.wsgi:application --bind 0.0.0.0:8000