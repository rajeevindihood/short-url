from sqlalchemy.sql.functions import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hash(Base):
    __tablename__ = "hash_keys"
    id = Column(Integer(), primary_key=True)
    original_key=Column(String(length=255), unique=True)
    hash_key=Column(String(length=8), unique=True)
    creation_date=Column(DateTime(),server_default=func.now(), default=func.now())
    last_visiting_time=Column(DateTime())
    is_enabled = Column(Boolean, default=True)
    expiry_date=Column(DateTime())
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


