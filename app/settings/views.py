import operator
from functools import reduce

from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.models import City, PinpointLocation, Prefecture, Region, Setting
from app.settings import bp
from app.settings.forms import PyTenkiForm


def store_form_data_to_db(form):
    Setting.update_setting(
        app='pytenki',
        raw_data={
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
    form = PyTenkiForm(
        fetch_intvl=get_dict_val(pytenki, ['fetch_intvl']) or 35,
        led_fine=get_dict_val(gpio, ['led', 'fine']),
        led_cloud=get_dict_val(gpio, ['led', 'cloud']),
        led_rain=get_dict_val(gpio, ['led', 'rain']),
        led_snow=get_dict_val(gpio, ['led', 'snow']),
        tts_button=get_dict_val(gpio, ['tts_button']),
    )
    form.region.query = Region.query
    form.prefecture.query = Prefecture.query
    form.city.query = City.query
    form.pinpoint_loc.query = PinpointLocation.query

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
