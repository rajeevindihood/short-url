from sqlalchemy.orm import relationship
from ._base import Base
from datetime import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Enum,
    Text,
)


class Tranch(Base):
    __tablename__ = "journey_tranch"
    __table_args__ = (Index("journey_tranch_client_id_7b9ec4ba", "client_id"),)
    id = Column(Integer(), primary_key=True)
    name = Column(String(length=64))
    secret_id = Column(String(length=100))
    client_id = Column(
        Integer(),
        ForeignKey(
            column="journey_client.id",
            initially="DEFERRED",
            # ondelete="CASCADE",
        ),
    )
    created_on = Column(DateTime(), default=datetime.now())
    campaign_type = Column(Enum("EMI", "SETTLEMENT"))
    enable_emi_payment = Column(Boolean(), default=False)
    enable_emi_payment_date = Column(DateTime())
    enable_liveassist = Column(Boolean(), default=False)
    is_gupshupenabled = Column(Boolean(), default=False)
    created_by = Column(String(length=30))

    # additional_features = Column(JSON)
    client = relationship("Client")

    is_enabled = Column(Boolean, default=False)
    telecalling_strategy = Column(Text)
    tranch_type = Column(String(30))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
