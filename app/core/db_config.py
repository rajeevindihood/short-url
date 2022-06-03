import logging
logger = logging.getLogger(__name__)

import logging
logger=logging.getLogger("db_config")
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases

from app.core.singleton_pattern import singleton
from threading import Lock
@singleton
class Counter:
    def __init__(self) -> None:
        self.lock = Lock()
        self.counter = 0
    
    def increment(self):
        self.lock.acquire()
        self.counter+=1
        self.lock.release()
        return self.counter

DATABASE_TYPE=os.getenv("DATABASE_TYPE",None)
DATABASE_USER=os.getenv("DATABASE_USER",None)
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD",None)
DATABASE_HOST=os.getenv("DATABASE_HOST",None)
DATABASE_PORT=os.getenv("DATABASE_PORT",None)
DATABASE_NAME=os.getenv("DATABASE_NAME",None)

DATABASE_URL = "postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}".format(DATABASE_USER=DATABASE_USER, DATABASE_PASSWORD=DATABASE_PASSWORD,DATABASE_HOST=DATABASE_HOST,DATABASE_PORT=DATABASE_PORT,DATABASE_NAME=DATABASE_NAME)
logger.info("Connecting to database:{}".format(DATABASE_URL))
DATABASE_URL2 = "postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}".format(DATABASE_USER=DATABASE_USER, DATABASE_PASSWORD=DATABASE_PASSWORD,DATABASE_HOST=DATABASE_HOST,DATABASE_PORT=DATABASE_PORT,DATABASE_NAME=DATABASE_NAME)
async_database = databases.Database(DATABASE_URL2, min_size=5, max_size=20)
engine = create_engine(DATABASE_URL, pool_recycle=3600, pool_size=20,max_overflow=20, connect_args={"options": "-c timezone=Asia/Calcutta"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency injection method
def get_db():
    try:
        counter = Counter().increment()
        logger.info("Allocated db conneciton for request:{}".format(counter))
        db = SessionLocal()
        yield db
    finally:
        logger.info("De-Allocated db conneciton for request:{}".format(counter))
        db.close()
