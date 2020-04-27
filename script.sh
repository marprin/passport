#!/bin/bash

if [ -z $1 ]; then
    echo "Please input paramters"
elif [ $1 = 'create-migration' ]; then
    env $(cat .env | xargs) python3 manage.py makemigrations
fi