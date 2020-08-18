from fastapi import FastAPI

from app.api.metadata import TAGS_METADATA
from app.api.routes.api import router as api_router
from app.core.config import (
    API_PREFIX,
    DEBUG,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    VERSION,
)
from app.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    application = FastAPI(
        title=PROJECT_NAME,
        description=PROJECT_DESCRIPTION,
        version=VERSION,
        debug=DEBUG,
        openapi_tags=TAGS_METADATA,
    )
    # fmt: off
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
    # fmt: on
    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()
