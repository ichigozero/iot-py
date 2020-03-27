from flask import redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.models import Setting
from app.settings import bp
from app.settings.forms import PyTenkiForm


def store_form_data_to_db(form):
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
    form = PyTenkiForm()

    if form.validate_on_submit():
        store_form_data_to_db(form)
        db.session.commit()
        return redirect(url_for('settings.pytenki'))

    return render_template(
        'settings/pytenki.html',
        title='PyTenki - Settings',
        form=form
    )
