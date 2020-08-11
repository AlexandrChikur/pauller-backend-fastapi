from fastapi import HTTPException, status

from app.resources.strings import INCORRECT_LOGIN_INPUT, PERMISSION_DENIED


class WrongLoginError(HTTPException):
    """Raised when log in input is incorrect (login/email or/and password)"""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=INCORRECT_LOGIN_INPUT
        )


class PermissionDeniedError(HTTPException):
    """Raised when user which made a request haven't any of permissions (active, super, staff)"""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=PERMISSION_DENIED
        )