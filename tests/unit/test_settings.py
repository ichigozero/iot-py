from app.models import City, PinpointLocation, Prefecture
from app.settings.views import get_dropdown_choices


def test_get_choices_of_prefectures(client):
    expected = [
        {'value': '__None', 'text': ''},
        {'value': 1, 'text': 'prefecture_1'},
        {'value': 2, 'text': 'prefecture_2'}
    ]
    output = get_dropdown_choices(Prefecture.query.filter_by(region_id=1))
    assert output == expected


def test_get_choices_of_city(client):
    expected = [
        {'value': '__None', 'text': ''},
        {'value': 1, 'text': 'city_1'},
        {'value': 2, 'text': 'city_2'}
    ]
    output = get_dropdown_choices(City.query.filter_by(pref_id=1))
    assert output == expected


def test_get_choices_of_pinpoint_loc(client):
    expected = [
        {'value': '__None', 'text': ''},
        {'value': 1, 'text': 'pinpoint_1'}
    ]
    output = get_dropdown_choices(PinpointLocation.query.filter_by(city_id=1))
    assert output == expected
