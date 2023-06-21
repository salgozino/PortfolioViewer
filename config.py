import os

basedir = os.path.abspath(os.path.dirname(__file__))

username = os.environ.get('MYSQL_DATABASE_USER')
password = os.environ.get('MYSQL_DATABASE_PASSWORD')
host = os.environ.get('MYSQL_DATABASE_HOST')
port = os.environ.get('MYSQL_DATABASE_PORT')
database_name = os.environ.get('MYSQL_DATABASE_DB')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if os.environ.get('FLASK_ENV') == 'development':
        host = 'localhost'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True
