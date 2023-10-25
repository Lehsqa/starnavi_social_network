from datetime import datetime

from project.app.infrastructure.database import BaseRepository, LikesTable
from .models import Like, LikeUncommited
from ..analytics.models import AnalyticsLikes


class LikesRepository(BaseRepository[LikesTable]):
    schema_class = LikesTable

    async def get(self, post_id_: int, user_id_: int) -> Like:
        instance: LikesTable = await self._get_two_parameters(key_1='post_id', value_1=post_id_,
                                                              key_2='user_id', value_2=user_id_)
        return Like.model_validate(instance)

    async def create(self, schema: LikeUncommited) -> Like:
        instance: LikesTable = await self._save(schema.model_dump())
        return Like.model_validate(instance)

    async def destroy(self, post_id_: int, user_id_: int):
        await self._destroy(key_1='post_id', value_1=post_id_, key_2='user_id', value_2=user_id_)

    async def count(self, date_from: datetime, date_to: datetime):
        async for instance in self._count(key='created_at',
                                          label_1='date', label_2='likes_count',
                                          value_1=date_from, value_2=date_to):
            yield AnalyticsLikes.model_validate(instance)
