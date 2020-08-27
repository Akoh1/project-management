# pull official base image
FROM python:3.6.9-alpine

# set work directory
WORKDIR /home/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add  gcc python3-dev musl-dev \
    && apk add postgresql-dev
    # && pip install psycopg2 \
    # && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /home/app/requirements.txt
RUN pip install -r /home/app/requirements.txt

# copy entrypoint-prod.sh
COPY ./entrypoint.sh /home/app/entrypoint.sh

# copy project
COPY . /home/app/

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]

