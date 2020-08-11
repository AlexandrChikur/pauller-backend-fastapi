from yoyo import step

from app.db.queries.tables import (CREATE_POLLS_TABLE_QUERY,
                                   CREATE_USERS_TABLE_QUERY)

step(CREATE_USERS_TABLE_QUERY, ignore_errors="apply")
step(CREATE_POLLS_TABLE_QUERY, ignore_errors="apply")
