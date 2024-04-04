from flask import Flask
from .models import db
from .routes import bp  # Adjust the import path as necessary

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    
    db.init_app(app)
    app.register_blueprint(bp, url_prefix='/api')

    return app
