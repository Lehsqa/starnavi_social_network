from datetime import datetime
from typing import Any

from project.app.infrastructure.database import BaseRepository, UsersTable
from .models import User, UserUncommited


class UsersRepository(BaseRepository[UsersTable]):
    schema_class = UsersTable

    async def get(self, name_: str) -> User:
        instance = await self._get(key='name', value=name_)
        return User.model_validate(instance)

    async def create(self, schema: UserUncommited) -> User:
        instance: UsersTable = await self._save(schema.model_dump())
        return User.model_validate(instance)

    async def update(self, id_: int, field_: str, data: Any) -> User:
        await self._update(key='id', value=id_, field=field_, data=data)
