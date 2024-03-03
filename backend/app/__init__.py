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
    config_object = Config()
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
    CORS(app,
        origins=[config_object.CORS_ALLOW_ORIGIN], # the domains allowed to access the server
        supports_credentials=config_object.CORS_SUPPORTS_CREDENTIALS) # True
    # CORS(app)
    
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    
    db.init_app(app)
    migrate = Migrate(app, db)


    # Register blueprints, initialize extensions, etc.
    from app.controllers.submit import bp as submit_bp
    from app.controllers.confirmation import bp as confirmation_bp
    from app.controllers.signin import bp as signin
    app.register_blueprint(submit_bp)
    app.register_blueprint(confirmation_bp)
    app.register_blueprint(signin)

    return app
