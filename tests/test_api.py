import json
from tempfile import NamedTemporaryFile

import pytest

from quest import db as _db
from quest.factory import create_app, register_blueprints


@pytest.fixture
def app(request):
    _app = create_app()
    register_blueprints(_app)

    with _app.app_context():
        yield _app


@pytest.fixture
def db(request, app):
    with NamedTemporaryFile(prefix="test", suffix=".db") as temp_db_file:
        temp_db_uri = "sqlite:///{}".format(temp_db_file.name)
        config = {
            "SQLALCHEMY_DATABASE_URI": temp_db_uri,
            "TESTING": True
        }

        app.config.update(config)
        _db.init_app(app)
        _db.create_all(app=app)

        yield _db


@pytest.fixture
def session(request, db):
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session(
        options={"bind": connection, "binds": {}})

    db.session = session
    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def client(request, app, session):
    with app.test_client() as client:
        yield client


def test_empty_db(client):
    response = client.get("/api/features")
    data = json.loads(response.get_data())
    assert data == {"features": []}
