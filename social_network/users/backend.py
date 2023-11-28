from datetime import datetime, timezone
from typing import Optional

from fastapi_users import BaseUserManager, models
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from social_network.conf.settings import settings


class TrackedJWTStrategy(JWTStrategy):
    async def read_token(
        self,
        token: Optional[str],
        user_manager: BaseUserManager[models.UP, models.ID],
    ) -> Optional[models.UP]:
        """Update user last request time."""
        user = await super().read_token(token, user_manager)
        if user is not None:
            last_request = datetime.now(tz=timezone.utc)
            await user_manager.user_db.update(user, {"last_request": last_request})
        return user


def get_jwt_strategy() -> TrackedJWTStrategy:
    return TrackedJWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME_SECONDS)


bearer_transport = BearerTransport(tokenUrl="api/auth/jwt/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
