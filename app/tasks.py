import functools
import re
import threading

import tenki_no_ko
import traininfojp
from flask_sse import sse
from pydensha import PyDensha
from pytenki import PyTenki

from app import db
from app.models import (
    City,
    Prefecture,
    RailwayCategory,
    RailwayLine,
    Region,
    Subprefecture,
    Setting,
)
from app.helper import get_dict_val


SECONDS_IN_MIN = 60


def wait_event(func):
    @functools.wraps(func)
    def wrapper(self, **kwargs):
        while True:
            func(self, **kwargs)
            if self.exit_thread.wait(
                    timeout=self.wait_time):
                break
    return wrapper


class BackgroundTask:
    def __init__(self):
        self.wait_time = 0
        self.task_thread = None
        self.exit_thread = threading.Event()

    def init_task(self):
        pass

    def _fetch_data(self):
        pass

    def get_fetched_data(self):
        pass

    def start(self):
        self.task_thread = threading.Thread(target=self._fetch_data)
        self.task_thread.start()

    def restart(self):
        self.exit_thread.set()
        self.exit_thread.clear()
        self.start()


class PyTenkiTask(BackgroundTask):
    def __init__(self):
        super().__init__()
        self.weather_scraper = tenki_no_ko.WeatherScraper()
        self.pytenki = PyTenki()
        self.settings = None
        self.location_codes = None

    def init_task(self):
        self.settings = Setting.load_setting('pytenki')
        city_id = get_dict_val(self.settings, ['fcst_area', 'city_id'])

        try:
            location = (
                db
                .session
                .query(Region, Prefecture, Subprefecture, City)
                .filter(
                    Region.id == Prefecture.region_id,
                    Prefecture.id == Subprefecture.prefecture_id,
                    Subprefecture.id == City.subprefecture_id,
                    City.id == city_id
                )
                .first()
            )
            self.location_codes = {
                'region_id': location.Region.code,
                'prefecture_id': location.Prefecture.code,
                'subprefecture_id': location.Subprefecture.code,
                'city_id': location.City.code,
            }
        except AttributeError:
            self.location_codes = None

        fetch_intvl = get_dict_val(self.settings, ['fetch_intvl']) or 35
        self.wait_time = fetch_intvl * SECONDS_IN_MIN

        self.pytenki._close_leds()
        self.pytenki._close_button()

        gpio = Setting.load_setting('gpio')
        led_pins = get_dict_val(gpio, ['weather', 'led'])
        self.pytenki.assign_leds(led_pins)

        button_pin = get_dict_val(gpio, ['weather', 'tts_button'])
        self.pytenki.assign_button(button_pin)

    @wait_event
    def _fetch_data(self):
        fetched_data = self.get_fetched_data()
        today_forecast = fetched_data.get('fcast').get('today')

        try:
            max_temp = (
                re
                .search(
                    r'([0-9]+)℃.*',
                    today_forecast.get('temps').get('high')
                )
                .group(1)
            )
            max_temp = '{}度'.format(max_temp)

            min_temp = (
                re
                .search(
                    r'([0-9]+)℃.*',
                    today_forecast.get('temps').get('low')
                )
                .group(1)
            )
            min_temp = '{}度'.format(min_temp)
        except AttributeError:
            max_temp = ''
            min_temp = ''

        self.pytenki.forecast = {
            'day': '今日',
            'city': fetched_data.get('fcast_loc'),
            'weather': today_forecast.get('weather'),
            'temp': {
                'max': max_temp,
                'min': min_temp
            },
        }
        self.pytenki.operate_all_weather_leds(
            on_time=get_dict_val(
                self.settings, ['led_duration', 'blink_on_time']),
            off_time=get_dict_val(
                self.settings, ['led_duration', 'blink_off_time']),
            fade_in_time=get_dict_val(
                self.settings, ['led_duration', 'fade_in_time']),
            fade_out_time=get_dict_val(
                self.settings, ['led_duration', 'fade_in_time'])
        )
        self.pytenki.tts_forecast_summary_after_button_press()

        from app import create_app

        app = create_app()
        with app.app_context():
            sse.publish(fetched_data, type='pytenki')

    def get_fetched_data(self):
        forecast_summary = (
            self.weather_scraper
            .extract_forecast_summary(self.location_codes)
        )

        return {
            'fcast': {
                'today': (
                    forecast_summary
                    .get('forecasts')
                    .get('today')
                ),
                'tomorrow': (
                    forecast_summary
                    .get('forecasts')
                    .get('tomorrow')
                ),
            },
            'fcast_24_hours': (
                self
                .weather_scraper
                .extract_3_hourly_forecasts_for_next_24_hours(
                    self.location_codes)
            ),
            'fcast_loc': forecast_summary.get('city')
        }


class PyDenshaTask(BackgroundTask):
    def __init__(self):
        super().__init__()
        self.rail_status_details = list()
        self.pydensha = PyDensha()
        self.rail_lines = None
        self.settings = None

    def init_task(self):
        self.settings = Setting.load_setting('pydensha')
        gpio = Setting.load_setting('gpio')

        fetch_intvl = get_dict_val(self.settings, ['fetch_intvl']) or 35
        self.wait_time = fetch_intvl * SECONDS_IN_MIN

        self.pydensha._close_led()

        led_pins = get_dict_val(gpio, ['train_info', 'led'])
        self.pydensha.assign_led(led_pins)

        line_ids = get_dict_val(self.settings, ['rail_info', 'line_ids'])
        self.rail_lines = (
            db.session
            .query(RailwayLine)
            .filter(RailwayLine.id.in_(line_ids))
            .all()
        )

        self.rail_status_details.clear()

        for line in self.rail_lines:
            self.rail_status_details.append(traininfojp.RailDetails())

    @wait_event
    def _fetch_data(self):
        train_infos = list()

        for idx, line in enumerate(self.rail_lines):
            self.rail_status_details[idx].fetch_parse_html_source(
                line.status_page_url)
            train_infos.append(
                self.rail_status_details[idx].get_line_status())

        self.pydensha.operate_led(
            train_infos=train_infos,
            on_time=get_dict_val(
                self.settings, ['led_duration', 'blink_on_time']),
            off_time=get_dict_val(
                self.settings, ['led_duration', 'blink_off_time'])
        )

        from app import create_app

        app = create_app()
        with app.app_context():
            sse.publish(self.get_fetched_data(), type='pydensha')

    def get_fetched_data(self):
        category_id = get_dict_val(self.settings, ['rail_info', 'category_id'])

        try:
            category_name = RailwayCategory.query.get(category_id).name
        except AttributeError:
            category_name = ''

        rail_info = dict()
        for idx, details in enumerate(self.rail_status_details, start=1):
            rail_info[str(idx)] = {
                'kanji_name':  details.get_line_kanji_name(),
                'last_update': details.get_last_updated_time(),
                'line_status': details.get_line_status(),
            }

        return {
            'rail_category': category_name,
            'rail_info': rail_info
        }
