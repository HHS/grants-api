"""add expanded opportunity models

Revision ID: 8d2a88569e7e
Revises: 479221fb8ba8
Create Date: 2024-02-07 12:16:16.564629

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8d2a88569e7e"
down_revision = "479221fb8ba8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lk_applicant_type",
        sa.Column("applicant_type_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
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
        sa.PrimaryKeyConstraint("applicant_type_id", name=op.f("lk_applicant_type_pkey")),
        schema="api",
    )
    op.create_table(
        "lk_funding_category",
        sa.Column("funding_category_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
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
        sa.PrimaryKeyConstraint("funding_category_id", name=op.f("lk_funding_category_pkey")),
        schema="api",
    )
    op.create_table(
        "lk_funding_instrument",
        sa.Column("funding_instrument_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
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
        sa.PrimaryKeyConstraint("funding_instrument_id", name=op.f("lk_funding_instrument_pkey")),
        schema="api",
    )
    op.create_table(
        "lk_opportunity_status",
        sa.Column("opportunity_status_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
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
        sa.PrimaryKeyConstraint("opportunity_status_id", name=op.f("lk_opportunity_status_pkey")),
        schema="api",
    )
    op.create_table(
        "link_applicant_type_opportunity",
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("applicant_type_id", sa.Integer(), nullable=False),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["applicant_type_id"],
            ["api.lk_applicant_type.applicant_type_id"],
            name=op.f("link_applicant_type_opportunity_applicant_type_id_lk_applicant_type_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["api.opportunity.opportunity_id"],
            name=op.f("link_applicant_type_opportunity_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_id", "applicant_type_id", name=op.f("link_applicant_type_opportunity_pkey")
        ),
        schema="api",
    )
    op.create_table(
        "link_funding_category_opportunity",
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("funding_category_id", sa.Integer(), nullable=False),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["funding_category_id"],
            ["api.lk_funding_category.funding_category_id"],
            name=op.f(
                "link_funding_category_opportunity_funding_category_id_lk_funding_category_fkey"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["api.opportunity.opportunity_id"],
            name=op.f("link_funding_category_opportunity_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_id",
            "funding_category_id",
            name=op.f("link_funding_category_opportunity_pkey"),
        ),
        schema="api",
    )
    op.create_table(
        "link_funding_instrument_opportunity",
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("funding_instrument_id", sa.Integer(), nullable=False),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["funding_instrument_id"],
            ["api.lk_funding_instrument.funding_instrument_id"],
            name=op.f(
                "link_funding_instrument_opportunity_funding_instrument_id_lk_funding_instrument_fkey"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["api.opportunity.opportunity_id"],
            name=op.f("link_funding_instrument_opportunity_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_id",
            "funding_instrument_id",
            name=op.f("link_funding_instrument_opportunity_pkey"),
        ),
        schema="api",
    )
    op.create_table(
        "opportunity_assistance_listing",
        sa.Column("opportunity_assistance_listing_id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("program_title", sa.Text(), nullable=True),
        sa.Column("assistance_listing_number", sa.Text(), nullable=True),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["opportunity_id"],
            ["api.opportunity.opportunity_id"],
            name=op.f("opportunity_assistance_listing_opportunity_id_opportunity_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_assistance_listing_id", name=op.f("opportunity_assistance_listing_pkey")
        ),
        schema="api",
    )
    op.create_index(
        op.f("opportunity_assistance_listing_opportunity_id_idx"),
        "opportunity_assistance_listing",
        ["opportunity_id"],
        unique=False,
        schema="api",
    )
    op.create_table(
        "opportunity_summary",
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("opportunity_status_id", sa.Integer(), nullable=True),
        sa.Column("summary_description", sa.Text(), nullable=True),
        sa.Column("is_cost_sharing", sa.Boolean(), nullable=True),
        sa.Column("close_date", sa.Date(), nullable=True),
        sa.Column("close_date_description", sa.Text(), nullable=True),
        sa.Column("post_date", sa.Date(), nullable=True),
        sa.Column("archive_date", sa.Date(), nullable=True),
        sa.Column("unarchive_date", sa.Date(), nullable=True),
        sa.Column("expected_number_of_awards", sa.Integer(), nullable=True),
        sa.Column("estimated_total_program_funding", sa.Integer(), nullable=True),
        sa.Column("award_floor", sa.Integer(), nullable=True),
        sa.Column("award_ceiling", sa.Integer(), nullable=True),
        sa.Column("additional_info_url", sa.Text(), nullable=True),
        sa.Column("additional_info_url_description", sa.Text(), nullable=True),
        sa.Column("version_number", sa.Integer(), nullable=True),
        sa.Column("modification_comments", sa.Text(), nullable=True),
        sa.Column("funding_category_description", sa.Text(), nullable=True),
        sa.Column("applicant_eligibility_description", sa.Text(), nullable=True),
        sa.Column("agency_code", sa.Text(), nullable=True),
        sa.Column("agency_name", sa.Text(), nullable=True),
        sa.Column("agency_phone_number", sa.Text(), nullable=True),
        sa.Column("agency_contact_description", sa.Text(), nullable=True),
        sa.Column("agency_email_address", sa.Text(), nullable=True),
        sa.Column("agency_email_address_description", sa.Text(), nullable=True),
        sa.Column("can_send_mail", sa.Boolean(), nullable=True),
        sa.Column("publisher_profile_id", sa.Integer(), nullable=True),
        sa.Column("publisher_user_id", sa.Text(), nullable=True),
        sa.Column("updated_by", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Text(), nullable=True),
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
            ["opportunity_id"],
            ["api.opportunity.opportunity_id"],
            name=op.f("opportunity_summary_opportunity_id_opportunity_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_status_id"],
            ["api.lk_opportunity_status.opportunity_status_id"],
            name=op.f("opportunity_summary_opportunity_status_id_lk_opportunity_status_fkey"),
        ),
        sa.PrimaryKeyConstraint("opportunity_id", name=op.f("opportunity_summary_pkey")),
        schema="api",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("opportunity_summary", schema="api")
    op.drop_index(
        op.f("opportunity_assistance_listing_opportunity_id_idx"),
        table_name="opportunity_assistance_listing",
        schema="api",
    )
    op.drop_table("opportunity_assistance_listing", schema="api")
    op.drop_table("link_funding_instrument_opportunity", schema="api")
    op.drop_table("link_funding_category_opportunity", schema="api")
    op.drop_table("link_applicant_type_opportunity", schema="api")
    op.drop_table("lk_opportunity_status", schema="api")
    op.drop_table("lk_funding_instrument", schema="api")
    op.drop_table("lk_funding_category", schema="api")
    op.drop_table("lk_applicant_type", schema="api")
    # ### end Alembic commands ###
