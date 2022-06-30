import os
from dotenv import load_dotenv

project_root = os.getcwd()
load_dotenv(os.path.join(project_root, '.env'))


class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = 1200
    JWT_REFRESH_TOKEN_EXPIRES = 800_000
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_STRING")
