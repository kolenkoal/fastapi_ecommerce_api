"""Changed payment method id field

Revision ID: b2741ccf7568
Revises: 90f5cce3a711
Create Date: 2024-02-23 08:39:31.072424

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b2741ccf7568"
down_revision: Union[str, None] = "90f5cce3a711"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "order_lines", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "order_lines", type_="unique")
    # ### end Alembic commands ###
