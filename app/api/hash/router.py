import hashlib
from datetime import datetime, timedelta
from logging import getLogger

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.db_config import get_db
from app.models import model

# TODO: Use TZ_IST & TZ_UTC
try:
    from zoneinfo import ZoneInfo
except (ImportError, ModuleNotFoundError):
    from backports.zoneinfo import ZoneInfo

import os

from app.models.model import Hash

app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

logger = getLogger(__file__)
router = APIRouter(tags=["Hash"])


# dependencies=[Depends(JWTBearer())]
def generateHash(s, char_length=8):
    """Geneate hexadecimal string with given length from a string

    >>> short_str("hello world", 8)
    '309ecc48'
    """
    if char_length > 128:
        raise ValueError("char_length {} exceeds 128".format(char_length))
    hash_object = hashlib.sha512(s.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[0:char_length]


@router.get("/{hash}")
def get_random_string(
    request: Request, hash: str, db_session: Session = Depends(get_db)
):
    """Returns a  string of length string_length."""
    try:
        hashQuery = (
            db_session.query(model.Hash)
            .filter(
                model.Hash.hash_key == hash,
                model.Hash.expiry_date >= datetime.now(tz=ZoneInfo("Asia/Kolkata")),
            )
            .first()
        )
        print(hashQuery)
        if not hashQuery:
            hashQuery2 = (
                db_session.query(model.Hash).filter(model.Hash.hash_key == hash).first()
            )
            if not hashQuery2:
                logger.error("Hash not found for :{}".format(hash))
                return HTTPException(
                    status_code=404, detail="Hash not found for :{}".format(hash)
                )
            else:
                hashQuery2.is_enabled = False
                db_session.flush()
                logger.error("The link has already expired")
                return HTTPException(status_code=410, detail="The link has expired")

        visitingTime = datetime.now(tz=ZoneInfo("Asia/Kolkata"))

        hashQuery.last_visiting_time = visitingTime
        db_session.commit()
        return RedirectResponse(hashQuery.original_key)

    except Exception as e:
        logger.error("Exception: ", e)
        raise HTTPException(status_code=404, detail="No such keys found")


# , dependencies=[Depends(JWTBearer())]


def _get_end_of_month():
    now = datetime.now(tz=ZoneInfo("Asia/Kolkata"))
    eod = now.replace(hour=0, minute=0, second=0, microsecond=0)

    next_month = eod.replace(day=28) + timedelta(days=4)
    start_of_next_month = next_month - timedelta(days=next_month.day - 1)
    return start_of_next_month


@router.post("/create-short-url")
async def save_url(
    url: str = Body(..., embed=True), db_session: Session = Depends(get_db)
):
    try:
        hash_key = generateHash(url)
        expiry_date = _get_end_of_month()
        hashObj = Hash(
            hash_key=hash_key,
            original_key=url,
            creation_date=datetime.now(tz=ZoneInfo("Asia/Kolkata")),
            expiry_date=expiry_date,
        )  # type: ignore
        db_session.add(hashObj)
        db_session.flush()
        db_session.commit()
        return hashObj.hash_key

    except Exception as e:
        logger.info("Exception: ", e)
        return hash_key


@router.post("/create-short-url/bulk/{tranch_id}")
async def bulk_save_url(
    request: Request, tranch_id: int, db_session: Session = Depends(get_db)
):
    all_borrs = db_session.query(model.Borrower).filter(
        model.Borrower.tranch_id == tranch_id
    )
    tranch = db_session.query(model.Tranch).filter(model.Tranch.id == tranch_id).first()
    client = (
        db_session.query(model.Client)
        .filter(model.Client.id == tranch.client_id)
        .first()
    )

    expiry_date = datetime.now(tz=None).replace(day=28) + timedelta(days=4)
    expiry_date = expiry_date - timedelta(days=expiry_date.day)

    for each in all_borrs:
        journey_url = "https://{host}/loan-repay/{canpebid}".format(
            host=client.domain, canpebid=each.canpebid
        )
        hashVal = generateHash(journey_url)

        hash_obj = (
            db_session.query(model.Hash).filter(model.Hash.hash_key == hashVal).first()
        )
        if not hash_obj:
            print("No existing Url found for {}".format(each.opportunity_name))
            hashObj = Hash(
                hash_key=hashVal,
                original_key=journey_url,
                tranch_id=tranch_id,
                creation_date=datetime.now(tz=None),
                expiry_date=expiry_date,
            )
            # each.sms_short_link = "https://api-staging.icanpe.com/short-url/{}".format(hashVal)
            each.sms_short_link = "https://api.icanpe.com/{}".format(hashVal)

            print(each.sms_short_link)
            db_session.add(hashObj)
            db_session.flush()

        else:
            print(
                "existing Url found for {} - {}".format(
                    each.opportunity_name, each.sms_short_link
                )
            )

    db_session.commit()
    return True
