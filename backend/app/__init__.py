from flask import Flask
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

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
