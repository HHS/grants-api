"""Add last_notified_at to user saved opportunity table

Revision ID: 43b179a7c92e
Revises: dc04ce955a9a
Create Date: 2025-01-24 17:15:14.064880

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "43b179a7c92e"
down_revision = "9e7fc937646a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_saved_opportunity",
        sa.Column(
            "last_notified_at", sa.TIMESTAMP(timezone=True), server_default="NOW()", nullable=False
        ),
        schema="api",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_saved_opportunity", "last_notified_at", schema="api")
    # ### end Alembic commands ###
