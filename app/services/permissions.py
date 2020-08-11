from typing import Dict, Optional

from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInDB


async def get_user_permissions(user: UserInDB) -> Optional[Dict[str, bool]]:
    if user:
        return {
            "is_active": user.is_active,
            "is_super": user.is_super,
            "is_staff": user.is_staff,
        }

    return None
