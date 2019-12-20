FROM python:3.7-alpine
LABEL AUTHOR="ELINGUI Pascal Uriel"

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user