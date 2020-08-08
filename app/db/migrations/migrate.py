import time

from psycopg2.errors import OperationalError
from yoyo import get_backend, read_migrations

from app.core.config import DATABASE_URL, PATH_TO_MIGRATIONS

while True:
    try:
        backend = get_backend(str(DATABASE_URL))
        break
    except OperationalError:
        time.sleep(1)


migrations = read_migrations(PATH_TO_MIGRATIONS)


def make_migrations() -> None:
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
