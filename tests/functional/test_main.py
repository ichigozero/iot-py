from flask import url_for


def test_fetch_index_page(client):
    response = client.get(url_for('main.index'))
    assert response.status_code == 200

    elements = (
        b'<span id="forecast-loc">(Tokyo/Minato-ku)</span>',
        b'<td id="today-weather">',
        b'Fine',
        b'<td id="hour-1">9</td>',
        b'<td id="hour-9">9</td>',
        b'<td id="weather-1"></td>',
        b'<td id="weather-9"></td>',
        b'<td id="temp-1"></td>',
        b'<td id="temp-9"></td>',
    )
    for element in elements:
        assert element in response.data
