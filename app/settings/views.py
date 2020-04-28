from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

import app
from app import db
from app.helper import get_dict_val
from app.models import City, PinpointLocation, Prefecture, Region, Setting
from app.settings import bp
from app.settings.forms import PyTenkiForm


def store_form_data_to_db(form):
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
    Setting.update_setting(
        app='gpio',
        raw_data={
            'led': {
                'fine': form.led_fine.data,
                'cloud': form.led_cloud.data,
                'rain': form.led_rain.data,
                'snow': form.led_snow.data
            },
            'tts_button': form.tts_button.data
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
        led_fine=get_dict_val(gpio, ['led', 'fine']),
        led_cloud=get_dict_val(gpio, ['led', 'cloud']),
        led_rain=get_dict_val(gpio, ['led', 'rain']),
        led_snow=get_dict_val(gpio, ['led', 'snow']),
        tts_button=get_dict_val(gpio, ['tts_button']),
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
        store_form_data_to_db(form)
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
