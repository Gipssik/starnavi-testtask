from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from social_network.api.dependencies.db import get_async_session
from social_network.services.like import LikeService
from social_network.services.post import PostService


async def get_post_service(session: AsyncSession = Depends(get_async_session)) -> PostService:
    return PostService(session)


async def get_like_service(session: AsyncSession = Depends(get_async_session)) -> LikeService:
    return LikeService(session)
