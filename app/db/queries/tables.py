CREATE_USERS_TABLE_QUERY = """
CREATE TABLE users(
    id serial PRIMARY KEY,
    username VARCHAR(24),
    email TEXT,
    hashed_password TEXT,
    bio TEXT,
    image VARCHAR,
    is_active BOOL,
    is_super BOOL,
    is_staff BOOL)
"""

CREATE_POLLS_TABLE_QUERY = """
CREATE TABLE polls(
    id serial PRIMARY KEY,
    title VARCHAR(32),
    description TEXT,
    author_id INT REFERENCES users(id),
    created_at timestamptz,
    start_at timestamptz,
    finish_at timestamptz,
    poll_type VARCHAR,
    anonymously BOOL)
"""
