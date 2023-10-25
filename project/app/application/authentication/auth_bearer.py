from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .authentication import verify_token
from project.app.infrastructure.errors import AuthenticationError, AuthorizationError


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer" or not verify_token(credentials.credentials):
                raise AuthenticationError
            return credentials.credentials
        else:
            raise AuthorizationError
