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
    _session = db.create_scoped_session(
        options={"bind": connection, "binds": {}})

    db.session = _session
    yield _session

    transaction.rollback()
    connection.close()
    _session.remove()


@pytest.fixture
def client(request, app, session):
    with app.test_client() as client:
        yield client


def test_empty_db(client):
    assert get(client, "/api/features") == {"features": []}


def test_add_feature(client):
    feature_data = {
        "title": "Good feature",
        "description": "It's really good",
        "client": "A",
        "priority": 1,
        "target_date": "2017-11-11",
        "product_area": "billing"
    }

    response_data = post(client, "/api/features", feature_data)
    assert set(response_data.keys()) == {"id"}

    feature_data["id"] = response_data["id"]
    assert get(client, "/api/features") == {"features": [feature_data]}


def test_delete_feature(client):
    feature_data = {
        "title": "Awesome feature",
        "description": "You won't believe it!",
        "client": "B",
        "priority": 1,
        "target_date": "2017-12-12",
        "product_area": "claims"
    }

    response_data = post(client, "/api/features", feature_data)
    assert set(response_data.keys()) == {"id"}

    feature_id = response_data["id"]
    delete_response = client.delete("/api/features/{}".format(feature_id))
    assert delete_response.status_code == 200

    assert get(client, "/api/features") == {"features": []}


def get(client, url):
    response = client.get(url)
    return get_response_json(response)


def post(client, url, data):
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    return get_response_json(response)


def get_response_json(response):
    return json.loads(response.get_data().decode("utf8"))
