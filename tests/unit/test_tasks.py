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
    spy_summary = mocker.spy(pytenki_task.fcast_summary,
                             'fetch_weather_data')
    spy_details = mocker.spy(pytenki_task.fcast_details,
                             'fetch_parse_html_source')
    spy_leds = mocker.spy(pytenki_task.pytenki,
                          'operate_all_weather_leds')
    spy_button = mocker.spy(pytenki_task.pytenki,
                            'tts_forecast_summary_after_button_press')
    spy_sse = mocker.spy(sse, 'publish')

    pytenki_task.init_task()
    pytenki_task.start()

    expected = {
        'fcast': {
            'today': {
                'day': 'Today',
                'city': 'Tokyo',
                'weather': 'Fine',
                'temp': {'max': 1, 'min': 0}
            },
            'tomorrow': {
                'day': 'Tomorrow',
                'city': 'Tokyo',
                'weather': 'Fine',
                'temp': {'max': 1, 'min': 0}
            },
        },
        'fcast_24_hours': [
            {'time': '9', 'temp': '', 'weather': ''},
            {'time': '12', 'temp': '', 'weather': ''},
            {'time': '15', 'temp': '', 'weather': ''},
            {'time': '18', 'temp': '', 'weather': ''},
            {'time': '21', 'temp': '', 'weather': ''},
            {'time': '0', 'temp': '', 'weather': ''},
            {'time': '3', 'temp': '', 'weather': ''},
            {'time': '6', 'temp': '', 'weather': ''},
            {'time': '9', 'temp': '', 'weather': ''}
        ],
        'fcast_loc': '(Tokyo/Minato-ku)'
    }

    spy_summary.assert_called_once_with(1)
    spy_details.assert_called_once_with(1)
    spy_sse.assert_called_once_with(pytenki_task.get_fetched_data(),
                                    type='pytenki')
    spy_leds.assert_called_once_with(on_time=1.0, off_time=1.0,
                                     fade_in_time=1.0, fade_out_time=1.0)
    spy_button.assert_called_once()
    assert pytenki_task.get_fetched_data() == expected


def test_init_pydensha_task(pydensha_task):
    pydensha_task.init_task()
    assert pydensha_task.settings is not None
    assert pydensha_task.wait_time == 35 * SECONDS_IN_MIN


def test_get_fetched_pydensha_data(mocker, pydensha_task):
    spy_sse = mocker.spy(sse, 'publish')

    pydensha_task.init_task()
    pydensha_task.start()

    expected = {
        '1': {
            'kanji_name': 'Yamanote Line',
            'last_update': '2020-06-01 09:00',
            'line_status': 'Delayed',
        },
    }
    spy_sse.assert_called_once_with(pydensha_task.get_fetched_data(),
                                    type='pydensha')
    assert pydensha_task.get_fetched_data() == expected
