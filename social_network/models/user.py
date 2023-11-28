from datetime import datetime
from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from social_network.models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(length=32), nullable=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_request: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    posts = relationship("Post", back_populates="user")
    liked_posts = relationship("Post", secondary="post_likes", back_populates="likes")
