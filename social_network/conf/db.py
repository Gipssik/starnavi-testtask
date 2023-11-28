from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from social_network.conf.settings import settings

engine = create_async_engine(settings.sqlalchemy_database_uri)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
