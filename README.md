# Quest

[![Travis CI status](https://travis-ci.org/jdanford/quest.svg?branch=master)](https://travis-ci.org/jdanford/quest)

A web application for creating feature requests.

## Requirements

- Python 3.5+
- Pipenv
- PostgreSQL (optional, see below)
- A relatively modern web browser

By default, Quest connects to a local PostgreSQL database named `quest`, but it can be configured to use any SQL database through the `DATABASE_URL` environment variable. Similarly, the port that the web server uses can be configured through the `PORT` environment variable.

## Running locally

```sh
# assuming PostgreSQL
createdb quest

pipenv install
pipenv run python app.py
```

## Testing and linting

```sh
pipenv install --dev
pipenv run python -m pytest
pipenv run flake8 app.py quest
```

## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Attributions

- Compass icon from [Open Iconic](https://useiconic.com/open)
