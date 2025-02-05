import uuid
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship, make_transient_to_detached, make_transient

from src.adapters.db.type_decorators.postgres_type_decorators import LookupColumn
from src.constants.lookup_constants import (
    ApplicantType,
    FundingCategory,
    FundingInstrument,
    OpportunityAttachmentType,
    OpportunityCategory,
    OpportunityStatus,
)
from src.db.models.agency_models import Agency
from src.db.models.base import ApiSchemaTable, TimestampMixin, VersionMixin
from src.db.models.lookup_models import (
    LkApplicantType,
    LkFundingCategory,
    LkFundingInstrument,
    LkOpportunityAttachmentType,
    LkOpportunityCategory,
    LkOpportunityStatus,
)

if TYPE_CHECKING:
    from src.db.models.user_models import UserSavedOpportunity


class Opportunity(ApiSchemaTable, TimestampMixin):
    __tablename__ = "opportunity"

    opportunity_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    opportunity_number: Mapped[str | None]
    opportunity_title: Mapped[str | None] = mapped_column(index=True)
    agency_code: Mapped[str | None] = mapped_column(index=True)

    @property
    def agency(self) -> str | None:
        # TODO - this is temporary until the frontend no longer needs this name
        return self.agency_code

    category: Mapped[OpportunityCategory | None] = mapped_column(
        "opportunity_category_id",
        LookupColumn(LkOpportunityCategory),
        ForeignKey(LkOpportunityCategory.opportunity_category_id),
        index=True,
    )
    category_explanation: Mapped[str | None]

    is_draft: Mapped[bool] = mapped_column(index=True)

    revision_number: Mapped[int | None]
    modified_comments: Mapped[str | None]

    # These presumably refer to the TUSER_ACCOUNT, and TUSER_PROFILE tables
    # although the legacy DB does not have them setup as foreign keys
    publisher_user_id: Mapped[str | None]
    publisher_profile_id: Mapped[int | None] = mapped_column(BigInteger)

    opportunity_attachments: Mapped[list["OpportunityAttachment"]] = relationship(
        back_populates="opportunity", uselist=True, cascade="all, delete-orphan"
    )

    opportunity_assistance_listings: Mapped[list["OpportunityAssistanceListing"]] = relationship(
        back_populates="opportunity", uselist=True, cascade="all, delete-orphan"
    )

    opportunity_change_audit: Mapped["OpportunityChangeAudit | None"] = relationship(
        back_populates="opportunity", single_parent=True, cascade="all, delete-orphan"
    )

    current_opportunity_summary: Mapped["CurrentOpportunitySummary | None"] = relationship(
        back_populates="opportunity", single_parent=True, cascade="all, delete-orphan"
    )

    all_opportunity_summaries: Mapped[list["OpportunitySummary"]] = relationship(
        back_populates="opportunity", uselist=True, cascade="all, delete-orphan"
    )

    saved_opportunities_by_users: Mapped[list["UserSavedOpportunity"]] = relationship(
        "UserSavedOpportunity",
        back_populates="opportunity",
        uselist=True,
        cascade="all, delete-orphan",
    )

    agency_record: Mapped[Agency | None] = relationship(
        Agency,
        primaryjoin="Opportunity.agency_code == foreign(Agency.agency_code)",
        uselist=False,
        viewonly=True,
    )

    @property
    def top_level_agency_name(self) -> str | None:
        if self.agency_record is not None and self.agency_record.top_level_agency is not None:
            return self.agency_record.top_level_agency.agency_name

        return None

    @property
    def agency_name(self) -> str | None:
        # Fetch the agency name from the agency table record (if one was found)
        if self.agency_record is not None:
            return self.agency_record.agency_name

        return None

    @property
    def summary(self) -> "OpportunitySummary | None":
        """
        Utility getter method for converting an Opportunity in our endpoints

        This handles mapping the current opportunity summary to the "summary" object
         in our API responses - handling nullablity as well.
        """
        if self.current_opportunity_summary is None:
            return None

        return self.current_opportunity_summary.opportunity_summary

    @property
    def opportunity_status(self) -> OpportunityStatus | None:
        if self.current_opportunity_summary is None:
            return None

        return self.current_opportunity_summary.opportunity_status

    @property
    def all_forecasts(self) -> list["OpportunitySummary"]:
        # Utility method for getting all forecasted summary records attached to the opportunity
        # Note this will include historical and deleted records.
        return [summary for summary in self.all_opportunity_summaries if summary.is_forecast]

    @property
    def all_non_forecasts(self) -> list["OpportunitySummary"]:
        # Utility method for getting all forecasted summary records attached to the opportunity
        # Note this will include historical and deleted records.
        return [summary for summary in self.all_opportunity_summaries if not summary.is_forecast]


