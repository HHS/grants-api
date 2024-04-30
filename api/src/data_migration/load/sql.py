#
# SQL building for data load process.
#

import sqlalchemy


def build_insert_select_sql(
    source_table: sqlalchemy.Table, destination_table: sqlalchemy.Table
) -> tuple[sqlalchemy.Insert, sqlalchemy.Select]:
    """Build an `INSERT INTO ... SELECT ... FROM ...` query for new rows."""

    all_columns = tuple(c.name for c in source_table.columns)

    # `SELECT col1, col2, ..., FALSE FROM <source_table>`    (the FALSE is for is_deleted)
    select_sql = sqlalchemy.select(source_table, False).where(
        # `WHERE (id1, id2, id3, ...) NOT IN`    (id1, id2, ... is the multipart primary key)
        sqlalchemy.tuple_(*source_table.primary_key.columns).not_in(
            # `(SELECT (id1, id2, id3, ...) FROM <destination_table>)`    (subquery)
            sqlalchemy.select(destination_table.primary_key.columns)
        )
    )
    # `INSERT INTO <destination_table> (col1, col2, ..., is_deleted) SELECT ...`
    insert_from_select_sql = sqlalchemy.insert(destination_table).from_select(
        all_columns + (destination_table.c.is_deleted,), select_sql
    )

    return insert_from_select_sql, select_sql


def build_update_sql(
    source_table: sqlalchemy.Table, destination_table: sqlalchemy.Table
) -> sqlalchemy.Update:
    """Build an `UPDATE ... SET ... WHERE ...` statement for updated rows."""
    return (
        # `UPDATE <destination_table>`
        sqlalchemy.update(destination_table)
        # `SET col1=source_table.col1, col2=source_table.col2, ...`
        .values(source_table.columns)
        # `WHERE ...`
        .where(
            sqlalchemy.tuple_(*destination_table.primary_key.columns)
            == sqlalchemy.tuple_(*source_table.primary_key.columns),
            destination_table.c.last_upd_date < source_table.c.last_upd_date,
        )
    )


def build_mark_deleted_sql(
    source_table: sqlalchemy.Table, destination_table: sqlalchemy.Table
) -> sqlalchemy.Update:
    """Build an `UPDATE ... SET is_deleted = TRUE WHERE ...` statement for deleted rows."""
    return (
        # `UPDATE <destination_table>`
        sqlalchemy.update(destination_table)
        # `SET is_deleted = TRUE`
        .values(is_deleted=True)
        # `WHERE`
        .where(
            # `is_deleted == FALSE`
            destination_table.c.is_deleted == False,  # noqa: E712
            # `AND (id1, id2, id3, ...) NOT IN`    (id1, id2, ... is the multipart primary key)
            sqlalchemy.tuple_(*destination_table.primary_key.columns).not_in(
                # `(SELECT (id1, id2, id3, ...) FROM <source_table>)`    (subquery)
                sqlalchemy.select(source_table.primary_key.columns)
            ),
        )
    )
