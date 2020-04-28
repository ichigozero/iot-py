def test_init_task(pytenki_task):
    SECONDS_IN_MIN = 60
    pytenki_task.init_task()
    assert pytenki_task.settings is not None
    assert pytenki_task.wait_time == 35 * SECONDS_IN_MIN


def test_get_fetched_data(mocker, pytenki_task):
    spy_summary = mocker.spy(pytenki_task.fcast_summary,
                             'fetch_weather_data')
    spy_details = mocker.spy(pytenki_task.fcast_details,
                             'fetch_parse_html_source')
    from flask_sse import sse
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
    assert pytenki_task.get_fetched_data() == expected
