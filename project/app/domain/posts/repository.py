from project.app.infrastructure.database import BaseRepository, PostsTable
from .models import Post, PostUncommited


class PostsRepository(BaseRepository[PostsTable]):
    schema_class = PostsTable

    async def get(self, id_: int) -> Post:
        instance = await self._get(key='id', value=id_)
        return Post.model_validate(instance)

    async def create(self, schema: PostUncommited) -> Post:
        instance: PostsTable = await self._save(schema.model_dump())
        return Post.model_validate(instance)
