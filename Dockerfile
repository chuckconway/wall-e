## Use an official lightweight Python image.
## https://hub.docker.com/_/python
#FROM python:3.12-slim-bookworm
#
## Set the working directory in the container to /app
#WORKDIR /app
#
## Copy the current directory contents into the container at /app
#COPY . /app
#
## Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
#
## Make port 80 available to the world outside this container
#EXPOSE 80
#
## Run app.py when the container launches
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

FROM python:3.12-slim-bookworm

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.2
  # ^^^
  # Make sure to update it!

# System deps:
RUN apt-get -y update; apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install $(test "$YOUR_ENV" == production && echo "--only=main") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

EXPOSE 8897

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8897"]