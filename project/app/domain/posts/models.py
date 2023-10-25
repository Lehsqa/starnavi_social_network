from datetime import datetime

from pydantic import Field

from project.app.infrastructure.models import InternalModel, PublicModel


# Public models
# ------------------------------------------------------
class _PostPublic(PublicModel):
    user_id: int = Field(description="OpenAPI desc")
    content: str = Field(description="OpenAPI desc")
    created_at: datetime = Field(description="OpenAPI desc")


class PostCreateRequestBody(_PostPublic):
    pass


class PostPublic(_PostPublic):
    id: int


# Internal models
# ------------------------------------------------------
class PostContent(InternalModel):
    content: str


class PostUncommited(PostContent):
    user_id: int
    created_at: datetime


class Post(PostUncommited):
    id: int
