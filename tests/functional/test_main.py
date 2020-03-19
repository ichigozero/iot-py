from flask import url_for


def test_fetch_index_page(client):
    response = client.get(url_for('main.index'))
    assert response.status_code == 200
