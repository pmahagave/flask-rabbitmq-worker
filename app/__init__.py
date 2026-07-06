from flask import Flask
from .config import Config
from .db import init_db
from .producer import bp as producer_bp
from .delay_api import bp as delay_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(producer_bp, url_prefix='/api')
    app.register_blueprint(delay_bp, url_prefix='/api')
    
    return app

__all__ = ['create_app', 'init_db']