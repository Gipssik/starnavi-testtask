from fastapi import APIRouter, Depends

from social_network.models import User
from social_network.schemas.user import UserActivity
from social_network.users import current_active_user

router = APIRouter()


@router.get(
    "/activity",
    summary="Get user activity",
    response_model=UserActivity,
)
async def get_user_activity(user: User = Depends(current_active_user)) -> UserActivity:
    return UserActivity(last_login=user.last_login, last_request=user.last_request)
