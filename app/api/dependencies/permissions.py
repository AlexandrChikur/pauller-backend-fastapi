from typing import Callable, Dict

from fastapi import Depends, Request

from app.api.errors.permissions import PermissionDeniedError
from app.services.permissions import get_permissions


def get_admin_permissionizer(*, required: bool = True) -> Callable:
    return has_admin_permission if required else has_admin_permission_optional


def get_active_permissionizer(*, required: bool = True) -> Callable:
    return has_active_permission if required else has_active_permission_optional


def has_active_permission_optional(
    request: Request, permissions: Dict[str, bool] = Depends(get_permissions)
) -> None:
    if permissions["is_active"]:
        request.app.state.active_user_requested = True
        return

    request.app.state.active_user_requested = False


def has_admin_permission_optional(
    request: Request, permissions: Dict[str, bool] = Depends(get_permissions)
) -> None:
    if permissions["is_admin"]:
        request.app.state.admin_user_requested = True
        return

    request.app.state.admin_user_requested = False


def has_active_permission(
    request: Request, permissions: Dict[str, bool] = Depends(get_permissions)
) -> None:
    if not permissions["is_active"]:
        raise PermissionDeniedError

    request.app.state.active_user_requested = True


def has_admin_permission(
    request: Request, permissions: Dict[str, bool] = Depends(get_permissions),
) -> None:
    if not permissions["is_admin"]:
        raise PermissionDeniedError(sub="user is not admin")

    request.app.state.admin_user_requested = True
