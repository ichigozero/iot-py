from flask import url_for
from flask_login import current_user

import app


def test_fetch_pytenki_settings_page(client, login_client):
    assert not current_user.is_anonymous

    response = client.get(url_for('settings.pytenki'))

    assert response.status_code == 200
    elements = (
        b'<option selected value="1">region</option>',
        b'<option selected value="1">prefecture_1</option>',
        b'<option selected value="1">subprefecture_1</option>',
        b'<option value="2">subprefecture_2</option>',
        b'<option selected value="1">city_1</option>',
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
                  subprefecture='', city='',
                  led_fine='', led_cloud='',
                  led_rain='', led_snow='',
                  tts_button=''),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'"form-control is-invalid" id="region"',
        b'"form-control is-invalid" id="prefecture"',
        b'"form-control is-invalid" id="subprefecture"',
        b'"form-control is-invalid" id="city"',
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
                  subprefecture='2', city='2',
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
    spy_init_task = mocker.spy(app.pytenki_task, 'init_task')
    spy_restart = mocker.spy(app.pytenki_task, 'restart')

    response = client.post(
        url_for('settings.pytenki'),
        data=dict(region='1', prefecture='1',
                  subprefecture='2', city='2',
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
        b'<option value="1">subprefecture_1</option>',
        b'<option selected value="2">subprefecture_2</option>',
        b'<option selected value="2">city_2</option>',
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
            {'value': 1, 'text': 'prefecture_1'},
            {'value': 2, 'text': 'prefecture_2'}
        ],
        'subprefectures': [
            {'value': 1, 'text': 'subprefecture_1'},
            {'value': 2, 'text': 'subprefecture_2'}
        ],
        'cities': [
            {'value': 1, 'text': 'city_1'}
        ],
    }

    assert response.json['choices'] == expected


def test_fetch_areas_by_prefecture(client, login_client):
    response = client.post(
        url_for('settings.areas_by_prefecture'),
        data=dict(prefecture='1')
    )

    assert response.status_code == 200

    expected = {
        'subprefectures': [
            {'value': 1, 'text': 'subprefecture_1'},
            {'value': 2, 'text': 'subprefecture_2'}
        ],
        'cities': [
            {'value': 1, 'text': 'city_1'}
        ]
    }

    assert response.json['choices'] == expected


def test_fetch_areas_by_subprefecture(client, login_client):
    response = client.post(
        url_for('settings.areas_by_subprefecture'),
        data=dict(subprefecture='1')
    )

    assert response.status_code == 200

    expected = {
        'cities': [
            {'value': 1, 'text': 'city_1'}
        ]
    }

    assert response.json['choices'] == expected


def test_fetch_pydensha_settings_page(client, login_client):
    assert not current_user.is_anonymous

    response = client.get(url_for('settings.pydensha'))

    assert response.status_code == 200
    elements = (
        b'<option selected value="1">rail_category</option>',
        b'<option selected value="1">rail_region_1</option>',
        b'<option value="2">rail_region_2</option>',
        b'<option selected value="1">rail_company</option>',
        b'<option selected value="1">rail_line_1</option>',
        b'name="fetch_intvl" step="5" type="range" value="35"',
        b'name="blink_on_time" step="0.5" type="range" value="1.0"',
        b'name="blink_off_time" step="0.5" type="range" value="1.0"',
        b'<option selected value="16">',
        b'<option selected value="20">',
        b'<option selected value="21">'
    )
    for element in elements:
        assert element in response.data

    assert b'<option value="2">rail_line_2</option>' not in response.data


def test_update_pydensha_settings_with_null_values(client, login_client):
    response = client.post(
        url_for('settings.pydensha'),
        data=dict(category='', region='',
                  company='', line='',
                  led_red='', led_green='',
                  led_blue=''),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'"form-control is-invalid" id="category"',
        b'"form-control is-invalid" id="company"',
        b'"form-control is-invalid" id="region"',
        b'"form-control is-invalid" id="line"',
        b'"form-control is-invalid" id="led_red"',
        b'"form-control is-invalid" id="led_green"',
        b'"form-control is-invalid" id="led_blue"',
    )
    for element in elements:
        assert element in response.data


def test_update_pydensha_settings_with_duplicate_values(client, login_client):
    response = client.post(
        url_for('settings.pydensha'),
        data=dict(category='1', region='1',
                  company='1', line='1',
                  led_red='13', led_green='13',
                  led_blue='13'),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'"form-control is-invalid" id="led_green"',
        b'"form-control is-invalid" id="led_blue"',
    )
    for element in elements:
        assert element in response.data


def test_successful_pydensha_settings_update(mocker, client, login_client):
    spy_init_task = mocker.spy(app.pydensha_task, 'init_task')
    spy_restart = mocker.spy(app.pydensha_task, 'restart')

    response = client.post(
        url_for('settings.pydensha'),
        data=dict(category='1', company='1',
                  region='2', line='2',
                  led_red='13', led_green='19',
                  led_blue='26', fetch_intvl='10',
                  blink_on_time='3.0', blink_off_time='2.0'),
        follow_redirects=True
    )

    spy_init_task.assert_called_once()
    spy_restart.assert_called_once()

    assert response.status_code == 200
    elements = (
        b'PyDensha Settings Have Been Updated Successfully',
        b'<option selected value="1">rail_category</option>',
        b'<option value="1">rail_region_1</option>',
        b'<option selected value="2">rail_region_2</option>',
        b'<option selected value="1">rail_company</option>',
        b'<option selected value="2">rail_line_2</option>',
        b'name="fetch_intvl" step="5" type="range" value="10"',
        b'<option selected value="13">',
        b'<option selected value="19">',
        b'<option selected value="26">',
        b'name="blink_on_time" step="0.5" type="range" value="3.0"',
        b'name="blink_off_time" step="0.5" type="range" value="2.0"',
    )
    for element in elements:
        assert element in response.data

    assert b'<option value="1">rail_line_1</option>' not in response.data


def test_fetch_railway_infos_by_category(client, login_client):
    response = client.post(
        url_for('settings.railway_infos_by_category'),
        data=dict(category='1')
    )

    assert response.status_code == 200

    expected = {
        'regions': [
            {'value': 1, 'text': 'rail_region_1'},
            {'value': 2, 'text': 'rail_region_2'}
        ],
        'companies': [
            {'value': 1, 'text': 'rail_company'},
        ],
        'lines': [
            {'value': 1, 'text': 'rail_line_1'}
        ]
    }

    assert response.json['choices'] == expected


def test_fetch_railway_infos_by_category_region(client, login_client):
    response = client.post(
        url_for('settings.railway_infos_by_category_region'),
        data=dict(category='1', region='1')
    )

    assert response.status_code == 200

    expected = {
        'companies': [
            {'value': 1, 'text': 'rail_company'},
        ],
        'lines': [
            {'value': 1, 'text': 'rail_line_1'}
        ]
    }

    assert response.json['choices'] == expected


def test_fetch_railway_infos_by_category_region_company(client, login_client):
    response = client.post(
        url_for('settings.railway_infos_by_category_region_company'),
        data=dict(category='1', region='1', company='1')
    )

    assert response.status_code == 200

    expected = {
        'lines': [
            {'value': 1, 'text': 'rail_line_1'}
        ]
    }

    assert response.json['choices'] == expected
