import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    REDIS_URL = 'redis://localhost'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'himitsu-kagi'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
