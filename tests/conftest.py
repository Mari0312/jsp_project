import os

import pytest
from fastapi.testclient import TestClient
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import Config

TEST_DATABASE_NAME = 'jsp_test_db'
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test@example.com"
LIBRARIAN_TEST_EMAIL = "librariantest@example.com"
path, _ = os.environ['TEST_DB_STRING'].rsplit('/', 1)
Config.SQLALCHEMY_DATABASE_URI = f'{path}/{TEST_DATABASE_NAME}'


@pytest.fixture(autouse=True, scope='function')
def clear_db():
    from alembic.command import upgrade
    from alembic.config import Config
    from database import session, db
    import psycopg2
    session.close()
    db.dispose()
    conn = psycopg2.connect(dsn=os.environ['TEST_DB_STRING'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute(f'DROP DATABASE IF EXISTS {TEST_DATABASE_NAME}')
    cursor.execute(f'CREATE DATABASE {TEST_DATABASE_NAME}')
    cursor.close()

    config = Config("alembic.ini")
    upgrade(config, "head")


@pytest.fixture
def client():
    """A test client for the app."""
    from main import app
    return TestClient(app)


@pytest.fixture
def authentication_headers(client):
    from database import User
    from utils import create_access_token

    def _authentication_headers(is_librarian: bool = False):
        if is_librarian:
            email = LIBRARIAN_TEST_EMAIL
        else:
            email = TEST_EMAIL

        user = User.find_by_email(email)

        if user is None:
            user = User(
                first_name="John",
                last_name="Connor",
                birthday="2022-06-29",
                address="Lviv",
                phone_number="380972879503",
                email=email,
                password='testpass',
                is_librarian=is_librarian,
            ).save()

        auth_token = create_access_token(user.email)
        headers = {"Authorization-Token": auth_token}

        return headers

    return _authentication_headers
