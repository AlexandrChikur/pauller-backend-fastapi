from fastapi import APIRouter

from app.api.routes import polls, users

router = APIRouter()

router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(polls.router, tags=["polls"], prefix="/polls")
