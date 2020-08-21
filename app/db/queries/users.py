CREATE_USER_QUERY = """
INSERT INTO users (username, email, hashed_password, bio, image, is_active, is_admin) VALUES($1, $2, $3, $4, $5, $6, $7)
"""

GET_USER_BY_USERNAME = """
SELECT id, username, email, hashed_password, bio, image, is_active, is_admin FROM users WHERE username=$1
"""

GET_USER_BY_EMAIL = """
SELECT id, username, email, hashed_password, bio, image, is_active, is_admin FROM users WHERE email=$1
"""

UPDATE_USER = """
UPDATE users SET username=$2, email=$3, hashed_password=$4, bio=$5, image=$6 WHERE username=$1
"""
