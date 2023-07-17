from flask import Blueprint

bp = Blueprint('signin', __name__)

from app.signin import routes