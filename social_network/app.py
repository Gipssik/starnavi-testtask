from fastapi import FastAPI

from social_network.api import post, user
from social_network.conf.settings import settings
from social_network.middlewares import init_middlewares
from social_network.schemas.user import UserRead, UserCreate
from social_network.users import fastapi_users, auth_backend


def init_routes(app: FastAPI) -> None:
    app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/api/auth/jwt", tags=["auth"])
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/api/auth",
        tags=["auth"],
    )
    app.include_router(user.router, prefix="/api/user", tags=["user"])
    app.include_router(post.router, prefix="/api/post", tags=["post"])


def get_app() -> FastAPI:
    app = FastAPI()
    init_routes(app)
    init_middlewares(app, settings)
    return app
