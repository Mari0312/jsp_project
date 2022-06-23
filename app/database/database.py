from typing import Type

from sqlalchemy import Column, Integer, update
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config as config

db_string = config.SQLALCHEMY_DATABASE_URI

db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()


class ModelBase:

    def __init__(self, *args, **kwargs):
        pass

    def save(self) -> 'Base':
        session.add(self)
        session.commit()
        return self

    @classmethod
    def get(cls, id) -> 'ModelBase':
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def list(cls, offset, limit):
        return session.query(cls).order_by(cls.id).offset(offset).limit(limit)

    @classmethod
    def delete(cls, id):
        return session.query(cls).filter_by(id=id).delete()

    @classmethod
    def update(cls, id, **parameters):
        return session.execute(update(cls).where(cls.id == id).values(**parameters))


Base: Type[ModelBase] = declarative_base(cls=ModelBase)
