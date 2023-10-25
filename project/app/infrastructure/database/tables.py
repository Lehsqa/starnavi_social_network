from typing import TypeVar

from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy.orm import declarative_base, relationship

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class _Base:
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=_Base, metadata=meta)

ConcreteTable = TypeVar("ConcreteTable", bound=Base)


class UsersTable(Base):
    __tablename__ = 'users'

    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    last_login = Column(DateTime, nullable=False)
    last_request = Column(DateTime, nullable=False)


class PostsTable(Base):
    __tablename__ = 'posts'

    user_id = Column(ForeignKey(UsersTable.id))
    content = Column(String, nullable=False)
    likes = relationship('LikesTable', backref='post', lazy='dynamic')
    created_at = Column(DateTime, nullable=False)


class LikesTable(Base):
    __tablename__ = 'likes'

    user_id = Column(ForeignKey(UsersTable.id))
    post_id = Column(ForeignKey(PostsTable.id))
    created_at = Column(DateTime, nullable=False)
