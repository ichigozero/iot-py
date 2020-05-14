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
    name = db.Column(db.String(32), index=True)
    prefectures = db.relationship('Prefecture', backref='region',
                                  lazy='dynamic')

    def __repr__(self):
        return '<Region {}>'.format(self.name)


class Prefecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    cities = db.relationship('City', backref='prefecture', lazy='dynamic')

    def __repr__(self):
        return '<Prefecture {}>'.format(self.name)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(64), index=True)
    pref_id = db.Column(db.Integer, db.ForeignKey('prefecture.id'))
    pinpoints = db.relationship('PinpointLocation', backref='city',
                                lazy='dynamic')

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
    railways = db.relationship('Railway', backref='category', lazy='dynamic')
    companies = db.relationship(
        'RailwayCompany',
        secondary=db.Table(
            'railway_category_company', db.Model.metadata,
            db.Column('railway_category_id', db.Integer,
                      db.ForeignKey('railway_category.id')),
            db.Column('railway_company_id', db.Integer,
                      db.ForeignKey('railway_company.id'))
        )
    )

    def __repr__(self):
        return '<RailwayCategory {}>'.format(self.name)


class RailwayCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    regions = db.relationship(
        'RailwayRegion',
        secondary=db.Table(
            'railway_company_region', db.Model.metadata,
            db.Column('railway_company_id', db.Integer,
                      db.ForeignKey('railway_company.id')),
            db.Column('railway_region_id', db.Integer,
                      db.ForeignKey('railway_region.id'))
        )
    )

    def __repr__(self):
        return '<RailwayCompany {}>'.format(self.name)


class RailwayRegion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    railways = db.relationship('Railway', backref='region', lazy='dynamic')

    def __repr__(self):
        return '<RailwayRegion {}>'.format(self.name)


class Railway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    status_page_url = db.Column(db.String(64), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('railway_category.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('railway_region.id'))

    def __repr__(self):
        return '<Railway {}>'.format(self.name)