class OpportunitySummary(ApiSchemaTable, TimestampMixin):
    __tablename__ = "opportunity_summary"

    __table_args__ = (
        # nulls not distinct makes it so nulls work in the unique constraint
        UniqueConstraint(
            "is_forecast", "revision_number", "opportunity_id", postgresql_nulls_not_distinct=True
        ),
        # Need to define the table args like this to inherit whatever we set on the super table
        # otherwise we end up overwriting things and Alembic remakes the whole table
        ApiSchemaTable.__table_args__,
    )

    opportunity_summary_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    opportunity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(Opportunity.opportunity_id), index=True
    )
    opportunity: Mapped[Opportunity] = relationship(Opportunity)

    summary_description: Mapped[str | None]

    is_cost_sharing: Mapped[bool | None]
    is_forecast: Mapped[bool]

    post_date: Mapped[date | None]
    close_date: Mapped[date | None]
    close_date_description: Mapped[str | None]
    archive_date: Mapped[date | None]
    unarchive_date: Mapped[date | None]

    # The award amounts can be for several billion requiring us to use BigInteger
    expected_number_of_awards: Mapped[int | None] = mapped_column(BigInteger)
    estimated_total_program_funding: Mapped[int | None] = mapped_column(BigInteger)
    award_floor: Mapped[int | None] = mapped_column(BigInteger)
    award_ceiling: Mapped[int | None] = mapped_column(BigInteger)

    additional_info_url: Mapped[str | None]
    additional_info_url_description: Mapped[str | None]

    # Only if the summary is forecasted
    forecasted_post_date: Mapped[date | None]
    forecasted_close_date: Mapped[date | None]
    forecasted_close_date_description: Mapped[str | None]
    forecasted_award_date: Mapped[date | None]
    forecasted_project_start_date: Mapped[date | None]
    fiscal_year: Mapped[int | None]

    revision_number: Mapped[int | None]
    modification_comments: Mapped[str | None]

    funding_category_description: Mapped[str | None]
    applicant_eligibility_description: Mapped[str | None]

    agency_phone_number: Mapped[str | None]
    agency_contact_description: Mapped[str | None]
    agency_email_address: Mapped[str | None]
    agency_email_address_description: Mapped[str | None]

    is_deleted: Mapped[bool | None]

    version_number: Mapped[int | None]
    can_send_mail: Mapped[bool | None]
    publisher_profile_id: Mapped[int | None] = mapped_column(BigInteger)
    publisher_user_id: Mapped[str | None]
    updated_by: Mapped[str | None]
    created_by: Mapped[str | None]

    # Do not use these agency fields, they're kept for now, but
    # are simply copying behavior from the legacy system - prefer
    # the same named values in the opportunity itself
    agency_code: Mapped[str | None]
    agency_name: Mapped[str | None]

    link_funding_instruments: Mapped[list["LinkOpportunitySummaryFundingInstrument"]] = (
        relationship(
            back_populates="opportunity_summary", uselist=True, cascade="all, delete-orphan"
        )
    )
    link_funding_categories: Mapped[list["LinkOpportunitySummaryFundingCategory"]] = relationship(
        back_populates="opportunity_summary", uselist=True, cascade="all, delete-orphan"
    )
    link_applicant_types: Mapped[list["LinkOpportunitySummaryApplicantType"]] = relationship(
        back_populates="opportunity_summary", uselist=True, cascade="all, delete-orphan"
    )

    # Create an association proxy for each of the link table relationships
    # https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html
    #
    # This lets us use these values as if they were just ordinary lists on a python
    # object. For example::
    #
    #   opportunity.funding_instruments.add(FundingInstrument.GRANT)
    #
    # will add a row to the link_opportunity_summary_funding_instrument table itself
    # and is still capable of using all of our column mapping code uneventfully.
    funding_instruments: AssociationProxy[set[FundingInstrument]] = association_proxy(
        "link_funding_instruments",
        "funding_instrument",
        creator=lambda obj: LinkOpportunitySummaryFundingInstrument(funding_instrument=obj),
    )
    funding_categories: AssociationProxy[set[FundingCategory]] = association_proxy(
        "link_funding_categories",
        "funding_category",
        creator=lambda obj: LinkOpportunitySummaryFundingCategory(funding_category=obj),
    )
    applicant_types: AssociationProxy[set[ApplicantType]] = association_proxy(
        "link_applicant_types",
        "applicant_type",
        creator=lambda obj: LinkOpportunitySummaryApplicantType(applicant_type=obj),
    )

    # We configure a relationship from a summary to the current opportunity summary
    # Just in case we delete this record, we can cascade to deleting the current_opportunity_summary
    # record as well automatically.
    current_opportunity_summary: Mapped["CurrentOpportunitySummary | None"] = relationship(
        back_populates="opportunity_summary", single_parent=True, cascade="delete"
    )

    def for_json(self) -> dict:
        json_valid_dict = super().for_json()

        # The proxy values don't end up in the JSON as they aren't columns
        # so manually add them.
        json_valid_dict["funding_instruments"] = self.funding_instruments
        json_valid_dict["funding_categories"] = self.funding_categories
        json_valid_dict["applicant_types"] = self.applicant_types

        return json_valid_dict

    def can_summary_be_public(self, current_date: date) -> bool:
        """
        Utility method to check whether a summary object
        """
        if self.is_deleted:
            return False

        if self.post_date is None or self.post_date > current_date:
            return False

        return True


