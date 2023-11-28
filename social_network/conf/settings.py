from pydantic.v1 import BaseSettings


class SocialNetworkSettings(BaseSettings):
    DB_NAME: str = "network"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_DRIVER: str = "postgresql+asyncpg"

    SECRET_KEY: str = "secret"
    ALLOWED_ORIGINS: list = ["*"]

    ACCESS_TOKEN_LIFETIME_SECONDS: int = 60 * 60 * 24 * 7

    @property
    def sqlalchemy_database_uri(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = SocialNetworkSettings()
