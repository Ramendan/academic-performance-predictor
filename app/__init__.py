"""
Flask application factory for the Academic Performance Monitoring & Prediction System.
"""

import os
from flask import Flask
from config import config


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure required directories exist
    os.makedirs(app.config["MODEL_DIR"], exist_ok=True)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.students import students_bp
    from app.routes.analytics import analytics_bp
    from app.routes.predictions import predictions_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(predictions_bp)

    return app
