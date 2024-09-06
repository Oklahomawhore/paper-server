import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///papers.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key_for_flask_app'
