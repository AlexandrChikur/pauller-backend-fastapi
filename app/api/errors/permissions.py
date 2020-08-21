from fastapi import HTTPException, status

from app.resources.strings import PERMISSION_DENIED


class PermissionDeniedError(HTTPException):
    """ Raised when the user do not have required permissions (active/admin) """

    def __init__(self, sub: str = "user is not active"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": PERMISSION_DENIED, "sub": sub},
        )
