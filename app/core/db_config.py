from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import ENV

DATABASE_URL = (
    "postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}".format(
        USER=ENV.DATABASE_USER,
        PASSWORD=ENV.DATABASE_PASSWORD.get_secret_value(),
        HOST=ENV.DATABASE_HOST,
        PORT=ENV.DATABASE_PORT,
        DATABASE_NAME=ENV.DATABASE_NAME,
    )
)

engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=20,
    connect_args={"options": "-c timezone=Asia/Calcutta"},
)

DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency injection method
def get_db():
    db = None
    try:
        db = DbSession()
        yield db
    finally:
        if db is not None:
            db.close()
