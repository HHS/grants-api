"""user session table

Revision ID: 16eaca2334c9
Revises: 7346f6b52c3d
Create Date: 2024-11-18 13:10:37.039657

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "16eaca2334c9"
down_revision = "7346f6b52c3d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_token_session",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token_id", sa.UUID(), nullable=False),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("is_valid", sa.Boolean(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["user_id"], ["api.user.user_id"], name=op.f("user_token_session_user_id_user_fkey")
        ),
        sa.PrimaryKeyConstraint("user_id", "token_id", name=op.f("user_token_session_pkey")),
        schema="api",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_token_session", schema="api")
    # ### end Alembic commands ###
