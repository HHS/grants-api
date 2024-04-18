#
# SQLAlchemy models for foreign tables.
#

import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import base


class Topportunity(base.Base):
    __tablename__ = "topportunity"

    opportunity_id: Mapped[int] = mapped_column(primary_key=True)
    oppnumber: Mapped[str | None]
    revision_number: Mapped[int | None]
    opptitle: Mapped[str | None]
    owningagency: Mapped[str | None]
    publisheruid: Mapped[str | None]
    listed: Mapped[str | None]
    oppcategory: Mapped[str | None]
    initial_opportunity_id: Mapped[int | None]
    modified_comments: Mapped[str | None]
    created_date: Mapped[datetime.datetime]
    last_upd_date: Mapped[datetime.datetime]
    creator_id: Mapped[str | None]
    last_upd_id: Mapped[str | None]
    flag_2006: Mapped[str | None]
    category_explanation: Mapped[str | None]
    publisher_profile_id: Mapped[int | None]
    is_draft: Mapped[str | None]


class TopportunityCfda(base.Base):
    __tablename__ = "topportunity_cfda"

    programtitle: Mapped[str | None]
    origtoppid: Mapped[int | None]
    origoppnum: Mapped[str | None]
    opp_cfda_id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[int]
    oppidcfdanum: Mapped[str | None]
    last_upd_id: Mapped[str | None]
    last_upd_date: Mapped[datetime.datetime | None]
    creator_id: Mapped[str | None]
    created_date: Mapped[datetime.datetime | None]
    cfdanumber: Mapped[str | None]
