from datetime import datetime
from email.policy import default

from importlib import import_module
import enum
from unittest.mock import DEFAULT

from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    BigInteger,
    String,
    DateTime,
    Date,
    Time,
    Text,
    Sequence,
    Enum,
    JSON,
    BLOB, FLOAT
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import FetchedValue
from sqlalchemy.sql.sqltypes import VARCHAR
# from sqlalchemy.sql.sqltypes import BLOB, BOOLEAN, Float, JSON
Base = declarative_base()

class Client(Base):
    __tablename__ = "journey_client"
    id = Column(Integer(), primary_key=True)
    name=Column(String(length=100))
    domain=Column(String(length=100))
    pg_type = Column(Enum('RAZORPAY','BILLDESK','NEFT','CASHFREE','DKGFS','APP-REDIRECT','SL-REDIRECT','ZP-REDIRECT'))
    contact_name=Column(String(length=100))
    contact_phone=Column(String(length=100))
    contact_email=Column(String(length=100))
    logo=Column(BLOB)
    created_by=Column(String(length=100))
    category=Column(Enum('NBFC','CC','BNPL'))
    creation_date=Column(DateTime(),server_default=func.now())
    last_update_time=Column(DateTime(),server_default=func.now())
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Tranch(Base):
    __tablename__ = "journey_tranch"
    id = Column(Integer(), primary_key=True)
    name = Column(String(length=64))
    client_id = Column(Integer(), ForeignKey(column="journey_client.id", ondelete="CASCADE"))
    created_on = Column(DateTime(),default=datetime.now())
    campaign_type = Column(Enum('EMI','SETTLEMENT'))
    enable_emi_payment = Column(Boolean(), default=False)
    enable_emi_payment_date = Column(DateTime())
    enable_liveassist = Column(Boolean(), default=False)
    is_gupshupenabled  = Column(Boolean(),default=False)
    created_by=Column(String(length=30))


    # additional_features = Column(JSON)
    client = relationship ("Client")

    is_enabled = Column(Boolean, default=False) 
    telecalling_strategy=Column(Text)


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Hash(Base):
    __tablename__ = "hash_keys"
    id = Column(Integer(), primary_key=True)
    original_key=Column(String(length=255), unique=True)
    hash_key=Column(String(length=8), unique=True)
    creation_date=Column(DateTime(),server_default=func.now(), default=func.now())
    last_visiting_time=Column(DateTime())
    is_enabled = Column(Boolean, default=True)
    tranch_id = Column(Integer(),ForeignKey(column="journey_tranch.id"))
    expiry_date=Column(DateTime())
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Borrower(Base):
    __tablename__ = "journey_borrower"
    id = Column(
        Integer(), primary_key=True, unique=True, nullable=False, autoincrement=True
    )

   
    canpebid = Column(String(length=255))
    opportunity_name = Column(String(length=255))
    sms_short_link = Column(String(length=32),default=None)
    total_outstanding_payment_link=Column(String(length=100))
    tranch_id = Column(Integer(),ForeignKey(column="journey_tranch.id"))



    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


