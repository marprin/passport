#!/bin/bash
coverage run --source='.' manage.py test --settings sso.settings.test $*
coverage html
coverage report -m