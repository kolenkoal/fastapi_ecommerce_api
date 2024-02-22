"""Added shipping method model

Revision ID: 4a90c4127d6a
Revises: 53afeed5974a
Create Date: 2024-02-22 15:57:52.564144

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4a90c4127d6a"
down_revision: Union[str, None] = "53afeed5974a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "shipping_methods",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint(None, "shopping_cart_items", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "shopping_cart_items", type_="unique")
    op.drop_table("shipping_methods")
    # ### end Alembic commands ###
