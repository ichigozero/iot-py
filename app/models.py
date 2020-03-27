import json

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app = db.Column(db.String(32), index=True, unique=True)
    value = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<Setting {}>'.format(self.app)

    @staticmethod
    def load_setting(app):
        setting = Setting.query.filter_by(app=app).first()
        return json.loads(setting.value)

    @staticmethod
    def update_setting(app, raw_data):
        setting = Setting.query.filter_by(app=app).first()
        setting.value = json.dumps(raw_data)
