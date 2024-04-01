from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask extensions, but without any Flask application instance
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Application Configuration
    app.config.from_object(config_class)
    
    # Initialize extensions with the application instance
    db.init_app(app)
    
    # Import and register Blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
