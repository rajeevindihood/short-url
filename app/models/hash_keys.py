"""
Owning Service: short-url
Repos: short-url
"""

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression
from ._base import Base
from ._types import IntPK
from sqlalchemy import (
    Boolean,
    DateTime,
    String,
    ForeignKey,
    UniqueConstraint,
)


class HashKey(Base):
    __tablename__ = "hash_keys"

    __table_args__ = (UniqueConstraint("hash_key", "original_key"),)

    id: Mapped[IntPK]
    original_key: Mapped[str] = mapped_column(String(255))
    hash_key: Mapped[str] = mapped_column(String(8))
    creation_date: Mapped[Optional[datetime]] = mapped_column(DateTime())
    tranch_id: Mapped[Optional[int]] = mapped_column(ForeignKey("journey_tranch.id"))
    last_visiting_time: Mapped[Optional[datetime]] = mapped_column(DateTime())
    is_enabled: Mapped[Optional[bool]] = mapped_column(
        Boolean(), server_default=expression.true()
    )
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime())
