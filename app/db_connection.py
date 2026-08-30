import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DEV_DATABASE_URL = os.getenv("DEV_DATABASE_URL") or ""

engine = create_engine(DEV_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, engine=engine, bind=engine)
# Base = declarative_base()


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
