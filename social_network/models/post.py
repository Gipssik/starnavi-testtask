import sqlalchemy as sa
from sqlalchemy.orm import relationship, mapped_column

from social_network.models.base import Base

post_likes = sa.Table(
    "post_likes",
    Base.metadata,
    sa.Column("post_id", sa.Integer, sa.ForeignKey("post.id"), primary_key=True),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
)


class Post(Base):
    __tablename__ = "post"

    id = mapped_column(sa.Integer, primary_key=True)
    title = mapped_column(sa.String(length=128), nullable=False)
    content = mapped_column(sa.String(length=1024), nullable=False)
    user_id = mapped_column(sa.ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="posts")
    likes = relationship("User", secondary=post_likes, back_populates="liked_posts")

    @property
    def likes_count(self) -> int:
        return len(self.likes)
