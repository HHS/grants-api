from uuid import UUID

from sqlalchemy import select

from src.adapters import db
from src.api.route_utils import raise_flask_error
from src.db.models.user_models import UserSavedSearch


def update_saved_search(
    db_session: db.Session, user_id: UUID, saved_search_id: UUID, json_data: dict
) -> None:
    """Update saved search for a user"""
    saved_search = db_session.execute(
        select(UserSavedSearch).where(
            UserSavedSearch.saved_search_id == saved_search_id, UserSavedSearch.user_id == user_id
        )
    ).scalar_one_or_none()

    if not saved_search:
        raise_flask_error(404, "Saved search not found")

    # Update
    UserSavedSearch.name = json_data["name"]
