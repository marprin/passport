run:
	./manage.py runserver

test:
	./manage.py test --settings sso.settings.test

mmigrations:
	./manage.py makemigrations

migrate:
	./manage.py migrate

