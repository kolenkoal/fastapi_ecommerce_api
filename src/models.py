import uuid
from datetime import datetime
from typing import Annotated

from fastapi_users_db_sqlalchemy import GUID, UUID_ID
from sqlalchemy import text
from sqlalchemy.orm import mapped_column

from src.database import str_256


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

uuidpk = Annotated[
    UUID_ID,
    mapped_column(GUID, primary_key=True, default=uuid.uuid4, unique=True),
]

uuidpk_not_unique = Annotated[
    UUID_ID,
    mapped_column(GUID, primary_key=True, default=uuid.uuid4, unique=False),
]

str256 = Annotated[str_256, mapped_column(nullable=False)]
