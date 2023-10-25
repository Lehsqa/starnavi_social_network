from datetime import datetime
from typing import Any

from project.app.application.authentication.authentication import get_password_hash
from project.app.domain.users import (
    User,
    UsersRepository,
    UserUncommited
)


async def create_user(payload: dict) -> User:
    payload.update(password=get_password_hash(payload["password"]),
                   last_login=datetime.now(),
                   last_request=datetime.now())

    user: User = await UsersRepository().create(
        UserUncommited(**payload)
    )
    return user


async def update_user(id: int, field: str, data: Any):
    await UsersRepository().update(id_=id, field_=field, data=data)
