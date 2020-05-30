from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

import app
from app import db
from app.helper import get_dict_val
from app.models import (
    City,
    PinpointLocation,
    Prefecture,
    RailwayCategory,
    RailwayCompany,
    RailwayInfo,
    RailwayLine,
    RailwayRegion,
    Region,
    Setting
)
from app.settings import bp
from app.settings.forms import PyTenkiForm, PyDenshaForm


def store_pytenki_form_data_to_db(form, gpio):
    Setting.update_setting(
        app='pytenki',
        raw_data={
            'fcst_area': {
                'region_id': form.region.data.id,
                'pref_id': form.prefecture.data.id,
                'city_id': form.city.data.id,
                'pinpoint_id': form.pinpoint_loc.data.id
            },
            'fetch_intvl': form.fetch_intvl.data,
            'led_duration': {
                'blink_on_time': form.blink_on_time.data,
                'blink_off_time': form.blink_off_time.data,
                'fade_in_time': form.fade_in_time.data,
                'fade_out_time': form.fade_out_time.data,
            },
        }
    )

    led_normal = get_dict_val(gpio, ['train_info', 'led', 'normal'])
    led_delayed = get_dict_val(gpio, ['train_info', 'led', 'delayed'])
    led_other = get_dict_val(gpio, ['train_info', 'led', 'other'])

    Setting.update_setting(
        app='gpio',
        raw_data={
            'weather': {
                'led': {
                    'fine': form.led_fine.data,
                    'cloud': form.led_cloud.data,
                    'rain': form.led_rain.data,
                    'snow': form.led_snow.data
                },
                'tts_button': form.tts_button.data
            },
            'train_info': {
                'led': {
                    'normal': led_normal,
                    'delayed': led_delayed,
                    'other': led_other
                },
                'tts_button': form.tts_button.data
            },
        }
    )


@bp.route('/settings/pytenki', methods=['GET', 'POST'])
@login_required
def pytenki():
    pytenki = Setting.load_setting('pytenki')
    gpio = Setting.load_setting('gpio')

    region_id_old = get_dict_val(pytenki, ['fcst_area', 'region_id'])
    pref_id_old = get_dict_val(pytenki, ['fcst_area', 'pref_id'])
    city_id_old = get_dict_val(pytenki, ['fcst_area', 'city_id'])
    pinpoint_id_old = get_dict_val(pytenki, ['fcst_area', 'pinpoint_id'])

    form = PyTenkiForm(
        region=Region.query.get(region_id_old),
        prefecture=Prefecture.query.get(pref_id_old),
        city=City.query.get(city_id_old),
        pinpoint_loc=PinpointLocation.query.get(pinpoint_id_old),
        fetch_intvl=get_dict_val(pytenki, ['fetch_intvl']) or 35,
        blink_on_time=get_dict_val(
            pytenki, ['led_duration', 'blink_on_time']) or 3.0,
        blink_off_time=get_dict_val(
            pytenki, ['led_duration', 'blink_off_time']) or 2.0,
        fade_in_time=get_dict_val(
            pytenki, ['led_duration', 'fade_in_time']) or 3.0,
        fade_out_time=get_dict_val(
            pytenki, ['led_duration', 'fade_out_time']) or 2.0,
        led_fine=get_dict_val(gpio, ['weather', 'led', 'fine']),
        led_cloud=get_dict_val(gpio, ['weather', 'led', 'cloud']),
        led_rain=get_dict_val(gpio, ['weather', 'led', 'rain']),
        led_snow=get_dict_val(gpio, ['weather', 'led', 'snow']),
        tts_button=get_dict_val(gpio, ['weather', 'tts_button']),
    )

    region_id = (
        request.form.get('region')
        or region_id_old
        or Region.query.first().id
    )

    pref_id = request.form.get('prefecture')

    if region_id == region_id_old:
        pref_id = pref_id or pref_id_old
    else:
        pref_id = pref_id or Prefecture.query.filter_by(
            region_id=region_id).first().id

    city_id = request.form.get('city')

    if pref_id == pref_id_old:
        city_id = city_id or city_id_old
    else:
        city_id = city_id or City.query.filter_by(pref_id=pref_id).first().id

    form.region.query = Region.query
    form.prefecture.query = Prefecture.query.filter_by(region_id=region_id)
    form.city.query = City.query.filter_by(pref_id=pref_id)
    form.pinpoint_loc.query = PinpointLocation.query.filter_by(city_id=city_id)

    if form.validate_on_submit():
        store_pytenki_form_data_to_db(form, gpio)
        db.session.commit()

        app.pytenki_task.init_task()
        app.pytenki_task.restart()

        flash('PyTenki Settings Have Been Updated Successfully', 'success')
        return redirect(url_for('settings.pytenki'))

    return render_template(
        'settings/pytenki.html',
        title='PyTenki - Settings',
        form=form
    )


@bp.route('/settings/pytenki/areas-by-region', methods=['POST'])
@login_required
def areas_by_region():
    region_id = int(request.form.get('region'))
    prefectures = Prefecture.query.filter_by(region_id=region_id)
    cities = City.query.filter_by(pref_id=prefectures.first().id)
    pinpoints = PinpointLocation.query.filter_by(city_id=cities.first().id)

    choices = {
        'prefectures': get_choices_of_area(prefectures),
        'cities': get_choices_of_area(cities),
        'pinpoints': get_choices_of_area(pinpoints)
    }

    return jsonify(choices=choices)


