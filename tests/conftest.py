import pytest
import simplejson as json
from flask import url_for
from gpiozero.pins.mock import MockFactory
from gpiozero import Device

from app import create_app, db
from app.models import (
    City,
    Prefecture,
    RailwayCategory,
    RailwayCompany,
    RailwayInfo,
    RailwayLine,
    RailwayRegion,
    Region,
    Setting,
    Subprefecture,
    User
)
from app.tasks import PyDenshaTask, PyTenkiTask
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    HASH_ROUNDS = 1


@pytest.fixture
def app(mocker):
    class MockWeatherScraper:
        def extract_forecast_summary(self, location_ids):
            return {
                'city': 'Minato-ku',
                'update_datetime': '8/20',
                'forecasts': {
                    'today': {
                        'date': 'Today',
                        'weather': 'Fine',
                        'temps': {
                            'high': '12℃. [+1]',
                            'low': '11℃. [+1]',
                        }
                    },
                    'tomorrow': {
                        'date': 'Tomorrow',
                        'weather': 'Fine',
                        'temps': {
                            'high': '10℃. [+1]',
                            'low': '9℃. [+1]',
                        }
                    },
                }
            }

        def extract_3_hourly_forecasts_for_next_24_hours(self, location_ids):
            return [
                {'hour': '09',  'weather': '', 'temp': ''},
                {'hour': '12', 'weather': '', 'temp': ''},
                {'hour': '15', 'weather': '', 'temp': ''},
                {'hour': '18', 'weather': '', 'temp': ''},
                {'hour': '21', 'weather': '', 'temp': ''},
                {'hour': '24',  'weather': '', 'temp': ''},
                {'hour': '03',  'weather': '', 'temp': ''},
                {'hour': '06',  'weather': '', 'temp': ''},
            ]

    class MockRailDetails:
        def fetch_parse_html_source(self, page_url):
            pass

        def get_line_kanji_name(self):
            return 'Yamanote Line'

        def get_last_updated_time(self):
            return '2020-06-01 09:00'

        def get_line_status(self):
            return 'Delayed'

    mocker.patch('tenki_no_ko.WeatherScraper',
                 return_value=MockWeatherScraper())
    mocker.patch('traininfojp.RailDetails',
                 return_value=MockRailDetails())

    Device.pin_factory = MockFactory()

    app = create_app(TestConfig)

    with app.app_context():
        app.test_request_context().push()
        yield app


@pytest.fixture
def client(mocker, app, app_db):
    pytenki_task = PyTenkiTask()
    pydensha_task = PyDenshaTask()
    mocker.patch('app.tasks.PyTenkiTask',
                 return_value=pytenki_task)
    mocker.patch('app.tasks.PyDenshaTask',
                 return_value=pydensha_task)

    yield app.test_client()
    pytenki_task.exit_thread.set()
    pytenki_task.pytenki._close_button()
    pydensha_task.exit_thread.set()


@pytest.fixture
def login_client(client):
    with client:
        yield client.post(
            url_for('auth.login'),
            data=dict(username='foo', password='bar'),
            follow_redirects=True
        )


@pytest.fixture
def pytenki_task(app, app_db):
    pytenki_task = PyTenkiTask()
    yield pytenki_task
    pytenki_task.exit_thread.set()
    pytenki_task.pytenki._close_button()


@pytest.fixture
def pydensha_task(app, app_db):
    pydensha_task = PyDenshaTask()
    yield pydensha_task
    pydensha_task.exit_thread.set()


@pytest.fixture
def app_db():
    db.create_all()

    user = User(username='foo')
    user.set_password('bar')

    region = Region(name='region', code='1')
    prefecture_1 = Prefecture(name='prefecture_1', code='1', region=region)
    prefecture_2 = Prefecture(name='prefecture_2', code='2', region=region)
    subprefecture_1 = Subprefecture(
        name='subprefecture_1',
        code='1',
        prefecture=prefecture_1
    )
    subprefecture_2 = Subprefecture(
        name='subprefecture_2',
        code='2',
        prefecture=prefecture_1
    )
    city_1 = City(name='city_1', code='1', subprefecture=subprefecture_1)
    city_2 = City(name='city_2', code='2', subprefecture=subprefecture_2)

    railway_category = RailwayCategory(name='rail_category')
    railway_region_1 = RailwayRegion(name='rail_region_1')
    railway_region_2 = RailwayRegion(name='rail_region_2')
    railway_company = RailwayCompany(name='rail_company')
    railway_line_1 = RailwayLine(name='rail_line_1', status_page_url='url_1')
    railway_line_2 = RailwayLine(name='rail_line_2', status_page_url='url_2')
    railway_info_1 = RailwayInfo(
        category=railway_category,
        region=railway_region_1,
        company=railway_company,
        line=railway_line_1
    )
    railway_info_2 = RailwayInfo(
        category=railway_category,
        region=railway_region_2,
        company=railway_company,
        line=railway_line_2
    )

    setting_1 = Setting(
        app='pytenki',
        value=json.dumps({
            'fcst_area': {
                'region_id': 1,
                'pref_id': 1,
                'subpref_id': 1,
                'city_id': 1,
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
        app='pydensha',
        value=json.dumps({
            'rail_info': {
                'category_id': 1,
                'region_id': 1,
                'company_id': 1,
                'line_ids': [1]
            },
            'led_duration': {
                'blink_on_time': 1.0,
                'blink_off_time': 1.0,
            }
        })
    )
    setting_3 = Setting(
        app='gpio',
        value=json.dumps({
            'weather': {
                'led': {
                    'fine': '2',
                    'cloud': '3',
                    'rain': '5',
                    'snow': '6',
                },
                'tts_button': '4'
            },
            'train_info': {
                'led': {
                    'red': '16',
                    'green': '20',
                    'blue': '21'
                },
            }
        })
    )

    db.session.add_all([
        user,
        region,
        prefecture_1,
        prefecture_2,
        subprefecture_1,
        subprefecture_2,
        city_1,
        city_2,
        railway_category,
        railway_region_1,
        railway_region_2,
        railway_company,
        railway_line_1,
        railway_line_2,
        railway_info_1,
        railway_info_2,
        setting_1,
        setting_2,
        setting_3
    ])
    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()
