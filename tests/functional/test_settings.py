from flask import url_for
from flask_login import current_user


def test_fetch_pytenki_settings_page(client, login_client):
    assert not current_user.is_anonymous

    response = client.get(url_for('settings.pytenki'))

    assert response.status_code == 200
    elements = (
        b'<option value="1">region</option>',
        b'<option value="1">prefecture</option>',
        b'<option value="1">city_1</option>',
        b'<option value="2">city_2</option>',
        b'<option value="1">pinpoint_1</option>',
        b'<option value="2">pinpoint_2</option>',
        b'name="fetch_intvl" step="5" type="range" value="35"',
        b'<option selected value="2">',
        b'<option selected value="3">',
        b'<option selected value="4">',
    )
    for element in elements:
        assert element in response.data


def test_update_pytenki_settings_with_null_values(client, login_client):
    response = client.post(
        url_for('settings.pytenki'),
        data=dict(led_fine='', led_cloud='',
                  led_rain='', led_snow='',
                  tts_button=''),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
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


def test_successful_pytenki_settings_update(client, login_client):
    response = client.post(
        url_for('settings.pytenki'),
        data=dict(region='1', prefecture='1',
                  city='2', pinpoint_loc='2',
                  led_fine='4', led_cloud='17',
                  led_rain='27', led_snow='22',
                  tts_button='2', fetch_intvl='20'),
        follow_redirects=True
    )

    assert response.status_code == 200
    elements = (
        b'PyTenki Settings Have Been Updated Successfully',
        b'name="fetch_intvl" step="5" type="range" value="20"',
        b'<option selected value="4">',
        b'<option selected value="17">',
        b'<option selected value="27">',
        b'<option selected value="22">',
        b'<option selected value="2">'
    )
    for element in elements:
        assert element in response.data
