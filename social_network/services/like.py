from datetime import date

from social_network.models import User
from social_network.models.post import post_likes
from social_network.services.base import BaseService


class LikeService(BaseService[post_likes]):
    model = post_likes

    async def like_post(self, user: User, post_id: int) -> None:
        """Check if user already liked post and like post if not."""
        if not await self.user_liked_post(user, post_id):
            await self.insert({"post_id": post_id, "user_id": user.id})

    async def unlike_post(self, user: User, post_id: int) -> None:
        """Check if user already liked post and unlike post if yes."""
        if await self.user_liked_post(user, post_id):
            filters = (self.model.c.post_id == post_id, self.model.c.user_id == user.id)
            await self.delete(filters)

    async def user_liked_post(self, user: User, post_id: int) -> bool:
        """Check if user liked post."""
        filters = (self.model.c.post_id == post_id, self.model.c.user_id == user.id)
        return await self.exists(filters)

    async def likes_made_in_range(self, from_date: date, to_date: date) -> int:
        """Count likes made in range."""
        filters = (self.model.c.created_at >= from_date, self.model.c.created_at <= to_date)
        return await self.count(filters)
