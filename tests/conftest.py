import pytest
import simplejson as json
from flask import url_for
from gpiozero.pins.mock import MockFactory
from gpiozero import Device

from app import create_app, db
from app.models import (
    City,
    PinpointLocation,
    Prefecture,
    Region,
    Setting,
    User
)
from app.tasks import PyTenkiTask
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    HASH_ROUNDS = 1


@pytest.fixture
def client(mocker):
    class MockForecastSummary:
        def fetch_weather_data(self, city_id):
            pass

        def get_city(self):
            return 'Tokyo'

        def get_summary(self, period=''):
            summary = {
                'day': 'Today',
                'city': self.get_city(),
                'weather': 'Fine',
                'temp': {'max': 1, 'min': 0}
            }

            if period:
                summary['day'] = 'Tomorrow'

            return summary

    class MockForecastDetails:
        def fetch_parse_html_source(self, pinpoint_id):
            pass

        def get_pinpoint_loc_name(self):
            return 'Minato-ku'

        def get_3_hourly_forecasts_for_next_24_hours(self):
            return [
                {'time': '9',  'temp': '', 'weather': ''},
                {'time': '12', 'temp': '', 'weather': ''},
                {'time': '15', 'temp': '', 'weather': ''},
                {'time': '18', 'temp': '', 'weather': ''},
                {'time': '21', 'temp': '', 'weather': ''},
                {'time': '0',  'temp': '', 'weather': ''},
                {'time': '3',  'temp': '', 'weather': ''},
                {'time': '6',  'temp': '', 'weather': ''},
                {'time': '9',  'temp': '', 'weather': ''}
            ]

    mocker.patch('tenkihaxjp.ForecastSummary',
                 return_value=MockForecastSummary())
    mocker.patch('tenkihaxjp.ForecastDetails',
                 return_value=MockForecastDetails())

    Device.pin_factory = MockFactory()

    pytenki_task = PyTenkiTask()
    mocker.patch('app.tasks.PyTenkiTask',
                 return_value=pytenki_task)

    app = create_app(TestConfig)

    with app.app_context():
        app.test_request_context().push()
        yield app.test_client()
        pytenki_task.exit_thread.set()
        pytenki_task.pytenki._close_button()


@pytest.fixture(scope='function')
def login_client(client, app_db):
    with client:
        yield client.post(
            url_for('auth.login'),
            data=dict(username='foo', password='bar'),
            follow_redirects=True
        )


@pytest.fixture(scope='function')
def pytenki_task(client, app_db):
    pytenki_task = PyTenkiTask()
    yield pytenki_task
    pytenki_task.exit_thread.set()
    pytenki_task.pytenki._close_button()


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
            'led': {
                'fine': '2',
                'cloud': '3',
                'rain': '5',
                'snow': '6'
            },
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
