from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import mapped_column


uuidpk = Annotated[
    UUID,
    mapped_column(
        primary_key=True, index=True, nullable=False, default_factory=uuid4
    ),
]
created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now() + interval '1 day')"),
        onupdate=datetime.utcnow,
    ),
]
