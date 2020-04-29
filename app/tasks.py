import functools
import threading

import tenkihaxjp
from flask_sse import sse
from pytenki import PyTenki

from app.models import Setting
from app.helper import get_dict_val


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
        self.fcast_summary = tenkihaxjp.ForecastSummary()
        self.fcast_details = tenkihaxjp.ForecastDetails()
        self.pytenki = PyTenki()
        self.settings = None

    def init_task(self):
        SECONDS_IN_MIN = 60
        self.settings = Setting.load_setting('pytenki')
        gpio = Setting.load_setting('gpio')

        fetch_intvl = get_dict_val(self.settings, ['fetch_intvl']) or 35
        self.wait_time = fetch_intvl * SECONDS_IN_MIN

        self.pytenki._close_leds()
        self.pytenki._close_button()

        led_pins = get_dict_val(gpio, ['led'])
        self.pytenki.assign_leds(led_pins)

        button_pin = get_dict_val(gpio, ['tts_button'])
        self.pytenki.assign_button(button_pin)

    @wait_event
    def _fetch_data(self):
        city_id = get_dict_val(self.settings, ['fcst_area', 'city_id'])
        pinpoint_id = get_dict_val(self.settings,
                                   ['fcst_area', 'pinpoint_id'])

        self.fcast_summary.fetch_weather_data(city_id)
        self.fcast_details.fetch_parse_html_source(pinpoint_id)

        self.pytenki.forecast = self.fcast_summary.get_summary()
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
            sse.publish(self.get_fetched_data(), type='pytenki')

    def get_fetched_data(self):
        fcast_loc = '/'.join(
            filter(bool, (self.fcast_summary.get_city(),
                          self.fcast_details.get_pinpoint_loc_name()))
        )

        if fcast_loc:
            fcast_loc = '({})'.format(fcast_loc)

        return {
            'fcast': {
                'today': self.fcast_summary.get_summary(),
                'tomorrow': self.fcast_summary
                                .get_summary(tenkihaxjp.Period.TOMORROW),
            },
            'fcast_24_hours': self.fcast_details
                                  .get_3_hourly_forecasts_for_next_24_hours(),
            'fcast_loc': fcast_loc
        }