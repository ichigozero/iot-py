from flask import Blueprint

bp = Blueprint('settings', __name__)

from app.settings import views
