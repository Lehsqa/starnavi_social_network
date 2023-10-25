from datetime import datetime

from pydantic import Field

from project.app.infrastructure.models import InternalModel, PublicModel


# Public models
# ------------------------------------------------------
class _LikePublic(PublicModel):
    user_id: int = Field(description="OpenAPI desc")
    post_id: int = Field(description="OpenAPI desc")
    created_at: datetime = Field(description="OpenAPI desc")


class LikeCreateRequestBody(_LikePublic):
    pass


class LikePublic(_LikePublic):
    id: int


# Internal models
# ------------------------------------------------------
class LikePostId(InternalModel):
    post_id: int


class LikeUncommited(LikePostId):
    user_id: int
    created_at: datetime


class Like(LikeUncommited):
    id: int
