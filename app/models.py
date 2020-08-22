import simplejson as json
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
        try:
            return json.loads(setting.value)
        except TypeError:
            return None

    @staticmethod
    def update_setting(app, raw_data):
        setting = Setting.query.filter_by(app=app).first()
        setting.value = json.dumps(raw_data)


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String(32))
    prefectures = db.relationship(
        'Prefecture',
        backref='region',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Region {}>'.format(self.name)


class Prefecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String(32))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    subprefectures = db.relationship(
        'Subprefecture',
        backref='prefecture',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Prefecture {}>'.format(self.name)


class Subprefecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String(64))
    prefecture_id = db.Column(db.Integer, db.ForeignKey('prefecture.id'))
    cities = db.relationship(
        'City',
        backref='subprefecture',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Subprefecture {}>'.format(self.name)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String(64))
    subprefecture_id = db.Column(
        db.Integer,
        db.ForeignKey('subprefecture.id')
    )

    def __repr__(self):
        return '<City {}>'.format(self.name)


class PinpointLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(64), index=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    def __repr__(self):
        return '<PinpointLocation {}>'.format(self.name)


class RailwayCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    infos = db.relationship('RailwayInfo', backref='category',
                            lazy='dynamic')

    def __repr__(self):
        return '<RailwayCategory {}>'.format(self.name)


class RailwayRegion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    infos = db.relationship('RailwayInfo', backref='region',
                            lazy='dynamic')

    def __repr__(self):
        return '<RailwayRegion {}>'.format(self.name)


class RailwayCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    infos = db.relationship('RailwayInfo', backref='company',
                            lazy='dynamic')

    def __repr__(self):
        return '<RailwayCompany {}>'.format(self.name)


class RailwayLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    status_page_url = db.Column(db.String(64), index=True)
    infos = db.relationship('RailwayInfo', backref='line',
                            lazy='dynamic')

    def __repr__(self):
        return '<Railway {}>'.format(self.name)


class RailwayInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('railway_category.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('railway_region.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('railway_company.id'))
    line_id = db.Column(db.Integer, db.ForeignKey('railway_line.id'))

    __table_args__ = (
        db.UniqueConstraint(category_id, region_id, company_id, line_id),)
