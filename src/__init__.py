from flask import Flask
from .modules import index, dashboard, data, about
from .config.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(index.main, url_prefix='/')
    app.register_blueprint(dashboard.main, url_prefix='/dashboard')
    app.register_blueprint(data.main, url_prefix='/data')
    app.register_blueprint(about.main, url_prefix='/about')


    return app