from datetime import timedelta

import pytest

import tests.src.db.models.factories as factories
from src.db.models.user_models import UserNotificationLog
from src.task.notifications.generate_notifications import NotificationConstants
from src.util import datetime_util


@pytest.fixture
def clear_notification_logs(db_session):
    """Clear all notification logs"""
    db_session.query(UserNotificationLog).delete()


def test_via_cli(cli_runner, db_session, enable_factory_create, user):
    """Simple test that verifies we can invoke the notification task via CLI"""
    result = cli_runner.invoke(args=["task", "generate-notifications"])

    assert result.exit_code == 0


def test_collect_notifications_cli(cli_runner, db_session, enable_factory_create, user, caplog):
    """Simple test that verifies we can invoke the notification task via CLI"""
    # Create a saved opportunity that needs notification
    opportunity = factories.OpportunityFactory.create()
    saved_opportunity = factories.UserSavedOpportunityFactory.create(
        user=user,
        opportunity=opportunity,
        last_notified_at=opportunity.updated_at - timedelta(days=1),
    )
    factories.OpportunityChangeAuditFactory.create(
        opportunity=opportunity,
        updated_at=saved_opportunity.last_notified_at + timedelta(minutes=1),
    )

    result = cli_runner.invoke(args=["task", "generate-notifications"])

    assert result.exit_code == 0

    # Verify expected log messages
    assert "Collected opportunity notifications" in caplog.text
    assert "Would send notification to user" in caplog.text

    # Verify the log contains the correct metrics
    log_records = [r for r in caplog.records if "Would send notification to user" in r.message]
    assert len(log_records) == 1
    extra = log_records[0].__dict__
    assert extra["user_id"] == user.user_id
    assert extra["opportunity_count"] == 1
    assert extra["search_count"] == 0


def test_last_notified_at_updates(cli_runner, db_session, enable_factory_create, user):
    """Test that last_notified_at gets updated after sending notifications"""
    # Create an opportunity that was updated after the last notification
    opportunity = factories.OpportunityFactory.create()
    saved_opp = factories.UserSavedOpportunityFactory.create(
        user=user,
        opportunity=opportunity,
        last_notified_at=opportunity.updated_at - timedelta(days=1),
    )
    factories.OpportunityChangeAuditFactory.create(
        opportunity=opportunity,
        updated_at=saved_opp.last_notified_at + timedelta(minutes=1),
    )
    # Store the original notification time
    original_notification_time = saved_opp.last_notified_at

    # Run the notification task
    result = cli_runner.invoke(args=["task", "generate-notifications"])
    assert result.exit_code == 0

    # Refresh the saved opportunity from the database
    db_session.refresh(saved_opp)

    # Verify last_notified_at was updated
    assert saved_opp.last_notified_at > original_notification_time
    # Verify last_notified_at is now after the opportunity's updated_at
    assert saved_opp.last_notified_at > opportunity.updated_at


def test_notification_log_creation(
    cli_runner, db_session, enable_factory_create, clear_notification_logs, user
):
    """Test that notification logs are created when notifications are sent"""
    # Create a saved opportunity that needs notification
    opportunity = factories.OpportunityFactory.create()
    saved_opportunity = factories.UserSavedOpportunityFactory.create(
        user=user,
        opportunity=opportunity,
        last_notified_at=opportunity.updated_at - timedelta(days=1),
    )

    factories.OpportunityChangeAuditFactory.create(
        opportunity=opportunity,
        updated_at=saved_opportunity.last_notified_at + timedelta(minutes=1),
    )

    # Run the notification task
    result = cli_runner.invoke(args=["task", "generate-notifications"])
    assert result.exit_code == 0

    # Verify notification log was created
    notification_logs = db_session.query(UserNotificationLog).all()
    assert len(notification_logs) == 1

    log = notification_logs[0]
    assert log.user_id == user.user_id
    assert log.notification_reason == NotificationConstants.OPPORTUNITY_UPDATES
    assert log.notification_sent is True


