FROM python:2.7
MAINTAINER Marprin Hennes Muchri <marprin93@gmail.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt