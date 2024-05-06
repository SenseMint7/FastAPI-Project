"""create post table

Revision ID: da5a04713d04
Revises: 4db45887bbc1
Create Date: 2024-05-06 00:00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "108c0ff7ecd6"
down_revision: Union[str, None] = "4db45887bbc1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    def get_current_tables(op):
        conn = op.get_bind()
        inspector = sa.Inspector.from_engine(conn)
        return inspector.get_table_names()

    tables = get_current_tables(op)
    if "post" not in tables:
        op.create_table(
            "post",
            sa.Column("id", sa.Integer, primary_key=True, autoincrement="auto"),
            sa.Column("title", sa.VARCHAR(255), index=True),
            sa.Column("content", sa.Text),
            sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id")),
            sa.Column("board_id", sa.Integer, sa.ForeignKey("board.id")),
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
    op.drop_table("post")
