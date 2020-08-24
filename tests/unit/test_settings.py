from app.models import (
    City,
    Subprefecture,
    Prefecture,
)
from app.settings.views import get_dropdown_choices


def test_get_choices_of_prefectures(client):
    expected = [
        {'value': 1, 'text': 'prefecture_1'},
        {'value': 2, 'text': 'prefecture_2'}
    ]
    output = get_dropdown_choices(Prefecture.query.filter_by(region_id=1))
    assert output == expected


def test_get_choices_of_subprefecture(client):
    expected = [
        {'value': 1, 'text': 'subprefecture_1'},
        {'value': 2, 'text': 'subprefecture_2'},
    ]
    output = get_dropdown_choices(
        Subprefecture.query.filter_by(prefecture_id=1))
    assert output == expected


def test_get_choices_of_city(client):
    expected = [
        {'value': 1, 'text': 'city_1'}
    ]
    output = get_dropdown_choices(City.query.filter_by(subprefecture_id=1))
    assert output == expected
