from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base
from app.main import app
import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}' \
                          f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)  # creates the tables for the _test database
    Base.metadata.create_all(bind=engine)  # creates the tables for the _test database
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # Dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)