from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from project.app.application.authentication import JWTBearer, get_current_user
from project.app.application.posts import create_post, create_like
from project.app.application.users import update_user
from project.app.domain.likes import LikePostId, LikePublic, Like, LikesRepository
from project.app.domain.posts import PostContent, PostPublic, Post
from project.app.domain.users import User

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.post("", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def post_create(
    _: Request,
    schema: PostContent,
    current_user: Annotated[User, Depends(get_current_user)]
) -> PostPublic:
    post: Post = await create_post(payload=schema.model_dump(), user_id=current_user.id)

    return PostPublic.model_validate(post)


@router.post("/like", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def post_like(
    _: Request,
    schema: LikePostId,
    current_user: Annotated[User, Depends(get_current_user)]
) -> LikePublic:
    like: Like = await create_like(payload=schema.model_dump(), user_id=current_user.id)

    return LikePublic.model_validate(like)


@router.post("/unlike", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_202_ACCEPTED)
async def post_unlike(
    _: Request,
    schema: LikePostId,
    current_user: Annotated[User, Depends(get_current_user)]
):
    await LikesRepository().destroy(post_id_=schema.post_id, user_id_=current_user.id)
    await update_user(id=current_user.id, field='last_request', data=datetime.now())

    return {'details': f'Like to post_id={schema.post_id} was deleted'}
