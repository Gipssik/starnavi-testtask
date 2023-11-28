from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from social_network.conf.settings import SocialNetworkSettings


def init_middlewares(app: FastAPI, app_settings: SocialNetworkSettings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
