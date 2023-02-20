# pull official base image
FROM python:3.9.16-alpine3.17

# set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# set environment variables
EXPOSE 8001

# set work directory
WORKDIR /app

# Adding mandatory packages to docker
RUN apk update && apk add --no-cache \
    postgresql \
    zlib \
    jpeg

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy entire files of project
COPY . .

RUN python manage.py collectstatic --no-input
RUN python manage.py makemigrations