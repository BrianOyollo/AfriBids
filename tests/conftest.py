from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
import os
from dotenv import load_dotenv
from app.database import Base, get_db
from app.main import app


load_dotenv()
POSTGRES_USERNAME=os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DATABASE_NAME=os.getenv('TEST_DATABASE_NAME')
POSTGRES_PORT=os.getenv('POSTGRES_PORT')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')


SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def TestSession():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(TestSession):
    def override_get_db():
        try:
            yield TestSession
        finally:
            TestSession.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



@pytest.fixture
def test_user(client):
    dummy_user = {
        "email":"testuser@gmail.com",
        "display_name":"testuser_123",
        "password": "TestPassword123"
    }

    response = client.post("/users/new", json=dummy_user)
    test_user = response.json()
    test_user['password'] = dummy_user['password']
    return test_user