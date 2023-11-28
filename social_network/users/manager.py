from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends
from fastapi_users import IntegerIDMixin, BaseUserManager
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from starlette.requests import Request
from starlette.responses import Response

from social_network.api.dependencies.db import get_user_db
from social_network.conf.settings import settings
from social_network.models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        """Update user last login time."""
        last_login = datetime.now(tz=timezone.utc)
        await self.user_db.update(user, {"last_login": last_login})


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
