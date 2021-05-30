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

The end points that are not documeted in swagger.

- /patients/billings/

  - **note**: patients will be renamed to manage_patients

  * you will need only **GET** **PUT**,
  * You wont need **DELTE** becuase this data will be immutable
  * You wont need **POST** because billes data will be created automaticly after a user request a servce.

- /alerts/ "convential I should name it notifcations"

  - **onmessage**
    {
    "message": [
    {
    "id": 1,
    "title": "ddd",
    "is_seen": false,
    "description": "changeddd",
    "deadline": null,
    "priority": "",
    "target_users": [],
    "target_groups": ['providers',]
    },
    {
    "id": 2,
    "title": "ddd",
    "is_seen": false,
    "description": "x",
    "deadline": null,
    "priority": "",
    "target_users": [],
    "target_groups": ['providers',]
    }
    ]
    }
  - **send**
    {id:1, is_seen:true}

- /statistics/

  - **note**: Usally, you don't need **POST** here because statstics autmaiclly created when you change the patient profiel data. for example if you change the blood prusser that will be registered in form of timesheet data.

  - quick example "statistics/?field_target=blood_pressure&object_id=9&time_frame=minute&target=field_value&cal=max/"
  - Example1 to get the change of somons blood pruser do this

    - First filter data like "?field_target=blood_pressure"
    - Then select the fields that you need "&fields=field_value,date_created"
    - Then select the patien or the object that you need to do statstics on "&object_id=9"
    - Then do this "&time_frame=minute&target=field_value&cal=avg"
      - cal = avg, min, max...
      - time_frame= minute/day/minuth/year

  - Example2 to get the change the number of patient thro over time 🚧

    - First filter data like "?field_target=patientprofile"
    - Then select the fields that you need "&fields=field_value,date_created"
    - then add "&count=patientprofile"

  - **GET** headers={}

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
   $ docker run -it --rm -v "$PWD":/django -w /django python:3.9 pip3 install --no-cache-dir -q pipenv && pipenv lock
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

### Getting Started

1. Run `pipenv shell`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Run `python manage.py runserver`
