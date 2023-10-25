from datetime import datetime

from project.app.application.users import update_user
from project.app.domain.likes import Like, LikesRepository, LikeUncommited
from project.app.domain.posts import Post, PostsRepository, PostUncommited
from project.app.infrastructure.errors import DatabaseError, NotFoundError


async def create_post(payload: dict, user_id: int) -> Post:
    payload.update(created_at=datetime.now())

    post: Post = await PostsRepository().create(
        PostUncommited(**payload, user_id=user_id)
    )
    await update_user(id=user_id, field='last_request', data=datetime.now())

    return post


async def create_like(payload: dict, user_id: int) -> Like:
    payload.update(created_at=datetime.now())

    await update_user(id=user_id, field='last_request', data=datetime.now())
    try:
        await LikesRepository().get(post_id_=payload.get('post_id'), user_id_=user_id)
        raise DatabaseError(message='Already exist')
    except NotFoundError:
        like: Like = await LikesRepository().create(
            LikeUncommited(**payload, user_id=user_id)
        )
        return like


async def delete_like(payload: dict, user_id: int) -> dict[str, str]:
    await LikesRepository().destroy(post_id_=payload.get('post_id'), user_id_=user_id)
    await update_user(id=user_id, field='last_request', data=datetime.now())

    return {'details': f'Like to post_id={payload.get("post_id")} was deleted'}

