# delicate_hall_24106

This is a repository for a web application developed with Django, built with [Crowdbotics](https://crowdbotics.com)

### Features

1. **Local Authentication** using email and password with [allauth](https://pypi.org/project/django-allauth/)
2. **Rest API** using [django rest framework](http://www.django-rest-framework.org/)
3. **Forgot Password**
4. Bootstrap4
5. Toast Notification
6. Inline content editor in homepage

# endpoints
 - queries
    - 'fieldname__relationalField'
    - 'fieldname__gte=' ,'__in=', '__startwith=', ...etc
    - 'fieldname=' 
    - you also can add '?earliest=true' or '&latest=true', for the objects with date_created field
The end points that are not documeted in swagger.

- /patients/billings/

  - **note**: patients will be renamed to manage_patients

  * you will need only **GET** **PUT**,
  * You wont need **DELTE** becuase this data will be immutable
  * You wont need **POST** because billes data will be created automaticly after a user request a servce.

- /alerts/ "convential I should name it notifcations"

  - **onmessage**
    ```
    
    ```
    
  - **send**
    ```
    {target:'events', id:1, is_seen:true}
    ```
    

- /statistics/

  - quick example "http://vytrac/statistics/?column__name=oxgyn&&field_value__lt=80"
    here you will get only the users with a history of oxygen level that reached under 80
  - quick example2 "http://vytrac/statistics/?column__name=oxgyn&&field_value__lt=80&date_created__gt=2021-06-09"
    now instead of getting all the users with a history of low oxygen, will get only the users that have currently or last measurement bellow 80
  - quick example3 "http://vytrac/statistics/?column__name=oxgyn&cal=min&number=10"
    you will get the 10 peaks of oxygen values
  - quick example4 "http://vytrac/statistics/?column__name=see_alerts&cal=duration"
   You will get how long the user spend before seeing each alert
    - Logic: calculate the time spent to change the value of the field `is_seen` from `false` to `true`
  
  
  - **GET** headers={}
    - the list view that look like the following as been sacrificed for the sake of aggregation and flexibility
    ```
    [{
    "name": "blood pressure",
    "user": 1,
    "column": [{
    "field_value": "22",
    "name": "ccc",
    "action": "added",
    "seen_by": [1],
    "date_created": "2021-06-09T10:42:41.458057Z"
    }, {
    "field_value": "44",
    "name": "ddd",
    "action": "added",
    "seen_by": [],
    "date_created": "2021-06-09T10:42:56.582589Z"
    }]
    }, {
    "name": "oxgyn",
    "user": 1,
    "column": [{
    "field_value": "11",
    "name": "",
    "action": "",
    "seen_by": [],
    "date_created": "2021-06-09T10:43:11.271641Z"
    }]
    }]
    ```
    - the aggrigaction friendly view 
    ```
    [{
    "field_value": "22",
    "name": "ccc",
    "action": "added",
    "seen_by": [1],
    "date_created": "2021-06-09T10:42:41.458057Z",
    "column": {
    "name": "blood pressure",
    "user": 1
    }
    }, {
    "field_value": "44",
    "name": "ddd",
    "action": "added",
    "seen_by": [],
    "date_created": "2021-06-09T10:42:56.582589Z",
    "column": {
    "name": "blood pressure",
    "user": 1
    }
    }, {
    "field_value": "11",
    "name": "",
    "action": "",
    "seen_by": [],
    "date_created": "2021-06-09T10:43:11.271641Z",
    "column": {
    "name": "oxgyn",
    "user": 1
    }
    }]
    ```
# Development

Following are instructions on setting up your development environment.

The recommended way for running the project locally and for development is using Docker.

It's possible to also run the project without Docker.

## Docker Setup (Recommended)

This project is set up to run using [Docker Compose](https://docs.docker.com/compose/) by default. It is the recommended way. You can also use existing Docker Compose files as basis for custom deployment, e.g. [Docker Swarm](https://docs.docker.com/engine/swarm/), [kubernetes](https://kubernetes.io/), etc.

1. Install Docker:
   - Linux - [get.docker.com](https://get.docker.com/)
   - Windows or MacOS - [Docker Desktop](https://www.docker.com/products/docker-desktop)
1. Clone this repo and `cd delicate_hall_24106`
1. Make sure `Pipfile.lock` exists. If it doesn't, generate it with:
   ```sh
   $ docker run -it --rm -v "$PWD":/django -w /django python:3.8 pip3 install --no-cache-dir -q pipenv && python3.8 -m pip install pipenv && python3.8 -m pipenv lock
   ```
   <!-- 1. Use `.env.example` to create `.env`:
      ```sh
      $ cp .env.example .env
      ``` -->
1. Update `.env` and `docker-compose.override.yml` replacing all `<placeholders>`
1. Start up the containers:

   ```sh
   $ docker-compose up
   ```

   This will build the necessary containers and start them, including the web server on the host and port you specified in `.env`.

   Current (project) directroy will be mapped with the container meaning any edits you make will be picked up by the container.

1. Seed the Postgres DB (in a separate terminal):
   ```sh
   $ docker-compose exec web python3 manage.py makemigrations
   $ docker-compose exec web python3 manage.py migrate
   ```
1. Create a superuser if required:
   ```sh
   $ docker-compose exec web python3 manage.py createsuperuser
   ```
   You will find an activation link in the server log output.

## Local Setup (Alternative to Docker)

1. [Postgresql](https://www.postgresql.org/download/)
2. [Python](https://www.python.org/downloads/release/python-365/)

### Installation

1. Install [pipenv](https://pypi.org/project/pipenv/)
2. Clone this repo and `cd delicate_hall_24106`
3. Run `pip install --user --upgrade pipenv` to get the latest pipenv version.
4. Run `pipenv --python 3.9`
5. Run `pipenv install`
6. Run `cp .env.example .env`
7. Update .env file `DATABASE_URL` with your `database_name`, `database_user`, `database_password`, if you use postgresql.
   Can alternatively set it to `sqlite:////tmp/my-tmp-sqlite.db`, if you want to use sqlite for local development.

### Getting Started.

1. Run `pipenv shell`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Run `python manage.py runserver`


### potential conflicts.
```
$ pipenv uninstall asgiref pyjwt djangochannelsrestframework asgi-redis channels-redis django djangorestframework djangorestframework-simplejwt
$ pipenv install asgiref pyjwt
$ pipenv install  djangochannelsrestframework asgi-redis channels-redis django djangorestframework djangorestframework-simplejwt
```