"""create_board_table

Revision ID: 4db45887bbc1
Revises: bfb4406ba3ab
Create Date: 2024-05-06 00:00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4db45887bbc1"
down_revision: Union[str, None] = "bfb4406ba3ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    def get_current_tables(op):
        conn = op.get_bind()
        inspector = sa.Inspector.from_engine(conn)
        return inspector.get_table_names()

    tables = get_current_tables(op)
    if "board" not in tables:
        op.create_table(
            "board",
            sa.Column("id", sa.Integer, primary_key=True, autoincrement="auto"),
            sa.Column("name", sa.VARCHAR(255), unique=True),
            sa.Column("public", sa.Boolean, nullable=False),
            sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), index=True),
            sa.Column(
                "created_dt", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_dt",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )


def downgrade() -> None:
    op.drop_table("board")
