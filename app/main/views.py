from flask import render_template

from app import pytenki_task
from app.main import bp
from app.tasks import PyTenkiTask


@bp.before_app_first_request
def start_all_background_tasks():
    global pytenki_task
    pytenki_task = PyTenkiTask()
    pytenki_task.init_task()
    pytenki_task.start()


@bp.route('/')
@bp.route('/index')
def index():
    data = pytenki_task.get_fetched_data()
    return render_template(
        'index.html',
        title='Index',
        today_fcast=data['fcast']['today'],
        tomorrow_fcast=data['fcast']['tomorrow'],
        fcast_loc=data['fcast_loc'],
        fcast_24_hours=data['fcast_24_hours']
    )
