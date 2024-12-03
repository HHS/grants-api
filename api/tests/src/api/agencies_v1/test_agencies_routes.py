import pytest

from src.db.models.agency_models import Agency, LinkAgencyDownloadFileType
from tests.src.db.models.factories import AgencyFactory


@pytest.fixture(autouse=True)
def cleanup_agencies(db_session):
    yield
    agencies = db_session.query(Agency).all()
    db_session.delete(agencies)
    db_session.commit()


def test_agencies_get_default_dates(client, api_auth_token, enable_factory_create, db_session):
    # These should return in the default date range
    AgencyFactory.create_batch(20)

    payload = {
        "filters": {},
        "pagination": {
            "page": 1,
            "page_size": 10,
            "page_offset": 1,
            "order_by": "created_at",
            "sort_direction": "descending",
        },
    }
    response = client.post("/v1/agencies", headers={"X-Auth": api_auth_token}, json=payload)
    assert response.status_code == 200
    data = response.json["data"]
    assert len(data) == 10
