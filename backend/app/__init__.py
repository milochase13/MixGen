from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Register blueprints, initialize extensions, etc.
    from app.main import bp as main_bp
    from app.confirmation import bp as confirmation_bp
    from app.signin import bp as signin
    app.register_blueprint(main_bp)
    app.register_blueprint(confirmation_bp)
    app.register_blueprint(signin)

    return app
