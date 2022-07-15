from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, insert
)
from sqlalchemy.sql import func, select

from models.async_db_session import AsyncDatabaseSession

Base = declarative_base()


class CheckDataTableMixin:
    @classmethod
    async def check_data(cls, session: AsyncDatabaseSession) -> bool:
        """
        checks if there is data in this table
        :param session:
        :return: bool
        """
        try:
            query = select(cls)
            results = await session.execute(query)
            return True if results else False
            # return results.one()
        except NoResultFound:
            return False
        finally:
            await session.close()


class NewInstanceMixin:
    @classmethod
    async def new_instance(cls, session: AsyncDatabaseSession, name: str):
        """
        creates a new record in this table
        :param session:
        :param name:
        :return:
        """
        try:
            query = insert(cls).values(name=name)
            await session.execute(query)
            await session.commit()
            return True
        finally:
            await session.close()


class DataToDictMixin:
    def as_dict(self):
        """
        returns a dictionary of the object where the dictionary keys are columns that exist in the table
        keys can be None here but they need to exist as attributes and be in the columns
        """
        return_dict = {}
        for key, value in vars(self).items():
            if key in self.__table__.columns:
                return_dict[key] = value
        return return_dict


class Manufactures(Base, DataToDictMixin, NewInstanceMixin, CheckDataTableMixin):
    __tablename__ = 'manufactures'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(256))


class Models(Base, DataToDictMixin, NewInstanceMixin, CheckDataTableMixin):
    __tablename__ = 'models'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(256))


class VinCodes(Base, DataToDictMixin, CheckDataTableMixin):
    __tablename__ = 'vin_codes'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)
    model = Column(Integer, ForeignKey("models.id"))
    manufacture = Column(Integer, ForeignKey("manufactures.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    @classmethod
    async def get_vin_code_info(cls, session: AsyncDatabaseSession, vin_code: str):
        """
        returns information about vehicle by vin code
        :param session:
        :param vin_code:
        :return:
        """
        try:
            query = select(cls.id, Models.id, Manufactures.id) \
                .join(Models.id, cls.model == Models.id) \
                .join(Manufactures.id, cls.manufacture == Manufactures.id) \
                .where(cls.name == vin_code)
            results = await session.execute(query)
            results = results.one()
            return {"id": results[0], "model_id": results[1], "manufacturer_id": results[2]}
        except NoResultFound:
            return None
        finally:
            await session.close()

    @classmethod
    async def new_vin_code(cls, session: AsyncDatabaseSession, name: str, model_id: int, manufacture_id: int):
        """
        creates a new entry in the table vin_codes
        :param session:
        :param name:
        :param model_id:
        :param manufacture_id:
        :return:
        """
        try:
            query = insert(cls).values(name=name, model=model_id, manufacture=manufacture_id)
            await session.execute(query)
            await session.commit()
            return True
        finally:
            await session.close()
