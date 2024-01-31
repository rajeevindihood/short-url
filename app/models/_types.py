from datetime import datetime
from typing import Annotated
from sqlalchemy import DateTime, String, func

from sqlalchemy.orm import mapped_column

IntPK = Annotated[int, mapped_column(primary_key=True)]
DateTimeTZ = Annotated[datetime, mapped_column(DateTime(timezone=True))]
DateTimeNowTZ = Annotated[
    datetime, mapped_column(DateTime(timezone=True), server_default=func.now())
]
StringNullable = Annotated[str, mapped_column(String(), nullable=True)]
