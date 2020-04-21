import pytest
import simplejson as json
from flask import url_for

from app import create_app, db
from app.models import (
    City,
    PinpointLocation,
    Prefecture,
    Region,
    Setting,
    User
)
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

    region = Region(name='region')
    pref_1 = Prefecture(name='prefecture_1', region=region)
    pref_2 = Prefecture(name='prefecture_2', region=region)
    city_1 = City(id=1, name='city_1', prefecture=pref_1)
    city_2 = City(id=2, name='city_2', prefecture=pref_1)
    pinpoint_loc_1 = PinpointLocation(id=1, name='pinpoint_1', city=city_1)
    pinpoint_loc_2 = PinpointLocation(id=2, name='pinpoint_2', city=city_2)

    setting_1 = Setting(
        app='pytenki',
        value=json.dumps({
            'fcst_area': {
                'region_id': 1,
                'pref_id': 1,
                'city_id': 1,
                'pinpoint_id': 1
            },
            'fetch_intvl': 35,
            'led_duration': {
                'blink_on_time': 1.0,
                'blink_off_time': 1.0,
                'fade_in_time': 1.0,
                'fade_out_time': 1.0,
            },
        })
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
        region,
        pref_1,
        pref_2,
        city_1,
        city_2,
        pinpoint_loc_1,
        pinpoint_loc_2,
        setting_1,
        setting_2
    ])
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
