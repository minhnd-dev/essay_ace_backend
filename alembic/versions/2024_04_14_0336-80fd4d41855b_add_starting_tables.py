"""add starting tables

Revision ID: 80fd4d41855b
Revises: 
Create Date: 2024-04-14 03:36:07.657225

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "80fd4d41855b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_name", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "responses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topics.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "feedbacks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("rewrite", sa.String(), nullable=False),
        sa.Column(
            "response_id",
            sa.Integer(),
            sa.ForeignKey("responses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("feedbacks")
    op.drop_table("responses")
    op.drop_table("topics")
    op.drop_table("users")
    # ### end Alembic commands ###
