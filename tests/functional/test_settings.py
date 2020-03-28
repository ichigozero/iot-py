from flask import url_for
from flask_login import current_user


def test_fetch_pytenki_settings_page(client, login_client):
    assert not current_user.is_anonymous

    response = client.get(url_for('settings.pytenki'))

    assert response.status_code == 200
    assert b'<option selected value="2">' in response.data
    assert b'<option selected value="3">' in response.data
    assert b'<option selected value="4">' in response.data


def test_update_pytenki_settings(client, login_client):
    response = client.post(
        url_for('settings.pytenki'),
        data=dict(led_fine='4', led_cloud='17',
                  led_rain='27', led_snow='22',
                  tts_button='2'),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'PyTenki Settings Have Been Updated Successfully' in response.data
    assert b'<option selected value="4">' in response.data
    assert b'<option selected value="17">' in response.data
    assert b'<option selected value="27">' in response.data
    assert b'<option selected value="22">' in response.data
    assert b'<option selected value="2">' in response.data
