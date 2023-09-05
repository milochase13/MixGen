from flask import Flask, session
from flask_cors import CORS
from config import Config
from config_prod import ConfigProd
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
db_prod = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    
    db.init_app(app)
    migrate = Migrate(app, db)


    # Register blueprints, initialize extensions, etc.
    from app.main import bp as main_bp
    from app.confirmation import bp as confirmation_bp
    from app.signin import bp as signin
    app.register_blueprint(main_bp)
    app.register_blueprint(confirmation_bp)
    app.register_blueprint(signin)

    return app
