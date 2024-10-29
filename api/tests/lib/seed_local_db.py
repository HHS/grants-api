import logging
import os
import pathlib
import random

import boto3
import click
from botocore.exceptions import ClientError
from sqlalchemy import func

import src.adapters.db as db
import src.logging
import src.util.datetime_util as datetime_util
import tests.src.db.models.factories as factories
from src.adapters.aws import S3Config, get_s3_client
from src.adapters.db import PostgresDBClient
from src.db.models.agency_models import Agency
from src.db.models.opportunity_models import Opportunity
from src.db.models.transfer.topportunity_models import TransferTopportunity
from src.util.local import error_if_not_local

logger = logging.getLogger(__name__)

TESTS_FOLDER = pathlib.Path(__file__).parent.resolve()


def _upload_opportunity_attachments_s3():
    s3_config = S3Config()
    s3_client = get_s3_client(
        s3_config, boto3.Session(aws_access_key_id="NO_CREDS", aws_secret_access_key="NO_CREDS")
    )
    test_folder_path = TESTS_FOLDER / "opportunity_attachment_test_files"

    for root, _, files in os.walk(test_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            object_name = os.path.relpath(file_path, test_folder_path)

            try:
                s3_client.upload_file(file_path, s3_config.s3_opportunity_bucket, object_name)
                logger.info("Successfully uploaded files")
            except ClientError as e:
                logger.error(
                    "Error uploading to s3: %s",
                    extra={"object_name": object_name, "file_path": file_path, "error": e},
                )


def _add_history(
    opps: list[Opportunity],
    add_forecast: bool = False,
    add_non_forecast: bool = False,
    add_forecast_hist: bool = False,
    add_non_forecast_hist: bool = False,
    is_history_deleted: bool = False,
):
    for opp in opps:
        builder = factories.OpportunitySummaryHistoryBuilder(opportunity=opp)

        if add_forecast:
            builder.add_forecast()

        if add_non_forecast:
            builder.add_non_forecast()

        if add_forecast_hist:
            for _ in range(random.randint(1, 3)):
                builder.add_forecast_history(
                    is_deleted=is_history_deleted, modification_comments="Modified forecast"
                )

        if add_non_forecast_hist:
            for _ in range(random.randint(1, 3)):
                builder.add_non_forecast_history(
                    is_deleted=is_history_deleted, modification_comments="Modified non-forecast"
                )

        builder.build()


def _build_opportunities(db_session: db.Session, iterations: int, include_history: bool) -> None:
    # Just create a variety of opportunities for local testing
    # we can eventually look into creating more specific scenarios
    for i in range(iterations):
        logger.info(f"Creating opportunity batch number {i}")
        # Create a few opportunities in various scenarios
        forecasted_opps = factories.OpportunityFactory.create_batch(
            size=5, is_forecasted_summary=True
        )
        posted_opps = factories.OpportunityFactory.create_batch(size=5, is_posted_summary=True)
        closed_opps = factories.OpportunityFactory.create_batch(size=5, is_closed_summary=True)
        archived_non_forecast_opps = factories.OpportunityFactory.create_batch(
            size=5, is_archived_non_forecast_summary=True
        )
        archived_forecast_opps = factories.OpportunityFactory.create_batch(
            size=5, is_archived_forecast_summary=True
        )
        no_current_summary_opps = factories.OpportunityFactory.create_batch(
            size=5, no_current_summary=True
        )

        if include_history:
            _add_history(forecasted_opps, add_forecast_hist=True)
            _add_history(
                posted_opps, add_non_forecast_hist=True, add_forecast=True, add_forecast_hist=True
            )
            _add_history(
                closed_opps, add_non_forecast_hist=True, add_forecast=True, add_forecast_hist=True
            )
            _add_history(
                archived_non_forecast_opps,
                add_non_forecast_hist=True,
                add_forecast=True,
                add_forecast_hist=True,
            )
            _add_history(archived_forecast_opps, add_forecast_hist=True)
            _add_history(no_current_summary_opps, is_history_deleted=True)

        # generate a few opportunities with mostly null values
        all_null_opportunities = factories.OpportunityFactory.create_batch(
            size=5, all_fields_null=True
        )
        for all_null_opportunity in all_null_opportunities:
            summary = factories.OpportunitySummaryFactory.create(
                # We  set post_date to something so that running the set-current-opportunities logic
                # won't get rid of it for having a null post date
                all_fields_null=True,
                opportunity=all_null_opportunity,
                post_date=datetime_util.get_now_us_eastern_date(),
            )
            factories.CurrentOpportunitySummaryFactory.create(
                opportunity=all_null_opportunity, opportunity_summary=summary
            )

    logger.info("Finished creating opportunities")

    logger.info("Creating records in the transfer_topportunity table")
    # Also seed the topportunity table for now in the same way
    max_opportunity_id = db_session.query(func.max(TransferTopportunity.opportunity_id)).scalar()
    if max_opportunity_id is None:
        max_opportunity_id = 0

    factories.TransferTopportunityFactory.reset_sequence(value=max_opportunity_id + 1)
    factories.TransferTopportunityFactory.create_batch(size=25)
    logger.info("Finished creating records in the transfer_topportunity table")


# Agencies we want to create locally - if we want to create significantly more
# we can consider shoving this into a CSV that we load instead.
AGENCIES_TO_CREATE = [
    {
        "agency_id": 1,
        "agency_code": "USAID",
        "agency_name": "Agency for International Development",
    },
    {
        "agency_id": 2,
        "agency_code": "ARPAH",
        "agency_name": "Advanced Research Projects Agency for Health",
    },
    {
        "agency_id": 3,
        "agency_code": "DOC",
        "agency_name": "Agency for International Development",
    },
    {
        "agency_id": 4,
        "agency_code": "DOC-EDA",
        "agency_name": "Agency for International Development",
        "top_level_agency_id": 3,  # DOC
    },
]


def _build_agencies(db_session: db.Session) -> None:
    # Create a static set of agencies, only if they don't already exist
    agencies = db_session.query(Agency).all()
    agency_codes = set([a.agency_code for a in agencies])

    for agency_to_create in AGENCIES_TO_CREATE:
        if agency_to_create["agency_code"] in agency_codes:
            continue

        logger.info("Creating agency %s in agency table", agency_to_create["agency_code"])
        factories.AgencyFactory.create(**agency_to_create)


@click.command()
@click.option(
    "--iterations",
    default=1,
    help="Number of sets of opportunities to create, note that several are created per iteration",
)
@click.option(
    "--include-history",
    is_flag=True,
    default=False,
    help="Whether to add historical records to the opportunities generated - much slower as this requires a lot more data to be generated",
)
def seed_local_db(iterations: int, include_history: bool) -> None:
    with src.logging.init("seed_local_db"):
        logger.info("Running seed script for local DB")
        error_if_not_local()

        _upload_opportunity_attachments_s3()
        #
        # db_client = PostgresDBClient()
        #
        # with db_client.get_session() as db_session:
        #     factories._db_session = db_session
        #
        #     _build_opportunities(db_session, iterations, include_history)
        #     # Need to commit to force any updates made
        #     # after factories created objects
        #     db_session.commit()
        #
        #     _build_agencies(db_session)
