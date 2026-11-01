import os

class Config:
    # Security key used by Flask sessions
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-secret-key-change-later"
    )

    # Database configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session cookie security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False

    # Session lifetime
    PERMANENT_SESSION_LIFETIME = 3600