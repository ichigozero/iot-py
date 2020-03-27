from flask import url_for
from flask_login import current_user

from app.models import Setting


def test_fetch_pytenki_settings_page(client, login_client):
    assert not current_user.is_anonymous
    response = client.get(url_for('settings.pytenki'))
    assert response.status_code == 200


def test_update_pytenki_settings(client, login_client):
    client.post(
        url_for('settings.pytenki'),
        data=dict(led_fine='4', led_cloud='17',
                  led_rain='27', led_snow='22',
                  tts_button='2'),
        follow_redirects=True
    )

    setting = Setting.load_setting('gpio')

    assert setting['led']['fine'] == '4'
    assert setting['led']['cloud'] == '17'
    assert setting['led']['rain'] == '27'
    assert setting['led']['snow'] == '22'
    assert setting['tts_button'] == '2'
