"""add_attachment_table_staging_and_foreign

Revision ID: 4a3e50aa3bd6
Revises: 6a23520d2c3c
Create Date: 2024-12-19 17:20:53.380134

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4a3e50aa3bd6"
down_revision = "6a23520d2c3c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tsynopsis_attachment",
        sa.Column("syn_att_id", sa.BigInteger(), nullable=False),
        sa.Column("opportunity_id", sa.BigInteger(), nullable=False),
        sa.Column("att_revision_number", sa.BigInteger(), nullable=True),
        sa.Column("att_type", sa.Text(), nullable=True),
        sa.Column("mime_type", sa.Text(), nullable=True),
        sa.Column("link_url", sa.Text(), nullable=True),
        sa.Column("file_name", sa.Text(), nullable=True),
        sa.Column("file_desc", sa.Text(), nullable=True),
        sa.Column("file_lob", sa.LargeBinary(), nullable=True),
        sa.Column("file_lob_size", sa.BigInteger(), nullable=True),
        sa.Column("create_date", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("created_date", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("last_upd_date", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("creator_id", sa.Text(), nullable=True),
        sa.Column("last_upd_id", sa.Text(), nullable=True),
        sa.Column("syn_att_folder_id", sa.BigInteger(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("transformed_at", sa.TIMESTAMP(timezone=True), nullable=True),
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
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("transformation_notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("syn_att_id", name=op.f("tsynopsis_attachment_pkey")),
        schema="staging",
    )
    op.create_index(
        op.f("tsynopsis_attachment_transformed_at_idx"),
        "tsynopsis_attachment",
        ["transformed_at"],
        unique=False,
        schema="staging",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("tsynopsis_attachment_transformed_at_idx"),
        table_name="tsynopsis_attachment",
        schema="staging",
    )
    op.drop_table("tsynopsis_attachment", schema="staging")
    # ### end Alembic commands ###
