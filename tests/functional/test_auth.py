from flask import request, url_for
from flask_login import current_user


def test_fetch_login_page(client):
    response = client.get(url_for('auth.login'))

    assert response.status_code == 200
    elements = (b'Username', b'Password', b'Log In')
    for element in elements:
        assert element in response.data


def test_invalid_user_login(client, app_db):
    response = client.post(
        url_for('auth.login'),
        data=dict(username='foo', password='foo'),
        follow_redirects=True
    )
    assert b'Invalid username or password' in response.data


def test_user_login(login_client):
    response = login_client

    assert response.status_code == 200
    assert request.path == url_for('main.index')
    assert not current_user.is_anonymous
    elements = (b'Settings', b'Log Out')
    for element in elements:
        assert element in response.data


def test_user_logout(client, login_client):
    assert not current_user.is_anonymous

    response = client.get(url_for('auth.logout'), follow_redirects=True)

    assert response.status_code == 200
    assert request.path == url_for('auth.login')
    assert current_user.is_anonymous
