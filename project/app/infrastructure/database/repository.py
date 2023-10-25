from typing import Any, AsyncGenerator, Generic, Type

from sqlalchemy import Result, func, select, delete, update

from project.app.infrastructure.database.session import Session
from project.app.infrastructure.database.tables import ConcreteTable
from project.app.infrastructure.errors import NotFoundError, UnprocessableError


class BaseRepository(Session, Generic[ConcreteTable]):  # type: ignore
    """This class implements the base interface for working with database
    # and makes it easier to work with type annotations.
    """

    schema_class: Type[ConcreteTable]
    schema_class_join = Type[ConcreteTable]

    def __init__(self) -> None:
        super().__init__()

        if not self.schema_class:
            raise UnprocessableError(
                message=(
                    "Can not initiate the class without schema_class attribute"
                )
            )

    async def _get(self, key: str, value: Any) -> ConcreteTable:
        query = select(
            self.schema_class
        ).where(
            getattr(self.schema_class, key) == value
        )
        result: Result = await self.execute(query)

        if not (_result := result.scalars().one_or_none()):
            raise NotFoundError

        return _result

    async def _get_two_parameters(self, key_1: str, value_1: Any, key_2: str, value_2: Any) -> ConcreteTable:
        query = select(
            self.schema_class
        ).where(
            getattr(self.schema_class, key_1) == value_1,
        ).where(
            getattr(self.schema_class, key_2) == value_2
        )
        result: Result = await self.execute(query)

        if not (_result := result.scalars().one_or_none()):
            raise NotFoundError

        return _result

    async def _save(self, payload: dict[str, Any]) -> ConcreteTable:
        schema = self.schema_class(**payload)
        await self.save(schema)
        return schema

    async def _destroy(self, key_1: str, value_1: Any, key_2: str, value_2: Any):
        query = delete(
            self.schema_class
        ).where(
            getattr(self.schema_class, key_1) == value_1,
        ).where(
            getattr(self.schema_class, key_2) == value_2
        )
        await self.execute(query)

    async def _update(self, key: str, value: Any, field: str, data: Any):
        query = update(
            self.schema_class
        ).where(
            getattr(self.schema_class, key) == value,
        ).values(
            {getattr(self.schema_class, field): data}
        )
        result: Result = await self.execute(query)

        return result

    async def _count(
        self,
        key: str,
        label_1: str,
        label_2: str,
        value_1: Any,
        value_2: Any
    ) -> AsyncGenerator[ConcreteTable, None]:
        query = select(
            func.date(getattr(self.schema_class, key)).label(label_1),
            func.count(getattr(self.schema_class, 'id')).label(label_2)
        ).where(
            getattr(self.schema_class, key) >= value_1
        ).where(
            getattr(self.schema_class, key) <= value_2
        ).group_by(
            func.date(getattr(self.schema_class, key))
        )
        result: Result = await self.execute(query)
        schemas = result.all()

        for schema in schemas:
            yield schema