class OpportunityAssistanceListing(ApiSchemaTable, TimestampMixin):
    __tablename__ = "opportunity_assistance_listing"

    opportunity_assistance_listing_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    opportunity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(Opportunity.opportunity_id), index=True
    )
    opportunity: Mapped[Opportunity] = relationship(Opportunity)

    assistance_listing_number: Mapped[str | None]
    program_title: Mapped[str | None]

    updated_by: Mapped[str | None]
    created_by: Mapped[str | None]


class LinkOpportunitySummaryFundingInstrument(ApiSchemaTable, TimestampMixin):
    __tablename__ = "link_opportunity_summary_funding_instrument"

    __table_args__ = (
        # We want a unique constraint so that legacy IDs are unique for a given opportunity summary
        UniqueConstraint("opportunity_summary_id", "legacy_funding_instrument_id"),
        # Need to define the table args like this to inherit whatever we set on the super table
        # otherwise we end up overwriting things and Alembic remakes the whole table
        ApiSchemaTable.__table_args__,
    )

    opportunity_summary_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(OpportunitySummary.opportunity_summary_id),
        primary_key=True,
        index=True,
    )
    opportunity_summary: Mapped[OpportunitySummary] = relationship(OpportunitySummary)

    funding_instrument: Mapped[FundingInstrument] = mapped_column(
        "funding_instrument_id",
        LookupColumn(LkFundingInstrument),
        ForeignKey(LkFundingInstrument.funding_instrument_id),
        primary_key=True,
        index=True,
    )

    legacy_funding_instrument_id: Mapped[int | None]

    updated_by: Mapped[str | None]
    created_by: Mapped[str | None]


