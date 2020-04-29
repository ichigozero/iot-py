from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sse import sse
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
pytenki_task = None


def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.settings import bp as settings_bp
    app.register_blueprint(settings_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    app.register_blueprint(sse, url_prefix='/stream')

    return app


from app import models
