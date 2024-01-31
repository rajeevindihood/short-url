from ._base import Base
from sqlalchemy import BLOB, Column, Enum, Integer, String, func, DateTime


class Client(Base):
    __tablename__ = "journey_client"
    id = Column(Integer(), primary_key=True)
    name = Column(String(length=100))
    domain = Column(String(length=100))
    pg_type = Column(
        Enum(
            "RAZORPAY",
            "BILLDESK",
            "NEFT",
            "CASHFREE",
            "DKGFS",
            "APP-REDIRECT",
            "SL-REDIRECT",
            "ZP-REDIRECT",
        )
    )
    contact_name = Column(String(length=100))
    contact_phone = Column(String(length=100))
    contact_email = Column(String(length=100))
    logo = Column(BLOB)
    created_by = Column(String(length=100))
    category = Column(Enum("NBFC", "CC", "BNPL", "BOFFER", "OFFER", "OFFER_LOAN"))
    creation_date = Column(DateTime(), server_default=func.now())
    last_update_time = Column(DateTime(), server_default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
