from flask_sse import sse

SECONDS_IN_MIN = 60


def test_init_pytenki_task(mocker, pytenki_task):

    spy_assign_leds = mocker.spy(pytenki_task.pytenki, 'assign_leds')
    spy_assign_btn = mocker.spy(pytenki_task.pytenki, 'assign_button')

    pytenki_task.init_task()

    assert pytenki_task.settings is not None
    assert pytenki_task.wait_time == 35 * SECONDS_IN_MIN

    spy_assign_leds.assert_called_once_with({
        'fine': '2', 'cloud': '3',
        'rain': '5', 'snow': '6'
    })
    spy_assign_btn.assert_called_once_with('4')


def test_get_fetched_pytenki_data(mocker, pytenki_task):
    pytenki_task.location_codes = {
        'region_id': 1,
        'prefecture_id': 1,
        'subprefecture_id': 1,
        'city_id': 1
    }

    spy_forecast_summary = mocker.spy(
        pytenki_task.weather_scraper,
        'extract_forecast_summary'
    )
    spy_hourly_forecast = mocker.spy(
        pytenki_task.weather_scraper,
        'extract_3_hourly_forecasts_for_next_24_hours'
    )
    spy_leds = mocker.patch.object(
        pytenki_task.pytenki,
        'operate_all_weather_leds'
    )
    spy_button = mocker.patch.object(
        pytenki_task.pytenki,
        'tts_forecast_summary_after_button_press'
    )

    pytenki_task.init_task()
    pytenki_task.start()

    expected = {
        'fcast': {
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
        },
        'fcast_24_hours': [
            {'hour': '09', 'temp': '', 'weather': ''},
            {'hour': '12', 'temp': '', 'weather': ''},
            {'hour': '15', 'temp': '', 'weather': ''},
            {'hour': '18', 'temp': '', 'weather': ''},
            {'hour': '21', 'temp': '', 'weather': ''},
            {'hour': '24', 'temp': '', 'weather': ''},
            {'hour': '03', 'temp': '', 'weather': ''},
            {'hour': '06', 'temp': '', 'weather': ''},
        ],
        'fcast_loc': 'Minato-ku',
    }

    spy_forecast_summary.assert_called_once_with(pytenki_task.location_codes)
    spy_hourly_forecast.assert_called_once_with(pytenki_task.location_codes)
    spy_leds.assert_called_once_with(on_time=1.0, off_time=1.0,
                                     fade_in_time=1.0, fade_out_time=1.0)
    spy_button.assert_called_once()
    assert pytenki_task.get_fetched_data() == expected


def test_init_pydensha_task(mocker, pydensha_task):
    spy = mocker.spy(pydensha_task.pydensha, 'assign_led')

    pydensha_task.init_task()
    assert pydensha_task.settings is not None
    assert pydensha_task.wait_time == 35 * SECONDS_IN_MIN

    spy.assert_called_once_with({'red': '16', 'green': '20', 'blue': '21'})


def test_get_fetched_pydensha_data(mocker, pydensha_task):
    spy_led = mocker.spy(pydensha_task.pydensha, 'operate_led')

    pydensha_task.init_task()
    pydensha_task.start()

    expected = {
        'rail_category': 'rail_category',
        'rail_info': {
            '1': {
                'kanji_name': 'Yamanote Line',
                'last_update': '2020-06-01 09:00',
                'line_status': 'Delayed',
            },
        },
    }
    spy_led.assert_called_once_with(train_infos=['Delayed'], on_time=1.0,
                                    off_time=1.0)
    assert pydensha_task.get_fetched_data() == expected