@bp.route('/settings/pytenki/areas-by-prefecture', methods=['POST'])
@login_required
def areas_by_prefecture():
    pref_id = int(request.form.get('prefecture'))
    cities = City.query.filter_by(pref_id=pref_id)
    pinpoints = PinpointLocation.query.filter_by(city_id=cities.first().id)

    choices = {
        'cities': get_choices_of_area(cities),
        'pinpoints': get_choices_of_area(pinpoints)
    }

    return jsonify(choices=choices)


@bp.route('/settings/pytenki/areas-by-city', methods=['POST'])
@login_required
def areas_by_city():
    city_id = int(request.form.get('city'))
    pinpoints = PinpointLocation.query.filter_by(city_id=city_id)
    choices = {'pinpoints': get_choices_of_area(pinpoints)}

    return jsonify(choices=choices)


def get_choices_of_area(areas):
    choices = list()
    choices.append({'value': '__None', 'text': ''})

    for area in areas:
        choices.append({'value': area.id, 'text': area.name})

    return choices


def store_pydensha_form_data_to_db(form, gpio):
    led_fine = get_dict_val(gpio, ['weather', 'led', 'fine'])
    led_cloud = get_dict_val(gpio, ['weather', 'led', 'cloud'])
    led_rain = get_dict_val(gpio, ['weather', 'led', 'rain'])
    led_snow = get_dict_val(gpio, ['weather', 'led', 'snow'])
    tts_button = get_dict_val(gpio, ['weather', 'tts_button'])

    Setting.update_setting(
        app='pydensha',
        raw_data={
            'rail_info': {
                'category_id': form.category.data.id,
                'region_id': form.region.data.id,
                'company_id': form.company.data.id,
                'line_ids': [data.id for data in form.line.data],
            },
            'fetch_intvl': form.fetch_intvl.data,
        }
    )
    Setting.update_setting(
        app='gpio',
        raw_data={
            'weather': {
                'led': {
                    'fine': led_fine,
                    'cloud': led_cloud,
                    'rain': led_rain,
                    'snow': led_snow
                },
                'tts_button': tts_button
            },
            'train_info': {
                'led': {
                    'normal': form.led_normal.data,
                    'delayed': form.led_delayed.data,
                    'other': form.led_other.data
                }
            }
        }
    )


@bp.route('/settings/pydensha', methods=['GET', 'POST'])
@login_required
def pydensha():
    pydensha = Setting.load_setting('pydensha')
    gpio = Setting.load_setting('gpio')

    category_id_old = get_dict_val(pydensha, ['rail_info', 'category_id'])
    company_id_old = get_dict_val(pydensha, ['rail_info', 'company_id'])
    region_id_old = get_dict_val(pydensha, ['rail_info', 'region_id'])
    line_ids_old = get_dict_val(pydensha, ['rail_info', 'line_ids'])

    form = PyDenshaForm(
        category=RailwayCategory.query.get(category_id_old),
        region=RailwayRegion.query.get(region_id_old),
        company=RailwayCompany.query.get(company_id_old),
        line=[RailwayLine.query.get(id)
              for id in line_ids_old if line_ids_old],
        fetch_intvl=get_dict_val(pydensha, ['fetch_intvl']) or 35,
        led_normal=get_dict_val(gpio, ['train_info', 'led', 'normal']),
        led_delayed=get_dict_val(gpio, ['train_info', 'led', 'delayed']),
        led_other=get_dict_val(gpio, ['train_info', 'led', 'other'])
    )

    category_id = (
        request.form.get('category')
        or category_id_old
        or RailwayCategory.query.first().id
    )

    if category_id == category_id_old:
        company_id = request.form.get('company') or company_id_old
    else:
        company_id = (
            RailwayInfo
            .query
            .filter_by(category_id=category_id)
            .first()
            .company_id
        )

    if company_id == company_id_old:
        region_id = request.form.get('region') or region_id_old
    else:
        region_id = (
            RailwayInfo
            .query
            .filter_by(category_id=category_id, company_id=company_id)
            .first()
            .region_id
        )

    form.category.query = RailwayCategory.query
    form.region.query = (
        RailwayRegion
        .query
        .join(RailwayInfo)
        .filter_by(category_id=category_id)
    )
    form.company.query = (
        RailwayCompany
        .query
        .join(RailwayInfo)
        .filter_by(
            category_id=category_id,
            region_id=region_id
        )
    )
    form.line.query = (
        RailwayLine
        .query
        .join(RailwayInfo)
        .filter_by(
            category_id=category_id,
            region_id=region_id,
            company_id=company_id
        )
    )

    if form.validate_on_submit():
        store_pydensha_form_data_to_db(form, gpio)
        db.session.commit()
        flash('PyDensha Settings Have Been Updated Successfully', 'success')
        return redirect(url_for('settings.pydensha'))

    return render_template(
        'settings/pydensha.html',
        title='PyDensha - Settings',
        form=form
    )
