from datetime import datetime
from logging import getLogger
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.db_config import get_db
from app.core.constants import TZ_IST

logger = getLogger(__file__)

router = APIRouter(prefix="/sys", tags=["System Status"])

_version = None


def get_server_version():
    global _version

    if not _version:
        version_path = Path("app/version.txt")

        if version_path.is_file():
            _version = version_path.read_text().strip()
        else:
            _version = "HEAD"

    return _version


@router.get("/version")
def sys_version_handler():
    return {"version": get_server_version()}


@router.get("/healthcheck")
def sys_healthcheck_handler(db_session: Session = Depends(get_db)):
    # Get version
    version = get_server_version()

    # Get system time
    try:
        system_time = datetime.now(TZ_IST)
    except Exception:
        system_time = None

    # Check if database connection is working
    database_time = None
    database_time = db_session.query(func.now()).scalar()

    if None in [version, system_time, database_time]:
        healthcheck = "FAILED"
    else:
        healthcheck = "PASSED"

    payload = {
        "version": str(version),
        "system_time": str(system_time),
        "database_time": str(database_time),
        "healthcheck": str(healthcheck),
    }

    if healthcheck == "PASSED":
        return {"detail": payload}
    else:
        raise HTTPException(status_code=500, detail=payload)
