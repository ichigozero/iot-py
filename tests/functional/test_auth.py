from flask import url_for


def test_fetch_login_page(client):
    response = client.get(url_for('auth.login'))

    assert response.status_code == 200
    assert b'Username' in response.data
    assert b'Password' in response.data
    assert b'Log In' in response.data
