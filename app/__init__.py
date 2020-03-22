from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app


from app import models
