from flask import Blueprint
from tenkihaxjp import ForecastArea, ForecastSummary

from app import db
from app.models import (
    City,
    PinpointLocation,
    Prefecture,
    Region,
    Setting,
    User
)


bp = Blueprint('cli', __name__)


def clear_data():
    meta = db.metadata

    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())


def add_admin_user():
    print('Add admin user')

    user = User(username='admin')
    user.set_password('Computer1')

    db.session.add(user)


def add_forecast_areas():
    print('Add forecast areas')

    fcst_area = ForecastArea()
    fcst_area.fetch_parse_html_source()
    areas = fcst_area.get_all_main_areas()

    for region_name, prefectures in areas.items():
        region = Region(name=region_name)
        db.session.add(region)

        for prefecture_name, cities in prefectures.items():
            pref = Prefecture(name=prefecture_name, region=region)
            db.session.add(pref)

            for city_id, city_name in cities.items():
                city = City(id=city_id, name=city_name, prefecture=pref)
                db.session.add(city)

                fcst_summary = ForecastSummary()
                fcst_summary.fetch_weather_data(city_id)

                for location in fcst_summary.get_pinpoint_locations():
                    loc_id = location['link'].rsplit('/', 1)[-1]
                    loc_name = location['name']

                    pinpoint = PinpointLocation(id=loc_id, name=loc_name,
                                                city=city)
                    db.session.add(pinpoint)


def add_settings():
    print('Add default settings')

    set1 = Setting(app='pytenki')
    set2 = Setting(app='gpio')

    db.session.add_all([set1, set2])


@bp.cli.command('init_db')
def init_db():
    """Initialise DB"""
    clear_data()
    add_admin_user()
    add_settings()
    add_forecast_areas()
    db.session.commit()
