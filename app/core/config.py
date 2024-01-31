# Store all configuration in this file
# Constants in the _Env class will be automatically
# read from the environment

import logging
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings

logger = logging.getLogger(__file__)


class _Env(BaseSettings):
    DATABASE_TYPE: str
    DATABASE_USER: str
    DATABASE_PASSWORD: SecretStr
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    # SYSTEM_USER_NAME: str
    # SYSTEM_USER_PASS: SecretStr

    # BACKEND_SERVICE_DOMAIN: str
    # NOTIFICATION_SERVICE: str

    SENTRY_DSN: Optional[str] = None


ENV = _Env()  # pyright: ignore -- the required fields will be read from the environment


logger.info("Loaded environment variables")
logger.info(f"ENV: {ENV.model_dump_json()}")
