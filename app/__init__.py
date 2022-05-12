from flask import Flask
from app.config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_environment):
    app = Flask(__name__)
    app.config.from_object(config_options[config_environment])
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprint
    from app.main import auth, landing
    from app import views, forms
    app.register_blueprint(auth.auth)
    app.register_blueprint(landing.landing)

    return app
