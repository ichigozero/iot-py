from flask import Blueprint

from app.models import db, Setting, User


bp = Blueprint('cli', __name__)


def clear_data():
    meta = db.metadata

    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())


def add_admin_user():
    print('Add admin user')

    user = User(username='admin')
    user.set_password('Computer1')

    db.session.add(user)


def add_settings():
    print('Add default settings')

    set1 = Setting(app='pytenki')
    set2 = Setting(app='gpio')

    db.session.add_all([set1, set2])


@bp.cli.command('init_db')
def init_db():
    """Initialise DB"""
    clear_data()
    add_admin_user()
    add_settings()

    db.session.commit()
