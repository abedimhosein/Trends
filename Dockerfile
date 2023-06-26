# pull base image
FROM python:3.9.16-alpine3.17

# set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Exposing port (just for documenting)
EXPOSE 8001/tcp

# setting work directory
WORKDIR /app

# Adding utitlity packages to os of base image
RUN apk update && apk upgrade && apk add --no-cache \
    build-base linux-headers \
    postgresql postgresql-dev postgresql-libs \
    zlib \
    jpeg \
    gcc libc-dev libffi-dev libmagic gettext curl

# Install dependencies
RUN pip install --upgrade pip
COPY requirements/prod.txt requirements/prod.txt
RUN pip install -r requirements/prod.txt

# copy entire files of project
COPY . .