def test_no_notification_log_when_no_updates(
    cli_runner, db_session, enable_factory_create, clear_notification_logs, user
):
    """Test that no notification log is created when there are no updates"""
    # Create a saved opportunity that doesn't need notification
    opportunity = factories.OpportunityFactory.create()
    factories.UserSavedOpportunityFactory.create(
        user=user,
        opportunity=opportunity,
        last_notified_at=opportunity.updated_at + timedelta(minutes=1),  # After the update
    )

    # Run the notification task
    result = cli_runner.invoke(args=["task", "generate-notifications"])
    assert result.exit_code == 0

    # Verify no notification log was created
    notification_logs = db_session.query(UserNotificationLog).all()
    assert len(notification_logs) == 0


def test_search_notifications_cli(
    cli_runner, db_session, enable_factory_create, user, caplog, clear_notification_logs
):
    """Test that verifies we can collect and send search notifications via CLI"""
    # Create a saved search that needs notification
    saved_search = factories.UserSavedSearchFactory.create(
        user=user,
        search_query={"keywords": "test"},
        name="Test Search",
        last_notified_at=datetime_util.utcnow() - timedelta(days=1),
        searched_opportunity_ids=[1, 2, 3],
    )

    result = cli_runner.invoke(args=["task", "generate-notifications"])

    assert result.exit_code == 0

    # Verify expected log messages
    assert "Collected search notifications" in caplog.text
    assert "Would send notification to user" in caplog.text

    # Verify the log contains the correct metrics
    log_records = [r for r in caplog.records if "Would send notification to user" in r.message]
    assert len(log_records) == 1
    extra = log_records[0].__dict__
    assert extra["user_id"] == user.user_id
    assert extra["opportunity_count"] == 0
    assert extra["search_count"] == 1

    # Verify notification log was created
    notification_logs = (
        db_session.query(UserNotificationLog)
        .filter(UserNotificationLog.notification_reason == NotificationConstants.SEARCH_UPDATES)
        .all()
    )
    assert len(notification_logs) == 1

    # Verify last_notified_at was updated
    db_session.refresh(saved_search)
    assert saved_search.last_notified_at > datetime_util.utcnow() - timedelta(minutes=1)


def test_combined_notifications_cli(
    cli_runner, db_session, enable_factory_create, user, caplog, clear_notification_logs
):
    """Test that verifies we can handle both opportunity and search notifications together"""
    # Create a saved opportunity that needs notification
    opportunity = factories.OpportunityFactory.create()
    saved_opportunity = factories.UserSavedOpportunityFactory.create(
        user=user,
        opportunity=opportunity,
        last_notified_at=opportunity.updated_at - timedelta(days=1),
    )
    factories.OpportunityChangeAuditFactory.create(
        opportunity=opportunity,
        updated_at=saved_opportunity.last_notified_at + timedelta(minutes=1),
    )

    # Create a saved search that needs notification
    saved_search = factories.UserSavedSearchFactory.create(
        user=user,
        search_query={"keywords": "test"},
        name="Test Search",
        last_notified_at=datetime_util.utcnow() - timedelta(days=1),
        searched_opportunity_ids=[1, 2, 3],
    )

    result = cli_runner.invoke(args=["task", "generate-notifications"])

    assert result.exit_code == 0

    # Verify expected log messages
    assert "Collected opportunity notifications" in caplog.text
    assert "Collected search notifications" in caplog.text
    assert "Would send notification to user" in caplog.text

    # Verify the log contains the correct metrics
    log_records = [r for r in caplog.records if "Would send notification to user" in r.message]
    assert len(log_records) == 1
    extra = log_records[0].__dict__
    assert extra["user_id"] == user.user_id
    assert extra["opportunity_count"] == 1
    assert extra["search_count"] == 1

    # Verify notification logs were created for both types
    notification_logs = db_session.query(UserNotificationLog).all()
    assert len(notification_logs) == 2

    notification_reasons = {log.notification_reason for log in notification_logs}
    assert notification_reasons == {
        NotificationConstants.OPPORTUNITY_UPDATES,
        NotificationConstants.SEARCH_UPDATES,
    }

    # Verify last_notified_at was updated for both
    db_session.refresh(saved_opportunity)
    db_session.refresh(saved_search)
    assert saved_opportunity.last_notified_at > datetime_util.utcnow() - timedelta(minutes=1)
    assert saved_search.last_notified_at > datetime_util.utcnow() - timedelta(minutes=1)
