import pytest

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True


@pytest.fixture(scope='module')
def client():
    app = create_app(TestConfig)

    with app.app_context():
        app.test_request_context().push()
        yield app.test_client()