class LinkOpportunitySummaryFundingCategory(ApiSchemaTable, TimestampMixin):
    __tablename__ = "link_opportunity_summary_funding_category"

    __table_args__ = (
        # We want a unique constraint so that legacy IDs are unique for a given opportunity summary
        UniqueConstraint("opportunity_summary_id", "legacy_funding_category_id"),
        # Need to define the table args like this to inherit whatever we set on the super table
        # otherwise we end up overwriting things and Alembic remakes the whole table
        ApiSchemaTable.__table_args__,
    )

    opportunity_summary_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(OpportunitySummary.opportunity_summary_id),
        primary_key=True,
        index=True,
    )
    opportunity_summary: Mapped[OpportunitySummary] = relationship(OpportunitySummary)

    funding_category: Mapped[FundingCategory] = mapped_column(
        "funding_category_id",
        LookupColumn(LkFundingCategory),
        ForeignKey(LkFundingCategory.funding_category_id),
        primary_key=True,
        index=True,
    )

    legacy_funding_category_id: Mapped[int | None]

    updated_by: Mapped[str | None]
    created_by: Mapped[str | None]


class LinkOpportunitySummaryApplicantType(ApiSchemaTable, TimestampMixin):
    __tablename__ = "link_opportunity_summary_applicant_type"

    __table_args__ = (
        # We want a unique constraint so that legacy IDs are unique for a given opportunity summary
        UniqueConstraint("opportunity_summary_id", "legacy_applicant_type_id"),
        # Need to define the table args like this to inherit whatever we set on the super table
        # otherwise we end up overwriting things and Alembic remakes the whole table
        ApiSchemaTable.__table_args__,
    )

    opportunity_summary_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(OpportunitySummary.opportunity_summary_id),
        primary_key=True,
        index=True,
    )
    opportunity_summary: Mapped[OpportunitySummary] = relationship(OpportunitySummary)

    applicant_type: Mapped[ApplicantType] = mapped_column(
        "applicant_type_id",
        LookupColumn(LkApplicantType),
        ForeignKey(LkApplicantType.applicant_type_id),
        primary_key=True,
        index=True,
    )

    legacy_applicant_type_id: Mapped[int | None]

    updated_by: Mapped[str | None]
    created_by: Mapped[str | None]


class CurrentOpportunitySummary(ApiSchemaTable, TimestampMixin):
    __tablename__ = "current_opportunity_summary"

    opportunity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(Opportunity.opportunity_id), primary_key=True, index=True
    )
    opportunity: Mapped[Opportunity] = relationship(single_parent=True)

    opportunity_summary_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(OpportunitySummary.opportunity_summary_id),
        primary_key=True,
        index=True,
    )
    opportunity_summary: Mapped[OpportunitySummary] = relationship(single_parent=True)

    opportunity_status: Mapped[OpportunityStatus] = mapped_column(
        "opportunity_status_id",
        LookupColumn(LkOpportunityStatus),
        ForeignKey(LkOpportunityStatus.opportunity_status_id),
        index=True,
    )


class OpportunityAttachment(ApiSchemaTable, TimestampMixin):
    __tablename__ = "opportunity_attachment"

    attachment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    opportunity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(Opportunity.opportunity_id), index=True
    )
    opportunity: Mapped[Opportunity] = relationship(Opportunity)
    opportunity_attachment_type: Mapped[OpportunityAttachmentType] = mapped_column(
        "opportunity_attachment_type_id",
        LookupColumn(LkOpportunityAttachmentType),
        ForeignKey(LkOpportunityAttachmentType.opportunity_attachment_type_id),
        index=True,
    )

    file_location: Mapped[str]
    mime_type: Mapped[str]
    file_name: Mapped[str]
    file_description: Mapped[str]
    file_size_bytes: Mapped[int] = mapped_column(BigInteger)
    created_by: Mapped[str | None]
    updated_by: Mapped[str | None]
    legacy_folder_id: Mapped[int | None] = mapped_column(BigInteger)


class OpportunityChangeAudit(ApiSchemaTable, TimestampMixin):
    __tablename__ = "opportunity_change_audit"

    opportunity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(Opportunity.opportunity_id), primary_key=True, index=True
    )
    opportunity: Mapped[Opportunity] = relationship(Opportunity)


