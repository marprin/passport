FROM python:3.7-alpine
LABEL MAINTAINER="Marprin Hennes Muchri <marprin93@gmail.com>"

RUN apk add --update build-base git libffi-dev openssl openssh postgresql-dev --update-cache --no-cache
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/logs/passport
RUN pip3 install pip --upgrade

WORKDIR /app/passport
ADD . /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir


CMD [ "python3 manage.py collectstatic --noinput" ]

ENTRYPOINT [ "gunicorn", "-b", ":8800", "-w", "4", "-k", "gevent", "-t", "120", "--graceful-timeout", "120", "config.wsgi:application" ]
