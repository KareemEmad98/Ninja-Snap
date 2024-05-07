import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder=Config.TEMPLATES_DIR)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    Bootstrap(app)
    db.init_app(app)
    setup_logging(app)
    from .views import main_blueprint

    app.register_blueprint(main_blueprint)
    with app.app_context():
        db.create_all()
    return app


def setup_logging(app):
    if not os.path.exists(Config.LOGGING_DIR):
        os.makedirs(Config.LOGGING_DIR)

        # General App Logger
    app_logger = logging.getLogger("app_logger")
    file_handler = RotatingFileHandler(
        os.path.join(Config.LOGGING_DIR, Config.LOG_FILE_NAME),
        maxBytes=10000,
        backupCount=10,
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    app_logger.addHandler(file_handler)
    app_logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # API Logger
    api_logger = logging.getLogger("api_logger")
    api_file_handler = RotatingFileHandler(
        os.path.join(Config.LOGGING_DIR, Config.API_LOG_FILE_NAME),
        maxBytes=10000,
        backupCount=10,
    )
    api_file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(funcName)s:%(lineno)d]"
        )
    )
    api_logger.addHandler(api_file_handler)
    api_logger.setLevel(logging.INFO)

    # DB Logger
    db_logger = logging.getLogger("db_logger")
    db_file_handler = RotatingFileHandler(
        os.path.join(Config.LOGGING_DIR, Config.DB_LOG_FILE_NAME),
        maxBytes=10000,
        backupCount=10,
    )
    db_file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(funcName)s:%(lineno)d]"
        )
    )
    db_logger.addHandler(db_file_handler)
    db_logger.setLevel(logging.INFO)
    app.logger.info("Logger Setup Done")
