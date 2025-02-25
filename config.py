from datetime import timedelta
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)


class DevelopmentConfig(Config):
    DEBUG = True
    server = "(localdb)\MSSQLLocaldb"
    database = "happy_kitchen"
    driver = "{ODBC Driver 17 for SQL Server}"
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={quote_plus(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')}"


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
