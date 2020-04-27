def test_init_task(pytenki_task):
    SECONDS_IN_MIN = 60
    pytenki_task.init_task()
    assert pytenki_task.settings is not None
    assert pytenki_task.wait_time == 35 * SECONDS_IN_MIN


def test_get_fetched_data(pytenki_task):
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

    assert pytenki_task.get_fetched_data() == expected
