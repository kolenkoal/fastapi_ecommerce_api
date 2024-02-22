"""Added shopping cart model

Revision ID: c6b3b34773d1
Revises: 89f21471607f
Create Date: 2024-02-19 13:59:04.519761

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c6b3b34773d1"
down_revision: Union[str, None] = "89f21471607f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "shopping_carts",
        sa.Column(
            "id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False
        ),
        sa.Column(
            "user_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shopping_carts")
    # ### end Alembic commands ###