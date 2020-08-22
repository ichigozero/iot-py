from flask import Blueprint
from tenki_no_ko import LocationScraper
from traininfojp import RailList, RailSummary

from app import db
from app.models import (
    City,
    Prefecture,
    RailwayCategory,
    RailwayCompany,
    RailwayInfo,
    RailwayLine,
    RailwayRegion,
    Region,
    Setting,
    Subprefecture,
    User
)

JP_REGION_ALL = '日本全国'
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

    scraper = LocationScraper()
    regions = scraper.extract_regions()

    for region_code, region_name in regions.items():
        region = Region(code=region_code, name=region_name)
        db.session.add(region)

        prefectures = scraper.extract_prefectures(region_code)

        for prefecture_code, prefecture_name in prefectures.items():
            prefecture = Prefecture(
                code=prefecture_code,
                name=prefecture_name,
                region=region
            )
            db.session.add(prefecture)

            subprefectures_cities = scraper.extract_subprefectures_and_cities(
                region_id=region_code,
                prefecture_id=prefecture_code
            )

            for subprefecture_name, city_codes in (
                    subprefectures_cities.items()):
                subprefecture = None
                for city_code, city_info in city_codes.items():
                    if subprefecture is None:
                        subprefecture = Subprefecture(
                            code=city_info['subprefecture_id'],
                            name=subprefecture_name,
                            prefecture=prefecture
                        )
                        db.session.add(subprefecture)

                    city = City(
                        code=city_code,
                        name=city_info['city_name'],
                        subprefecture=subprefecture
                    )
                    db.session.add(city)


def add_regular_railway_data():
    print('Add regular railway data')

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

            lines = rail_summary.get_line_names_by_rail_company(company_name)

            for line in lines:
                url = rail_summary.get_line_details_page_url(line)
                line = RailwayLine(
                    name=line,
                    status_page_url=url
                )
                association = RailwayInfo(category=category, region=region,
                                          company=company, line=line)
                db.session.add(association)
                db.session.add(line)
            db.session.add(company)
        db.session.add(region)
    db.session.add(category)


def add_rapid_railway_data():
    print('Add rapid railway data')

    rail_list = RailList()
    rail_summary = RailSummary()

    rail_list.fetch_parse_html_source()
    summary_pages = rail_list.get_rapid_train_summary_page_urls()

    category = RailwayCategory(name=rail_list.get_rapid_train_title())
    region = (
        RailwayRegion.query.filter_by(name=JP_REGION_ALL).first() or
        RailwayRegion(name=JP_REGION_ALL)
    )

    page = summary_pages[0]
    rail_summary.fetch_parse_html_source(page['url'])
    company_names = rail_summary.get_rail_company_names()

    for company_name in company_names:
        company = (
            RailwayCompany.query.filter_by(name=company_name).first() or
            RailwayCompany(name=company_name)
        )

        lines = rail_summary.get_line_names_by_rail_company(company_name)

        for line in lines:
            url = rail_summary.get_line_details_page_url(line)
            line = RailwayLine(
                name=line,
                status_page_url=url
            )
            association = RailwayInfo(category=category, region=region,
                                      company=company, line=line)
            db.session.add(association)
            db.session.add(line)
        db.session.add(company)
    db.session.add(region)
    db.session.add(category)


def add_bullet_railway_data():
    print('Add bullet railway data')

    rail_list = RailList()
    rail_list.fetch_parse_html_source()
    details_page = rail_list.get_bullet_train_details_page_urls()

    category = RailwayCategory(name=rail_list.get_bullet_train_title())
    region = (
        RailwayRegion.query.filter_by(name=JP_REGION_ALL).first() or
        RailwayRegion(name=JP_REGION_ALL)
    )
    company = RailwayCompany(name='JRグループ各社')

    for page in details_page:
        line = RailwayLine(
            name=page['title'],
            status_page_url=page['url']
        )
        association = RailwayInfo(category=category, region=region,
                                  company=company, line=line)
        db.session.add(association)
        db.session.add(line)
    db.session.add(company)
    db.session.add(region)
    db.session.add(category)


def add_settings():
    print('Add default settings')

    set1 = Setting(app='pytenki')
    set2 = Setting(app='pydensha')
    set3 = Setting(app='gpio')

    db.session.add_all([set1, set2, set3])


@bp.cli.command('init_db')
def init_db():
    """Initialise DB"""
    clear_data()
    add_admin_user()
    add_settings()
    add_forecast_areas()
    add_regular_railway_data()
    add_rapid_railway_data()
    add_bullet_railway_data()
    db.session.commit()
