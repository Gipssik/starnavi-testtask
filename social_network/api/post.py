from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from social_network.api.dependencies.services import get_post_service, get_like_service
from social_network.models import User, Post
from social_network.schemas.post import PostRead, PostCreate, LikesAnalytics
from social_network.services.like import LikeService
from social_network.services.post import PostService
from social_network.users import current_active_user

router = APIRouter()


@router.post(
    "",
    summary="Create a post",
    response_model=PostRead,
)
async def create_post(
    request_data: PostCreate,
    post_service: PostService = Depends(get_post_service),
    user: User = Depends(current_active_user),
) -> Post:
    return await post_service.create_post(request_data, user)


@router.patch(
    "/like/{post_id}",
    summary="Like a post",
    response_model=PostRead,
)
async def like_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    like_service: LikeService = Depends(get_like_service),
    user: User = Depends(current_active_user),
) -> Post:
    if not (await post_service.post_exists(post_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await like_service.like_post(user, post_id)
    return await post_service.get_post(post_id)


@router.patch(
    "/unlike/{post_id}",
    summary="Unlike a post",
    response_model=PostRead,
)
async def unlike_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    like_service: LikeService = Depends(get_like_service),
    user: User = Depends(current_active_user),
) -> Post:
    if not (await post_service.post_exists(post_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await like_service.unlike_post(user, post_id)
    return await post_service.get_post(post_id)


@router.get(
    "/analytics",
    summary="Get analytics",
    response_model=LikesAnalytics,
)
async def get_analytics(
    from_date: date,
    to_date: date,
    like_service: LikeService = Depends(get_like_service),
) -> LikesAnalytics:
    return LikesAnalytics(likes_count=await like_service.likes_made_in_range(from_date, to_date))
