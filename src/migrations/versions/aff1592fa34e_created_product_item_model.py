"""Created product item model

Revision ID: aff1592fa34e
Revises: 4b17fc7d6ed2
Create Date: 2024-02-16 13:40:09.612402

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "aff1592fa34e"
down_revision: Union[str, None] = "4b17fc7d6ed2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product_items",
        sa.Column(
            "id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False
        ),
        sa.Column("SKU", sa.String(), nullable=False),
        sa.Column("quantity_in_stock", sa.Integer(), nullable=False),
        sa.Column("product_image", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column(
            "product_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["product_id"], ["products.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_unique_constraint(None, "products", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "products", type_="unique")
    op.drop_table("product_items")
    # ### end Alembic commands ###
