from typing import Optional, Dict, Any

from starlette import status

from core import UnicornException


class Unauthorized(UnicornException):
    def __init__(
        self,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            developer_message=kwargs.get('developer_message', "You cannot access this resource with the provided credentials."),
            user_message=kwargs.get("user_message", "You cannot access this resource with the provided credentials.")
        )
        self.headers = headers