from flask import render_template
from flask_login import login_required

from app.settings import bp


@bp.route('/settings/pytenki')
@login_required
def pytenki():
    return render_template(
        'settings/pytenki.html',
        title='PyTenki - Settings'
    )
