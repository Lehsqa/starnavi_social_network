from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette import status

from project.app.application.analytics import get_likes_analytics_data
from project.app.application.authentication import JWTBearer, get_current_user
from project.app.application.users import update_user
from project.app.domain.users import User, UserPublic, UsersRepository

router = APIRouter(prefix='/analytics', tags=['Analytics'])


@router.get("/user", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def user_analytics(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserPublic:
    user_public: User = await UsersRepository().get(name_=current_user.name)

    return UserPublic.model_validate(user_public)


@router.get("/likes", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def likes_analytics(
    date_from: date,
    date_to: date,
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)]
):
    analytics_data = await get_likes_analytics_data(date_from=date_from, date_to=date_to, user_id=current_user.id)

    return analytics_data
