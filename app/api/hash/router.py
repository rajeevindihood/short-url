import hashlib
import os
from datetime import datetime, timedelta
from logging import getLogger
from random import randint
from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.core.constants import TZ_IST
from app.core.db_config import get_db
from app.core.errors import DuplicateDataError, ExpiredDataError, ResourceNotFoundError
from app.models import Client, HashKey, Tranch
from app.models.journey_borrower import Borrower

app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

logger = getLogger(__file__)
router = APIRouter(tags=["Hash"])


class HashKeyResponse(BaseModel):
    url: str
    slug: str
    original_key: str
    creation_date: Optional[datetime]
    expiry_date: Optional[datetime]

    class Config:
        from_attributes = True


def _generate_hash(s, char_length=8):
    """Geneate hexadecimal string with given length from a string

    >>> _generate_hash("hello world", 8)
    '309ecc48'
    """
    if char_length > 128:
        raise ValueError(f"{char_length=} exceeds 128")
    hash_object = hashlib.sha512(s.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[0:char_length]


def _get_end_of_month():
    now = datetime.now(tz=TZ_IST)
    eod = now.replace(hour=0, minute=0, second=0, microsecond=0)

    next_month = eod.replace(day=28) + timedelta(days=4)
    start_of_next_month = next_month - timedelta(days=next_month.day - 1)
    return start_of_next_month


@router.get("/{hash}")
def redirect_to_original_url(hash: str, db_session: Session = Depends(get_db)):
    try:
        obj = db_session.execute(
            select(HashKey).where(HashKey.hash_key == hash).limit(1)
        ).scalar_one()
    except NoResultFound:
        logger.exception(f"No record found for {hash=}")
        raise ResourceNotFoundError(f"This link does not exist: {hash}", HashKey)

    now = datetime.now(tz=TZ_IST).replace(tzinfo=None)

    if obj.is_enabled and obj.expiry_date and obj.expiry_date < now:
        obj.is_enabled = False
        db_session.commit()

    if not obj.is_enabled:
        logger.exception(f"Record {hash=} has expired")
        raise ExpiredDataError(f"This link has expired: {hash}")

    obj.last_visiting_time = now

    db_session.commit()

    return RedirectResponse(obj.original_key)


@router.post("/create-short-url")
def save_url(
    url: str = Body(..., embed=True),
    expiry_date: Optional[datetime] = Body(None, embed=True),  # IST
    add_salt: bool = Body(True, embed=True),
    db_session: Session = Depends(get_db),
):
    if add_salt:
        value = url + f"{randint(0, 999999)}"
    else:
        value = url

    hash_key = _generate_hash(value)

    if not expiry_date:
        expiry_date = _get_end_of_month()

    obj = HashKey(
        hash_key=hash_key,
        original_key=url,
        creation_date=datetime.now(tz=TZ_IST),
        expiry_date=expiry_date,
    )

    try:
        db_session.add(obj)
        db_session.commit()
    except IntegrityError as e:
        raise DuplicateDataError(f"Duplicate entry for {url=}", e)

    return HashKeyResponse(
        url=f"https://api.icanpe.com/{obj.hash_key}",
        slug=obj.hash_key,
        original_key=obj.original_key,
        creation_date=obj.creation_date,
        expiry_date=obj.expiry_date,
    )


# TODO: Deprecate
@router.post("/create-short-url/bulk/{tranch_id}")
def bulk_save_url(tranch_id: int, db_session: Session = Depends(get_db)):
    tranch = db_session.query(Tranch).filter(Tranch.id == tranch_id).first()

    if tranch is None:
        raise ResourceNotFoundError(f"No tranch found with {tranch_id}=", Tranch)

    all_borrs = db_session.query(Borrower).filter(Borrower.tranch_id == tranch_id)

    client = db_session.query(Client).filter(Client.id == tranch.client_id).first()

    if client is None:
        raise ResourceNotFoundError(f"No client found for {tranch_id=}")

    expiry_date = _get_end_of_month()

    for each in all_borrs:
        journey_url = f"https://{client.domain}/loan-repay/{each.canpebid}"
        hashVal = _generate_hash(journey_url)

        hash_obj = db_session.query(HashKey).filter(HashKey.hash_key == hashVal).first()

        if not hash_obj:
            hashObj = HashKey(
                hash_key=hashVal,
                original_key=journey_url,
                tranch_id=tranch_id,
                creation_date=datetime.now(tz=None),
                expiry_date=expiry_date,
            )
            each.sms_short_link = f"https://api.icanpe.com/{hashVal}"

            logger.info(
                f"Generated new url for {each.opportunity_name}: {each.sms_short_link}"
            )

            db_session.add(hashObj)

        else:
            each.sms_short_link = f"https://api.icanpe.com/{hashVal}"
            logger.info(
                f"Existing url found for {each.opportunity_name}: {each.sms_short_link}"
            )

    db_session.commit()
    return True
