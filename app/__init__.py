from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sse import sse
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
pytenki_task = None
pydensha_task = None


def create_app(class_config=Config):
    app = Flask(__name__, static_url_path='/iot-py/static')
    app.config.from_object(class_config)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/iot-py')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/iot-py')

    from app.settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/iot-py')

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp, url_prefix='/iot-py')

    app.register_blueprint(sse, url_prefix='/iot-py/stream')

    return app


from app import models
