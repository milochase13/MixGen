from flask import Blueprint

bp = Blueprint('confirmation', __name__)

from app.controllers.confirmation import routes