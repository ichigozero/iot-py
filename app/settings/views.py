from flask import render_template
from flask_login import login_required

from app.settings import bp
from app.settings.forms import PyTenkiForm


@bp.route('/settings/pytenki')
@login_required
def pytenki():
    form = PyTenkiForm()

    return render_template(
        'settings/pytenki.html',
        title='PyTenki - Settings',
        form=form
    )
