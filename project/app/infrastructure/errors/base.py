"""
This module is responsible for describing shared errors
that are handled on the last step of processing the request.
"""


from starlette import status


class BaseError(Exception):
    def __init__(
        self,
        message: str = "",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.message: str = message
        self.status_code: int = status_code

        super().__init__(message)


class BadRequestError(BaseError):
    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnprocessableError(BaseError):
    def __init__(
        self, message: str = "Validation error"
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class NotFoundError(BaseError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(
            message=message, status_code=status.HTTP_404_NOT_FOUND
        )


class DatabaseError(BaseError):
    def __init__(
        self, message: str = "Database error"
    ) -> None:
        super().__init__(
            message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class AuthenticationError(BaseError):
    def __init__(
        self, message: str = "Authentication error"
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(BaseError):
    def __init__(
        self, message: str = "Authorization error"
    ) -> None:
        super().__init__(
            message=message, status_code=status.HTTP_403_FORBIDDEN
        )
