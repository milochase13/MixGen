from flask import Blueprint

bp = Blueprint('submit', __name__)

from app.controllers.submit import routes