class Parent(ApiSchemaTable, TimestampMixin, VersionMixin):
    __tablename__ = "parent"

    __table_args__ = (
        # nulls not distinct makes it so nulls work in the unique constraint
        UniqueConstraint(
            "opportunity_id", "end", postgresql_nulls_not_distinct=True
        ),
        # Need to define the table args like this to inherit whatever we set on the super table
        # otherwise we end up overwriting things and Alembic remakes the whole table
        ApiSchemaTable.__table_args__,
    )


    parent_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)

    # TODO - while we need the legacy opportunity ID, should we make a table
    #        that maps legacy IDs to UUIDs and use that instead?
    opportunity_id: Mapped[int] = mapped_column(index=True)

    title: Mapped[str]

    other_field: Mapped[str | None]

    all_children: Mapped[list["Child"]] = relationship(
        back_populates="parent", uselist=True, cascade="all, delete-orphan",
        primaryjoin="Parent.opportunity_id == foreign(Child.opportunity_id)",
    )


    # We configure a relationship from a summary to the current opportunity summary
    # Just in case we delete this record, we can cascade to deleting the current_opportunity_summary
    # record as well automatically.
    current_child: Mapped["CurrentChild | None"] = relationship(
        back_populates="parent", single_parent=True, cascade="delete"
    )

    def new_version(self, db_session):
        prior_current_child = self.current_child
        VersionMixin.new_version(self, db_session)

        # This automatically moves the current_opportunity_summary
        # to point to the new opportunity we just made.
        if prior_current_child is not None:
            new_current_child = CurrentChild(parent=self, child=prior_current_child.child, opportunity_status=prior_current_child.opportunity_status)
            db_session.add(new_current_child)
            db_session.delete(prior_current_child)

class ParentAssistanceListing(ApiSchemaTable, TimestampMixin):
    __tablename__ = "parent_assistance_listing"

    parent_assistance_listing_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)

    parent_id: Mapped[int] = mapped_column(
        UUID, ForeignKey(Parent.parent_id), primary_key=True, index=True
    )
    parent: Mapped[Parent] = relationship(single_parent=True)

    assistance_listing_number: Mapped[str]


class Child(ApiSchemaTable, TimestampMixin, VersionMixin):
    __tablename__ = "child"

    __table_args__ = (
        # nulls not distinct makes it so nulls work in the unique constraint
        UniqueConstraint(
            "opportunity_id", "is_forecast", "end", postgresql_nulls_not_distinct=True
        ),
        # Need to define the table args like this to inherit whatever we set on the super table
        # otherwise we end up overwriting things and Alembic remakes the whole table
        ApiSchemaTable.__table_args__,
    )

    child_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)

    opportunity_id: Mapped[int] = mapped_column(index=True)

    is_forecast: Mapped[bool] = mapped_column(index=True)

    description: Mapped[str]

    parent: Mapped[Parent] = relationship(Parent, primaryjoin="and_(Child.opportunity_id == foreign(Parent.opportunity_id), Parent.end.is_(None))")


class CurrentChild(ApiSchemaTable, TimestampMixin):
    __tablename__ = "current_child"

    parent_id: Mapped[int] = mapped_column(
        UUID, ForeignKey(Parent.parent_id), primary_key=True, index=True
    )
    parent: Mapped[Parent] = relationship(single_parent=True)

    child_id: Mapped[int] = mapped_column(
        UUID,
        ForeignKey(Child.child_id),
        primary_key=True,
        index=True,
    )
    child: Mapped[Child] = relationship(single_parent=True)

    opportunity_status: Mapped[OpportunityStatus] = mapped_column(
        "opportunity_status_id",
        LookupColumn(LkOpportunityStatus),
        ForeignKey(LkOpportunityStatus.opportunity_status_id),
        index=True,
    )





# TODO
# * Current opportunity summary style logic (what happens when the IDs get changed? Can that be handled at least when the parent changes?)
# * Behavior of our one-to-many link tables - can we make them pretend to be versioned on the parent
# * Verify no weird behavior with our lk tables
