from yoyo import step

from app.db.queries.tables import CREATE_USERS_TABLE_QUERY

steps = [step(CREATE_USERS_TABLE_QUERY, ignore_errors="apply")]
