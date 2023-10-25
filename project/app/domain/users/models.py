from datetime import datetime

from pydantic import Field

from project.app.infrastructure.models import InternalModel, PublicModel


# Public models
# ------------------------------------------------------
class _UserPublic(PublicModel):
    name: str = Field(description="OpenAPI desc")
    last_login: datetime = Field(description="OpenAPI desc")
    last_request: datetime = Field(description="OpenAPI desc")


class UserCreateRequestBody(_UserPublic):
    password: str


class UserPublic(_UserPublic):
    id: int


# Internal models
# ------------------------------------------------------
class UserLogin(InternalModel):
    name: str
    password: str


class UserUncommited(UserLogin):
    last_login: datetime
    last_request: datetime


class User(UserUncommited):
    id: int
