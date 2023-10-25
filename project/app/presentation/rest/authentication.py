import os
from datetime import timedelta

from fastapi import APIRouter, Request, status

from project.app.application.authentication import authenticate_user, create_access_token
from project.app.application.users import create_user
from project.app.domain.authentication import (
    TokenClaimPublic,
    TokenClaimRequestBody,
)
from project.app.domain.users import User, UserLogin, UserPublic
from project.app.infrastructure.errors import DatabaseError

router = APIRouter(prefix="", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    _: Request,
    schema: TokenClaimRequestBody,
) -> TokenClaimPublic:
    access_token_expires = timedelta(minutes=float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    token_payload = await authenticate_user(schema, expires_delta=access_token_expires)
    access_token = create_access_token(token_payload=token_payload)

    return TokenClaimPublic(access=access_token.raw_token)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_signup(
    _: Request,
    schema: UserLogin,
) -> UserPublic:
    try:
        user: User = await create_user(payload=schema.model_dump())
        return UserPublic.model_validate(user)
    except DatabaseError:
        raise DatabaseError('Already exist')
