import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    # Use a PostgreSQL database when SQLALCHEMY_DATABASE_URI is provided,
    # otherwise fall back to a local SQLite file.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///webcontrol.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
