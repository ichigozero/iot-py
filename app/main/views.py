from flask import render_template

import app
import app.tasks
from app.main import bp


@bp.before_app_first_request
def start_all_background_tasks():
    app.pytenki_task = app.tasks.PyTenkiTask()
    app.pytenki_task.init_task()
    app.pytenki_task.start()

    app.pydensha_task = app.tasks.PyDenshaTask()
    app.pydensha_task.init_task()
    app.pydensha_task.start()


@bp.route('/')
@bp.route('/index')
def index():
    pytenki_data = app.pytenki_task.get_fetched_data()
    pydensha_data = app.pydensha_task.get_fetched_data()
    return render_template(
        'index.html',
        title='Index',
        today_fcast=pytenki_data['fcast']['today'],
        tomorrow_fcast=pytenki_data['fcast']['tomorrow'],
        fcast_loc=pytenki_data['fcast_loc'],
        fcast_24_hours=pytenki_data['fcast_24_hours'],
        rail_category=pydensha_data['rail_category'],
        rail_info=pydensha_data['rail_info']
    )
