import operator
from functools import reduce

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
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


def get_dict_val(dict_obj, map_list):
    try:
        return reduce(operator.getitem, map_list, dict_obj)
    except (KeyError, TypeError):
        return ''


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

    if region_id == region_id_old:
        pref_id = request.form.get('prefecture') or pref_id_old
    else:
        pref_id = Prefecture.query.filter_by(region_id=region_id).first().id

    if pref_id == pref_id_old:
        city_id = request.form.get('city') or city_id_old
    else:
        city_id = City.query.filter_by(pref_id=pref_id).first().id

    form.region.query = Region.query
    form.prefecture.query = Prefecture.query.filter_by(region_id=region_id)
    form.city.query = City.query.filter_by(pref_id=pref_id)
    form.pinpoint_loc.query = PinpointLocation.query.filter_by(city_id=city_id)

    if form.validate_on_submit():
        store_form_data_to_db(form)
        db.session.commit()
        flash('PyTenki Settings Have Been Updated Successfully', 'success')
        return redirect(url_for('settings.pytenki'))

    return render_template(
        'settings/pytenki.html',
        title='PyTenki - Settings',
        form=form
    )
