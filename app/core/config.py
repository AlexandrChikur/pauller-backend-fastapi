from starlette.config import Config
from starlette.datastructures import URL, Secret

config = Config(".env")

API_PREFIX = "/api"
JWT_TOKEN_PREFIX = "Token"

PROJECT_NAME: str = config("PROJECT_NAME", default="Pauller")
PROJECT_DESCRIPTION: str = config("PROJECT_DESCRIPTION", cast=str, default="")
VERSION: str = config("VERSION", default="latest")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: URL = config("DATABASE_URL", cast=URL)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)

PATH_TO_MIGRATIONS: str = config("PATH_TO_MIGRATIONS", cast=str)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
