import os
from dotenv import load_dotenv

project_root = os.getcwd()
load_dotenv(os.path.join(project_root, '.env'))


class Config(object):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    JWT_ACCESS_TOKEN_EXPIRES = 1200  # seconds
    JWT_REFRESH_TOKEN_EXPIRES = 800_000
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_STRING")
