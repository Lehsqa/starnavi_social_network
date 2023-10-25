import os
from datetime import datetime
import time
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from project.app.domain.authentication import TokenPayload, TokenClaimRequestBody, AccessToken

from datetime import timedelta

from passlib.context import CryptContext

from project.app.domain.users import User, UsersRepository
from project.app.infrastructure.errors import AuthenticationError, NotFoundError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name=os.environ.get("AUTHENTICATION_SCHEME"),
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
    login_psw: TokenClaimRequestBody,
    expires_delta: timedelta or None = None
) -> TokenPayload:
    try:
        user_public: User = await UsersRepository().get(name_=login_psw.login)
        if not verify_password(login_psw.password, user_public.password):
            raise AuthenticationError
        if expires_delta:
            expire: datetime = datetime.utcnow() + expires_delta
        else:
            expire: datetime = datetime.utcnow() + timedelta(minutes=15)
        await UsersRepository().update(id_=user_public.id, field_='last_login', data=datetime.now())
        return TokenPayload(sub=login_psw.login, exp=time.mktime(expire.timetuple()))
    except NotFoundError:
        raise AuthenticationError


def create_access_token(token_payload: TokenPayload) -> AccessToken:
    encoded_jwt: str = jwt.encode(
        token_payload.model_dump(),
        os.environ.get("SECRET_KEY"),
        algorithm=os.environ.get("ALGORITHM")
    )
    return AccessToken(payload=token_payload, raw_token=encoded_jwt)


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            return False
        return True
    except JWTError:
        return False


async def get_current_user(token: Annotated[str, Depends(oauth2_oauth)]) -> User:
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        username: str = payload.get("sub")
        if username is None:
            raise AuthenticationError
        user_public: User = await UsersRepository().get(name_=username)
        return user_public
    except (JWTError, NotFoundError):
        raise AuthenticationError
