from flask import url_for
from flask_login import current_user


def test_fetch_pytenki_settings_page(client, login_client):
    assert not current_user.is_anonymous
    response = client.get(url_for('settings.pytenki'))
    assert response.status_code == 200
