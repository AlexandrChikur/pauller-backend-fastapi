CREATE_POLL = """
INSERT INTO polls (title, description, author_id, created_at, start_at, finish_at, poll_type, anonymously)
VALUES($1, $2, $3, $4, $5, $6, $7, $8)
"""
