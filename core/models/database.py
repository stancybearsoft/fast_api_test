from contextlib import contextmanager


from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from core.settings import SQLALCHEMY_DATABASE_URL


Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)


@contextmanager
def session():
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    try:
        yield db_session
    except Exception as e:
        print('sql', e)
    finally:
        db_session.remove()
        connection.close()


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


class Manufactures(Base, DataToDictMixin):
    __tablename__ = 'manufactures'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(256))

    def __repr__(self):
        return f"Manufactures model id: {self.id}, name: {self.name}"


class Models(Base, DataToDictMixin):
    __tablename__ = 'models'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(256))

    def __repr__(self):
        return f"Models model id: {self.id}, name: {self.name}"


class VinCodes(Base, DataToDictMixin):
    __tablename__ = 'vin_codes'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)
    model = Column(Integer, ForeignKey("models.id"))
    manufacturer = Column(Integer, ForeignKey("manufactures.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"VinCodes model id: {self.id}, name: {self.name} " \
               f"model_id: {self.model} manufacturer_id: {self.manufacturer}"
