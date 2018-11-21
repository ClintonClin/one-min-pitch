import os
# allow for interaction with the operating system dependent functionality
class Config:
    """
    Describes the general configs
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOADED_PHOTOS_DEST = 'app/static/photos' #fjfj
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://clinton:admin@localhost/pitches'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # mail config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # simple mde  config
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True


class ProdConfig(Config):
    """
    Describes production config of child class
    Args:
        Config: The parent configration class with General config settings
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://clinton:admin@localhost/pitches'


class DevConfig(Config):
    """
    Describes development configuration child class
    Args:
         Config: The parent configuration class with General configuration settings
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://clinton:admin@localhost/pitches'
    DEBUG = True
# Dictionary
config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
