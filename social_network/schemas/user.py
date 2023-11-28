from datetime import datetime

from fastapi_users import schemas as fu_schemas
from pydantic import BaseModel


class UserRead(fu_schemas.BaseUser[int]):
    nickname: str | None = None


class UserCreate(fu_schemas.BaseUserCreate):
    nickname: str | None = None


class UserActivity(BaseModel):
    last_login: datetime | None = None
    last_request: datetime | None = None
