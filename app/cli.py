from flask import Blueprint
from tenkihaxjp import ForecastArea, ForecastSummary
from traininfojp import RailList, RailSummary

from app import db
from app.models import (
    City,
    PinpointLocation,
    Prefecture,
    Railway,
    RailwayCategory,
    RailwayCompany,
    RailwayRegion,
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


def add_regular_railway_data():
    rail_list = RailList()
    rail_summary = RailSummary()

    rail_list.fetch_parse_html_source()
    summary_pages = rail_list.get_regular_train_summary_page_urls()

    category = RailwayCategory(name=rail_list.get_regular_train_title())

    for page in summary_pages:
        rail_summary.fetch_parse_html_source(page['url'])
        company_names = rail_summary.get_rail_company_names()

        region = RailwayRegion(name=page['title'])

        for company_name in company_names:
            company = (
                RailwayCompany.query.filter_by(name=company_name).first() or
                RailwayCompany(name=company_name)
            )
            company.regions.append(region)
            category.companies.append(company)

            lines = rail_summary.get_line_names_by_rail_company(company_name)

            for line in lines:
                url = rail_summary.get_line_details_page_url(line)
                railway = Railway(
                    name=line,
                    status_page_url=url,
                    category=category,
                    region=region
                )
                db.session.add(railway)
            db.session.add(company)
        db.session.add(region)
    db.session.add(category)


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
    add_regular_railway_data()
    db.session.commit()
