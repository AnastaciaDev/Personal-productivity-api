
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app():

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Import models
    from app.models import User, Note

    # Import authentication routes
    from app.routes.auth import auth_bp

    from app.routes.notes import notes_bp

    app.register_blueprint(notes_bp)

    # Register authentication routes
    app.register_blueprint(auth_bp)

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health():
        return {
            "message": "Personal Productivity API is running!"
        }, 200

    return app


