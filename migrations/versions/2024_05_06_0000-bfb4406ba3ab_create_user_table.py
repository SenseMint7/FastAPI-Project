"""create user table

Revision ID: bfb4406ba3ab
Revises:
Create Date: 2024-05-06 00:00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bfb4406ba3ab"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    def get_current_tables(op):
        conn = op.get_bind()
        inspector = sa.Inspector.from_engine(conn)
        return inspector.get_table_names()

    tables = get_current_tables(op)
    if "user" not in tables:
        op.create_table(
            "user",
            sa.Column("id", sa.Integer, primary_key=True, autoincrement="auto"),
            sa.Column("fullname", sa.VARCHAR(100), nullable=False),
            sa.Column(
                "email", sa.VARCHAR(100), index=True, nullable=False, unique=True
            ),
            sa.Column("password", sa.VARCHAR(255), nullable=False),
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
    op.drop_table("user")
