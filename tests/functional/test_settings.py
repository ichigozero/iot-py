from flask import url_for
from flask_login import current_user


def test_fetch_pytenki_settings_page(client, login_client):
    assert not current_user.is_anonymous

    response = client.get(url_for('settings.pytenki'))

    assert response.status_code == 200
    elements = (
        b'<option selected value="1">region</option>',
        b'<option selected value="1">prefecture_1</option>',
        b'<option selected value="1">city_1</option>',
        b'<option value="2">city_2</option>',
        b'<option selected value="1">pinpoint_1</option>',
        b'name="fetch_intvl" step="5" type="range" value="35"',
        b'name="blink_on_time" step="0.5" type="range" value="1.0"',
        b'name="blink_off_time" step="0.5" type="range" value="1.0"',
        b'name="fade_in_time" step="0.5" type="range" value="1.0"',
        b'name="fade_out_time" step="0.5" type="range" value="1.0"',
        b'<option selected value="2">',
        b'<option selected value="3">',
        b'<option selected value="4">',
    )
    for element in elements:
        assert element in response.data


def test_update_pytenki_settings_with_null_values(client, login_client):
    response = client.post(
        url_for('settings.pytenki'),
        data=dict(region='', prefecture='',
                  city='', pinpoint_loc='',
                  led_fine='', led_cloud='',
                  led_rain='', led_snow='',
                  tts_button=''),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'"form-control is-invalid" id="region"',
        b'"form-control is-invalid" id="prefecture"',
        b'"form-control is-invalid" id="city"',
        b'"form-control is-invalid" id="pinpoint_loc"',
        b'"form-control is-invalid" id="led_fine"',
        b'"form-control is-invalid" id="led_cloud"',
        b'"form-control is-invalid" id="led_rain"',
        b'"form-control is-invalid" id="led_snow"',
        b'"form-control is-invalid" id="tts_button"'
    )
    for element in elements:
        assert element in response.data


def test_update_pytenki_settings_with_duplicate_values(client, login_client):
    response = client.post(
        url_for('settings.pytenki'),
        data=dict(region='1', prefecture='1',
                  city='2', pinpoint_loc='2',
                  led_fine='4', led_cloud='4',
                  led_rain='4', led_snow='4',
                  tts_button='4'),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'"form-control is-invalid" id="led_cloud"',
        b'"form-control is-invalid" id="led_rain"',
        b'"form-control is-invalid" id="led_snow"',
        b'"form-control is-invalid" id="tts_button"'
    )
    for element in elements:
        assert element in response.data


def test_successful_pytenki_settings_update(mocker, client, login_client):
    import app

    spy_init_task = mocker.spy(app.pytenki_task, 'init_task')
    spy_restart = mocker.spy(app.pytenki_task, 'restart')

    response = client.post(
        url_for('settings.pytenki'),
        data=dict(region='1', prefecture='1',
                  city='2', pinpoint_loc='2',
                  led_fine='4', led_cloud='17',
                  led_rain='27', led_snow='22',
                  tts_button='2', fetch_intvl='20',
                  blink_on_time='3.0', blink_off_time='2.0',
                  fade_in_time='3.0', fade_out_time='2.0'),
        follow_redirects=True
    )

    spy_init_task.assert_called_once()
    spy_restart.assert_called_once()

    assert response.status_code == 200
    elements = (
        b'PyTenki Settings Have Been Updated Successfully',
        b'<option selected value="1">region</option>',
        b'<option selected value="1">prefecture_1</option>',
        b'<option value="1">city_1</option>',
        b'<option selected value="2">city_2</option>',
        b'<option selected value="2">pinpoint_2</option>',
        b'name="fetch_intvl" step="5" type="range" value="20"',
        b'name="blink_on_time" step="0.5" type="range" value="3.0"',
        b'name="blink_off_time" step="0.5" type="range" value="2.0"',
        b'name="fade_in_time" step="0.5" type="range" value="3.0"',
        b'name="fade_out_time" step="0.5" type="range" value="2.0"',
        b'<option selected value="4">',
        b'<option selected value="17">',
        b'<option selected value="27">',
        b'<option selected value="22">',
        b'<option selected value="2">'
    )
    for element in elements:
        assert element in response.data


def test_fetch_areas_by_region(client, login_client):
    response = client.post(
        url_for('settings.areas_by_region'),
        data=dict(region='1')
    )

    assert response.status_code == 200

    expected = {
        'prefectures': [
            {'value': '__None', 'text': ''},
            {'value': 1, 'text': 'prefecture_1'},
            {'value': 2, 'text': 'prefecture_2'}
        ],
        'cities': [
            {'value': '__None', 'text': ''},
            {'value': 1, 'text': 'city_1'},
            {'value': 2, 'text': 'city_2'}
        ],
        'pinpoints': [
            {'value': '__None', 'text': ''},
            {'value': 1, 'text': 'pinpoint_1'}
        ]
    }

    assert response.json['choices'] == expected


def test_fetch_areas_by_prefecture(client, login_client):
    response = client.post(
        url_for('settings.areas_by_prefecture'),
        data=dict(prefecture='1')
    )

    assert response.status_code == 200

    expected = {
        'cities': [
            {'value': '__None', 'text': ''},
            {'value': 1, 'text': 'city_1'},
            {'value': 2, 'text': 'city_2'}
        ],
        'pinpoints': [
            {'value': '__None', 'text': ''},
            {'value': 1, 'text': 'pinpoint_1'}
        ]
    }

    assert response.json['choices'] == expected


def test_fetch_areas_by_city(client, login_client):
    response = client.post(
        url_for('settings.areas_by_city'),
        data=dict(city='1')
    )

    assert response.status_code == 200

    expected = {
        'pinpoints': [
            {'value': '__None', 'text': ''},
            {'value': 1, 'text': 'pinpoint_1'}
        ]
    }

    assert response.json['choices'] == expected


def test_fetch_pydensha_settings_page(client, login_client):
    assert not current_user.is_anonymous

    response = client.get(url_for('settings.pydensha'))

    assert response.status_code == 200
    elements = (
        b'name="fetch_intvl" step="5" type="range" value="35"',
        b'<option selected value="16">',
        b'<option selected value="20">',
        b'<option selected value="21">'
    )
    for element in elements:
        assert element in response.data


def test_update_pydensha_settings_with_null_values(client, login_client):
    response = client.post(
        url_for('settings.pydensha'),
        data=dict(led_normal='', led_delayed='',
                  led_other=''),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'"form-control is-invalid" id="led_normal"',
        b'"form-control is-invalid" id="led_delayed"',
        b'"form-control is-invalid" id="led_other"',
    )
    for element in elements:
        assert element in response.data


def test_update_pydensha_settings_with_duplicate_values(client, login_client):
    response = client.post(
        url_for('settings.pydensha'),
        data=dict(led_normal='13', led_delayed='13',
                  led_other='13'),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'"form-control is-invalid" id="led_delayed"',
        b'"form-control is-invalid" id="led_other"',
    )
    for element in elements:
        assert element in response.data


def test_successful_pydensha_settings_update(mocker, client, login_client):
    response = client.post(
        url_for('settings.pydensha'),
        data=dict(led_normal='13', led_delayed='19',
                  led_other='26', fetch_intvl='10'),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'PyDensha Settings Have Been Updated Successfully',
        b'name="fetch_intvl" step="5" type="range" value="10"',
        b'<option selected value="13">',
        b'<option selected value="19">',
        b'<option selected value="26">'
    )
    for element in elements:
        assert element in response.data
