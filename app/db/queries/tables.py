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
    is_staff BOOL
)"""
