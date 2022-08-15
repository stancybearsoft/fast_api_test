import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from core.models.database import Base, Manufactures, Models, VinCodes
from main import app


SQLALCHEMY_DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://postgres:example@localhost:5432/fast_api')

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


client = TestClient(app)


@pytest.fixture(autouse=True, scope="module")
def create_test_database():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    s = TestingSessionLocal()

    manufactures = Manufactures(name="test_name", id=10)
    model = Models(name="test_name", id=10)
    vin_code = VinCodes(name="4Y1SL65848Z411439", manufacturer=10, model=10, id=10)
    s.add(manufactures)
    s.add(model)
    s.add(vin_code)
    s.commit()
    yield
    Base.metadata.drop_all(test_engine)


def test_read_item_bad_invalid_vin_code():
    response = client.get("/v1/vehicle/get/12568")
    assert response.status_code == 422


def test_read_item_not_defined_vin_code():
    response = client.get("/v1/vehicle/get/5Y1SL65848Z411438")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}


def test_read_item(create_test_database):
    response = client.get("/v1/vehicle/get/4Y1SL65848Z411439")
    assert response.status_code == 200
    assert response.json() == {'id': 10, 'model_id': 10, 'manufacturer_id': 10}

