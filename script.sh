#!/bin/bash

if [ -z $1 ]; then
    echo "Please input paramters"
else
    env $(cat .env | xargs) python3 manage.py $@
fi