"""tmp

Revision ID: 314b6a199117
Revises: 43b179a7c92e
Create Date: 2025-02-06 12:33:42.124805

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "314b6a199117"
down_revision = "43b179a7c92e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "parent",
        sa.Column("parent_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_number", sa.Text(), nullable=True),
        sa.Column("opportunity_title", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("parent_id", name=op.f("parent_pkey")),
        schema="api",
    )
    op.create_index(
        op.f("parent_opportunity_title_idx"),
        "parent",
        ["opportunity_title"],
        unique=False,
        schema="api",
    )
    op.create_table(
        "parent_history",
        sa.Column("parent_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_number", sa.Text(), nullable=True),
        sa.Column("opportunity_title", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("version_id", sa.UUID(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("start", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("end", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("parent_id", "version_id", name=op.f("parent_history_pkey")),
        schema="api",
    )
    op.create_index(
        op.f("parent_history_opportunity_title_idx"),
        "parent_history",
        ["opportunity_title"],
        unique=False,
        schema="api",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("parent_history_opportunity_title_idx"), table_name="parent_history", schema="api"
    )
    op.drop_table("parent_history", schema="api")
    op.drop_index(op.f("parent_opportunity_title_idx"), table_name="parent", schema="api")
    op.drop_table("parent", schema="api")
    # ### end Alembic commands ###
