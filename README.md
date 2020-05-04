# Passport

## Setup

Please install [mysql](https://www.mysql.com/) first before continue to next steps

Before install the requirements, you can choose to install directly, using virtualenv, or using [Docker](https://www.docker.com/)

### A. Setup Using Virtualenv

1. Install virtualenv by `pip3 install virtualenv`
2. Create virtualenv project by `virtualenv venv` (This will create venv folder in current directory)
3. Run the virtualenv by `source venv/bin/activate` (After this, you will see the (venv) in front of folder directory)
4. For next step, you can go to step B

### B. Setup the Requirements or Direct Install

Move to project directory and run

    pip3 install -r requirements.txt

### C. Setup with Docker

1. Install the docker engine
2. Install the docker compose
3. Run `docker-compose -f <docker-compose-version.yml> up` in the project directory

## How To Run The Code

To run the code, the steps are:

1. For steps A and B run `python manage.py runserver` then access `localhost:8000/`
2. For step C, directly access at `localhost:8800/`

## Important

If you change JavaScript file(s), you have to update the js by running this command based on how you setup the project

1. Setup using Docker

- get inside the docker container by `docker exec -ti <container name> bash`
- run `python manage.py collectstatic`

2. Setup using virtualenv

- run `python manage.py collectstatic`

## To Run a test

To run a test just type

    `./manage.py test app_name`

If you want to run whole test then just type

    `./manage.py test`

## Check Coverage

If you want to check code coverage just run

    `covarage run --source='.' manage.py test app_name(optional)`

and then to see the report just run

    `coverage report`
