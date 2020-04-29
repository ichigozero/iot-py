from flask import render_template

import app
import app.tasks
from app.main import bp


@bp.before_app_first_request
def start_all_background_tasks():
    app.pytenki_task = app.tasks.PyTenkiTask()
    app.pytenki_task.init_task()
    app.pytenki_task.start()


@bp.route('/')
@bp.route('/index')
def index():
    data = app.pytenki_task.get_fetched_data()
    return render_template(
        'index.html',
        title='Index',
        today_fcast=data['fcast']['today'],
        tomorrow_fcast=data['fcast']['tomorrow'],
        fcast_loc=data['fcast_loc'],
        fcast_24_hours=data['fcast_24_hours']
    )
