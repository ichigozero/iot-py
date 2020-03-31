import json

import pytest
from flask import url_for

from app import create_app, db
from app.models import User, Setting
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    HASH_ROUNDS = 1


@pytest.fixture(scope='module')
def client():
    app = create_app(TestConfig)

    with app.app_context():
        app.test_request_context().push()
        yield app.test_client()


@pytest.fixture(scope='function')
def login_client(client, app_db):
    with client:
        yield client.post(
            url_for('auth.login'),
            data=dict(username='foo', password='bar'),
            follow_redirects=True
        )


@pytest.fixture(scope='function')
def app_db():
    db.create_all()

    user = User(username='foo')
    user.set_password('bar')

    setting_1 = Setting(
        app='pytenki',
        value=json.dumps({})
    )
    setting_2 = Setting(
        app='gpio',
        value=json.dumps({
            'led': {'fine': '2', 'cloud': '3'},
            'tts_button': '4'
        })
    )

    db.session.add_all([
        user,
        setting_1,
        setting_2
    ])
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
