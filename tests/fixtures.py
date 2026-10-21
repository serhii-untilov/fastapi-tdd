import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from tests.utils.database_utils import migrate_to_db
from tests.utils.docker_utils import start_database_container


@pytest.fixture(scope="session", autouse=True)
def test_db_container():
    # Starts (or reuses) the test-db container for every test run,
    # including unit tests, and leaves it running after the session
    # so the DB stays reachable afterwards:
    # psql postgresql://postgres:postgres@127.0.0.1:5445/inventory
    container = start_database_container()
    migrate_to_db()
    yield container
    # container intentionally NOT stopped/removed here


@pytest.fixture(scope="session")
def db_session(test_db_container):
    url = os.getenv("TEST_DATABASE_URL") or ""
    print("url: ", url)
    engine = create_engine(url)

    SessionLocal = sessionmaker(autoflush=True, bind=engine)

    yield SessionLocal

    # container.stop()
    # container.remove()
    # engine.dispose()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as _client:
        yield _client
