import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

from main import app
from database import get_session

@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def client(test_engine):
    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def alumni_data():
    return {
        "ime": "Ana",
        "prezime": "Kovač",
        "spol": "F",
        "broj_indeksa": "0123456",
        "fakultet": "Pravni fakultet",
        "odsjek": "Pravo",
        "godina_pocetka": "2016/2017",
        "godina_zavrsetka": "2020/2021",
        "broj_diplome": "D-2020-001"
    }