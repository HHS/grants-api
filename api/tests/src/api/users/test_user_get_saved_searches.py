import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import delete

from src.constants.lookup_constants import FundingInstrument
from src.db.models.user_models import UserSavedSearch, UserTokenSession
from tests.src.db.models.factories import UserFactory, UserSavedSearchFactory


@pytest.fixture
def saved_searches(user, db_session):
    searches = [
        UserSavedSearchFactory.create(
            user=user,
            name="Test Search 1",
            search_query={
                "query": "python",
                "filters": {"funding_instrument": {"one_of": [FundingInstrument.GRANT]}},
            },
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        ),
        UserSavedSearchFactory.create(
            user=user,
            name="Test Search 2",
            search_query={
                "query": "python",
                "filters": {
                    "keywords": "java",
                    "funding_instrument": {"one_of": [FundingInstrument.COOPERATIVE_AGREEMENT]},
                },
            },
            created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
        ),
        UserSavedSearchFactory.create(
            user=user,
            name="Test Search 2",
            search_query={
                "query": "python",
                "filters": {
                    "keywords": "java",
                    "funding_instrument": {"one_of": [FundingInstrument.PROCUREMENT_CONTRACT]},
                },
            },
            created_at=datetime(2024, 1, 3, tzinfo=timezone.utc),
        ),
    ]
    db_session.commit()
    return searches


@pytest.fixture(autouse=True)
def clear_data(db_session):
    db_session.execute(delete(UserSavedSearch))
    db_session.execute(delete(UserTokenSession))
    db_session.commit()
    yield


def test_user_get_saved_searches_unauthorized_user(
    client, db_session, user, user_auth_token, saved_searches
):
    # Try to get searches for a different user ID
    different_user = UserFactory.create()
    db_session.commit()

    response = client.get(
        f"/v1/users/{different_user.user_id}/saved-searches",
        headers={"X-SGG-Token": user_auth_token},
    )

    assert response.status_code == 401
    assert response.json["message"] == "Unauthorized user"


def test_user_get_saved_searches_no_auth(client, db_session, user, saved_searches):
    # Try to get searches without authentication
    response = client.get(
        f"/v1/users/{user.user_id}/saved-searches",
    )

    assert response.status_code == 401
    assert response.json["message"] == "Unable to process token"


def test_user_get_saved_searches_empty(client, user, user_auth_token):
    response = client.get(
        f"/v1/users/{user.user_id}/saved-searches",
        headers={"X-SGG-Token": user_auth_token},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Success"
    assert response.json["data"] == []


def test_user_get_saved_searches(client, user, user_auth_token, saved_searches):
    response = client.post(
        f"/v1/users/{user.user_id}/saved-searches/list",
        headers={"X-SGG-Token": user_auth_token},
        json={
            "pagination": {
                "page_offset": 1,
                "page_size": 25,
                "sort_order": [
                    {"order_by": "name", "sort_direction": "descending"},
                    {"order_by": "created_at", "sort_direction": "descending"},
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json["message"] == "Success"

    data = response.json["data"]
    assert len(data) == 3

    # Verify the searches are returned in descending order by name, then descending order by created_at
    assert data[0]["name"] == "Test Search 1"
    assert data[0]["search_query"]["filters"]["funding_instrument"]["one_of"] == ["grant"]
    assert data[1]["name"] == "Test Search 2"
    assert data[1]["search_query"]["filters"]["funding_instrument"]["one_of"] == [
        "cooperative_agreement"
    ]

    assert data[2]["name"] == "Test Search 2"
    assert data[2]["search_query"]["filters"]["funding_instrument"]["one_of"] == [
        "procurement_contract"
    ]

    # Verify UUIDs are properly serialized
    assert uuid.UUID(data[0]["saved_search_id"])
    assert uuid.UUID(data[1]["saved_search_id"])
    assert uuid.UUID(data[2]["saved_search_id"])
