from datetime import date

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    likes_count: int

    class Config:
        from_attributes = True


class LikesAnalytics(BaseModel):
    likes_count: int
