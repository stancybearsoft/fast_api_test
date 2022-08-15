from sqlalchemy.orm import Session

from core.models.database import session, Models, Manufactures, VinCodes
from core.schemas.schemas import ModelsCreate, ManufacturerCreate, VinCodeCreate


class CrudMixin:
    """
    implements basic database operations
    """

    def fetch_by_id(self, _id):
        """
        get model by id
        :param _id:
        :return:
        """
        with self.session() as s:
            return s.query(self.model).filter(self.model.id == _id).first()

    def fetch_by_name(self, name):
        """
        get model by name
        :param name:
        :return:
        """
        with self.session() as s:
            return s.query(self.model).filter(self.model.name == name).first()

    def fetch_all(self, skip: int = 0, limit: int = 100):
        """
        get all model
        :param skip:
        :param limit:
        :return:
        """
        with self.session() as s:
            return s.query(self.model).offset(skip).limit(limit).all()

    def delete(self, item_id):
        """
        delete model
        :param item_id:
        :return:
        """
        with self.session() as s:
            db_item = s.query(self.model).filter_by(id=item_id).first()
            s.delete(db_item)
            s.commit()

    def update(self, item_data):
        """
        update model
        :param item_data:
        :return:
        """
        with self.session() as s:
            updated_item = s.merge(item_data)
            s.commit()
            s.refresh(updated_item)
            return updated_item


class ModelsRepo(CrudMixin):
    def __init__(self, db_session):
        self.session = db_session
        self.model = Models

    def create(self, item: ModelsCreate):
        """
        create record model
        :param item:
        :return:
        """
        db_item = self.model(name=item.name)
        with self.session() as s:
            s.add(db_item)
            s.commit()
            s.refresh(db_item)
        return db_item


class ManufacturerRepo(CrudMixin):
    def __init__(self, db_session):
        self.session = db_session
        self.model = Manufactures

    def create(self, item: ManufacturerCreate):
        """
        create record manufacturer
        :param item:
        :return:
        """
        db_item = self.model(name=item.name)
        with self.session() as s:
            s.add(db_item)
            s.commit()
            s.refresh(db_item)
        return db_item


class VinCodeRepo(CrudMixin):
    def __init__(self, db_session):
        if not db_session:
            self.session = session
        else:
            self.session = db_session
        self.model = VinCodes

    def create(self, item: VinCodeCreate):
        """
        create record vin code
        :param item:
        :return:
        """
        db_item = self.model(name=item.name, manufacturer=item.manufacturer, model=item.model)
        with self.session() as s:
            s.add(db_item)
            s.commit()
            s.refresh(db_item)
        return db_item

    async def get_vin_code_info(self, vin_code: str):
        """
        returns information about vehicle by vin code
        :param vin_code:
        :return:
        """
        with self.session() as s:
            result = s.query(self.model).filter(self.model.name == vin_code).first()
            if result:
                return {"id": result.id, "model_id": result.model, "manufacturer_id": result.manufacturer}


vin_code_repo = VinCodeRepo(db_session=session)
manufacturer_repo = ManufacturerRepo(db_session=session)
models_repo = ModelsRepo(db_session=session)
