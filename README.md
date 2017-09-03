# Quest

A web application for creating feature requests.

## Linting

    pipenv run flake8 app.py quest

## Testing

    pipenv run python -m pytest

## Running (development)

    pipenv run python app.py

## Running (production)

    pipenv run gunicorn app:app
