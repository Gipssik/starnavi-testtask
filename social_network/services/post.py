from sqlalchemy.orm import selectinload

from social_network.models import Post, User
from social_network.schemas.post import PostCreate
from social_network.services.base import BaseService


class PostService(BaseService[Post]):
    model = Post

    async def get_post(self, post_id: int) -> Post:
        """Get a post with the given id."""
        filters = (self.model.id == post_id,)
        options = (selectinload(Post.likes),)
        return await self.get_one(filters, options)

    async def post_exists(self, post_id: int) -> bool:
        """Check if post with the given id exists."""
        filters = (self.model.id == post_id,)
        return await self.exists(filters)

    async def create_post(self, data: PostCreate, user: User) -> Post:
        """Create a post with the given data."""
        values = {
            "title": data.title,
            "content": data.content,
            "user_id": user.id,
        }
        obj = await self.insert_obj(self.model(**values))
        obj.__dict__["likes"] = []  # to avoid making another query
        return obj
