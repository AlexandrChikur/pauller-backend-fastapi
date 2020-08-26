CREATE_POLL = """
INSERT INTO polls (title, description, author_id, created_at, start_at, finish_at, poll_type, anonymously)
VALUES($1, $2, $3, $4, $5, $6, $7, $8)
"""

GET_POLLS = """
SELECT * FROM polls OFFSET $1 LIMIT $2
"""

GET_ALL_POLLS = """
SELECT * FROM polls
"""

GET_POLLS_COUNT = """
SELECT COUNT(*) FROM polls
"""

DELETE_POLL_BY_ID = """
DELETE FROM polls WHERE id=$1
"""
