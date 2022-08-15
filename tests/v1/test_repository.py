import os

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.models.database import Base, Manufactures, Models, VinCodes
from core.models.repositories import ModelsRepo, ManufacturerRepo, VinCodeRepo
from core.schemas.schemas import ModelsCreate, ManufacturerCreate, VinCodeCreate
from core.settings import TEST_DATABASE_URL
from main import app

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
client = TestClient(app)


@pytest.fixture(autouse=True, scope="module")  # adjust your scope
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


def test_create_model():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    item_obj = ModelsCreate(name="new_model")
    result = repo.create(item=item_obj)
    assert result.name == "new_model"


def test_fetch_by_id_model():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_id(10)
    assert result.name == "test_name"


def test_fetch_by_name_model():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_name("test_name")
    assert result.id == 10


def test_fetch_by_name_model_not_found():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_name("test_na")
    assert result is None


def test_fetch_by_id_model_not_found():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_id(2)
    assert result is None


def test_fetch_all_model_isinstance():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    result = repo.fetch_all()
    assert isinstance(result, list)


def test_invalid_delete_model():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    item_obj = ModelsCreate(name="new_man")
    result = repo.create(item=item_obj)
    assert result is not None
    id_obj = repo.fetch_by_name("new_man").id
    assert id_obj is not None
    repo.delete(id_obj)
    obj = repo.fetch_by_id(id_obj)
    assert obj is None


def test_update_model():
    repo = ModelsRepo(db_session=TestingSessionLocal)
    item_obj = repo.fetch_by_id("10")
    item_obj.name = "new_name2"
    result = repo.update(item_obj)
    assert result.name == "new_name2"


def test_create_manufacturer():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    item_obj = ManufacturerCreate(name="new_manufacturer")
    result = repo.create(item=item_obj)
    assert result.name == "new_manufacturer"


def test_fetch_by_id_manufacturer():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_id(10)
    assert result.name == "test_name"


def test_fetch_by_id_manufacturer_not_found():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_id(2)
    assert result is None


def test_fetch_by_name_manufacturer():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_name("test_name")
    assert result.id == 10


def test_fetch_by_name_manufacturer_not_found():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_name("test_name252525")
    assert result is None


def test_fetch_all_manufacturer_isinstance():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    result = repo.fetch_all()
    assert isinstance(result, list)


def test_update_manufacturer():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    item_obj = repo.fetch_by_id("10")
    item_obj.name = "new_name2"
    result = repo.update(item_obj)
    assert result.name == "new_name2"


def test_delete_manufacturer():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    item_obj = ManufacturerCreate(name="new_man")
    result = repo.create(item=item_obj)
    assert result is not None
    id_obj = repo.fetch_by_name("new_man").id
    assert id_obj is not None
    repo.delete(id_obj)
    obj = repo.fetch_by_id(id_obj)
    assert obj is None


def test_create_vin_code():
    repo = VinCodeRepo(db_session=TestingSessionLocal)
    item_obj = VinCodeCreate(name="4Y1SL65848Z411435", manufacturer=10, model=10)
    result = repo.create(item=item_obj)
    assert result.name == "4Y1SL65848Z411435"


def test_invalid_create_vin_code():
    with pytest.raises(ValidationError):
        repo = VinCodeRepo(db_session=TestingSessionLocal)
        item_obj = VinCodeCreate(name="4Y1SL65848Z", manufacturer=10, model=10)
        repo.create(item=item_obj)


def test_fetch_by_id_vin_code_not_found():
    repo = VinCodeRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_id(2)
    assert result is None


def test_fetch_by_name_vin_code():
    repo = VinCodeRepo(db_session=TestingSessionLocal)
    result = repo.fetch_by_name("4Y1SL65848Z411439")
    assert result.id == 10


def test_update_vin_code():
    repo = ManufacturerRepo(db_session=TestingSessionLocal)
    item_obj = repo.fetch_by_id("10")
    item_obj.name = "BY1SL65848Z411439"
    result = repo.update(item_obj)
    assert result.name == "BY1SL65848Z411439"


def test_delete_vin_code():
    repo = VinCodeRepo(db_session=TestingSessionLocal)
    item_obj = VinCodeCreate(name="9Y1SL65848Z411439", manufacturer=10, model=10)
    result = repo.create(item=item_obj)
    assert result is not None
    id_obj = repo.fetch_by_name("9Y1SL65848Z411439").id
    assert id_obj is not None
    repo.delete(id_obj)
    obj = repo.fetch_by_id(id_obj)
    assert obj is None
