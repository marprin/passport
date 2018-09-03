FROM python:3.6-alpine
MAINTAINER Marprin Hennes Muchri <marprin93@gmail.com>

RUN apk add --update build-base git libffi-dev openssl openssh postgresql-dev --update-cache --no-cache
ENV PYTHONUNBUFFERED 1

COPY ./requirements/base.txt /requirements/base.txt
RUN pip3 install pip --upgrade \
    && pip3 install -r requirements/base.txt --no-cache-dir

ADD . /app
WORKDIR /app
RUN mkdir -p /var/logs/passport

WORKDIR /app/passport

CMD python3 manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8800 -w $GUNICORN_WORKER -t 120 --graceful-timeout 120 config.wsgi:application
