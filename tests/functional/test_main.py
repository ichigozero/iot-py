from flask import url_for


def test_fetch_index_page(client):
    response = client.get(url_for('main.index'))
    assert response.status_code == 200

    elements = (
        b'<span id="forecast-loc"> [Minato-ku]</span>',
        b'<td id="today-weather">',
        b'Fine',
        b'<td id="hour-1">09</td>',
        b'<td id="hour-8">06</td>',
        b'<td id="weather-1"></td>',
        b'<td id="weather-8"></td>',
        b'<td id="temp-1"></td>',
        b'<td id="temp-8"></td>',
        b'<span id="rail-category"> [rail_category]</span>',
        b'<td id="rail-line-1">',
        b'Yamanote Line',
        b'<td id="rail-status-1">',
        b'Delayed',
        b'<td id="rail-status-timestamp-1">',
        b'2020-06-01 09:00'
    )
    for element in elements:
        assert element in response.data
