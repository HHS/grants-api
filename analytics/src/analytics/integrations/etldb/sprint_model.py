"""Define EtlSprintModel class to encapsulate db CRUD operations."""

from pandas import Series
from sqlalchemy import text

from analytics.datasets.etl_dataset import EtlEntityType
from analytics.integrations.etldb.etldb import EtlChangeType, EtlDb


class EtlSprintModel(EtlDb):
    """Encapsulate CRUD operations for sprint entity."""

    def sync_sprint(self, sprint_df: Series, ghid_map: dict) -> tuple[
        int | None,
        EtlChangeType,
    ]:
        """Write sprint data to etl database."""
        # initialize return value
        change_type = EtlChangeType.NONE

        # insert dimensions
        sprint_id = self._insert_dimensions(sprint_df, ghid_map)
        if sprint_id is not None:
            change_type = EtlChangeType.INSERT

        # if insert failed, select and update
        if sprint_id is None:
            sprint_id, change_type = self._update_dimensions(sprint_df, ghid_map)

        return sprint_id, change_type

    def _insert_dimensions(self, sprint_df: Series, ghid_map: dict) -> int | None:
        """Write sprint dimension data in etl database."""
        # insert into dimension table: sprint
        new_row_id = None
        cursor = self.connection()
        result = cursor.execute(
            text(
                "insert into gh_sprint(ghid, name, start_date, end_date, duration, quad_id) "
                "values (:ghid, :name, :start, :end, :duration, :quad_id) "
                "on conflict(ghid) do nothing returning id",
            ),
            {
                "ghid": sprint_df["sprint_ghid"],
                "name": sprint_df["sprint_name"],
                "start": sprint_df["sprint_start"],
                "end": sprint_df["sprint_end"],
                "duration": sprint_df["sprint_length"],
                "quad_id": ghid_map[EtlEntityType.QUAD].get(sprint_df["quad_ghid"]),
            },
        )
        row = result.fetchone()
        if row:
            new_row_id = row[0]

        # commit
        self.commit(cursor)

        return new_row_id

    def _update_dimensions(self, sprint_df: Series, ghid_map: dict) -> tuple[
        int | None,
        EtlChangeType,
    ]:
        """Update sprint dimension data in etl database."""
        # initialize return value
        change_type = EtlChangeType.NONE

        # get new values
        new_values = (
            sprint_df["sprint_name"],
            sprint_df["sprint_start"],
            sprint_df["sprint_end"],
            sprint_df["sprint_length"],
            ghid_map[EtlEntityType.QUAD].get(sprint_df["quad_ghid"]),
        )

        # select old values
        sprint_id, old_name, old_start, old_end, old_duration, old_quad_id = (
            self._select(sprint_df["sprint_ghid"])
        )
        old_values = (old_name, old_start, old_end, old_duration, old_quad_id)

        # compare
        if sprint_id is not None and new_values != old_values:
            change_type = EtlChangeType.UPDATE
            cursor = self.connection()
            cursor.execute(
                text(
                    "update gh_sprint set name = :new_name, start_date = :new_start, "
                    "end_date = :new_end, duration = :new_duration, quad_id = :quad_id, "
                    "t_modified = current_timestamp where id = :sprint_id",
                ),
                {
                    "new_name": new_values[0],
                    "new_start": new_values[1],
                    "new_end": new_values[2],
                    "new_duration": new_values[3],
                    "quad_id": new_values[4],
                    "sprint_id": sprint_id,
                },
            )
            self.commit(cursor)

        return sprint_id, change_type

    def _select(self, ghid: str) -> tuple[
        int | None,
        str | None,
        str | None,
        str | None,
        int | None,
        int | None,
    ]:
        """Select epic data from etl database."""
        cursor = self.connection()
        result = cursor.execute(
            text(
                "select id, name, start_date, end_date, duration, quad_id "
                "from gh_sprint where ghid = :ghid",
            ),
            {"ghid": ghid},
        )
        row = result.fetchone()
        if row:
            return row[0], row[1], row[2], row[3], row[4], row[5]

        return None, None, None, None, None, None
