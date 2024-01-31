from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from .config import ENV

DATABASE_URL = "postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}".format(
    DATABASE_USER=ENV.DATABASE_USER,
    DATABASE_PASSWORD=ENV.DATABASE_PASSWORD.get_secret_value(),
    DATABASE_HOST=ENV.DATABASE_HOST,
    DATABASE_PORT=ENV.DATABASE_PORT,
    DATABASE_NAME=ENV.DATABASE_NAME,
)

SQLA_ASYNC_DB_URL = URL.create(
    "postgresql+asyncpg",
    username=ENV.DATABASE_USER,
    password=ENV.DATABASE_PASSWORD.get_secret_value(),
    host=ENV.DATABASE_HOST,
    port=int(ENV.DATABASE_PORT),
    database=ENV.DATABASE_NAME,
)

engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=20,
    connect_args={"options": "-c timezone=Asia/Calcutta"},
)

async_engine = create_async_engine(
    SQLA_ASYNC_DB_URL,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=20,
)

DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

AsyncDbSession = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=async_engine
)


# Dependency injection method
def get_db():
    db = None
    try:
        db = DbSession()
        yield db
    finally:
        if db is not None:
            db.close()


async def get_async_db():
    async with AsyncDbSession() as session:
        yield session
