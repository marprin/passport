#!/bin/bash

if [ -z $1 ]; then
    echo "Please input paramters"
elif [ $1 = 'makemigrations' ]; then
    env $(cat .env | xargs) python3 manage.py makemigrations
elif [ $1 = 'runserver' ]; then
    env $(cat .env | xargs) python3 manage.py runserver
elif [ $1 = 'migrate' ]; then
    env $(cat .env | xargs) python3 manage.py migrate
elif [ $1 = 'shell' ]; then
    env $(cat .env | xargs) python3 manage.py shell
else
    echo "No command found"
fi