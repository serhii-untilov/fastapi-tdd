import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db_connection import get_db_session
from app.main import app
from tests.utils.database_utils import migrate_to_db
from tests.utils.docker_utils import start_database_container


@pytest.fixture(scope="function")
def db_session_integration():
    container = start_database_container()
    url = os.getenv("TEST_DATABASE_URL") or ""
    print("url: ", url)
    engine = create_engine(url)

    migrate_to_db()

    SessionLocal = sessionmaker(autoflush=True, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    container.stop()
    container.remove()
    engine.dispose()


@pytest.fixture()
def override_get_db_session(db_session_integration):
    def override():
        return db_session_integration

    app.dependency_overrides[get_db_session] = override


@pytest.fixture(scope="function")
def client(override_get_db_session):
    with TestClient(app) as _client:
        yield _client
