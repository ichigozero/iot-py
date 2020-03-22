from flask import Blueprint

from app.models import db, User


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


@bp.cli.command('init_db')
def init_db():
    """Initialise DB"""
    clear_data()
    add_admin_user()

    db.session.commit()
