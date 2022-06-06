from cgitb import reset
from datetime import datetime, timedelta
import logging
from sqlite3 import IntegrityError
from urllib import request

logger= logging.getLogger(__file__)

from fastapi import APIRouter, Depends, HTTPException, Request, params, status, Query, Request, Form
from fastapi.responses import RedirectResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.core.db_config import get_db
from app.models import model


import hashlib

import json

try:
    from zoneinfo import ZoneInfo
except:
    from backports.zoneinfo import ZoneInfo
from urllib.parse import unquote, quote_plus, urlencode,urlparse, parse_qs

from app.middleware.authorizer import JWTBearer

import requests
import os
from app.models.model import Hash

app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

router = APIRouter(prefix="/v1", tags=["Hash"], dependencies=[Depends(JWTBearer())])

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
def get_random_string(request:Request, hash: str, db_session: Session=Depends(get_db)):
    """Returns a  string of length string_length."""
    try:
        hashQuery = db_session.query(model.Hash).filter(model.Hash.hash_key == hash, model.Hash.expiry_date >= datetime.now(tz=ZoneInfo('Asia/Kolkata'))).first()
        if not hashQuery:
            hashQuery2 = db_session.query(model.Hash).filter(model.Hash.hash_key == hash).first()
            if not hashQuery2:
                logger.error("Hash not found for :{}".format(hash))
                raise HTTPException(status_code=404, detail="Hash not found for :{}".format(hash))
            else:
                hashQuery.is_enabled = False
                db_session.flush()
                raise HTTPException(status_code=410, detail="The link has expired")
        
        visitingTime = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        
        hashQuery.last_visiting_time = visitingTime
        db_session.commit()
        return RedirectResponse(hashQuery.original_key)

    except Exception as e:
        logger.error("Exception: ", e)
        raise HTTPException(status_code=404, detail="No such keys found")

@router.post("/", dependencies=[Depends(JWTBearer())])
async def send_zeropay_payment_request(request: Request, db_session:Session=Depends(get_db)):
    try:
        body = await request.body()
        response = json.loads(body.decode('utf-8'))
        hash_key = generateHash(response["text"])
        expiry_date = datetime.now(tz=ZoneInfo('Asia/Kolkata')).replace(day=28) + timedelta(days=4) 
        expiry_date = expiry_date - timedelta(days=expiry_date.day)
        print(expiry_date)
        print(datetime.now(tz=ZoneInfo('Asia/Kolkata')))
        hashObj = Hash(hash_key= hash_key, original_key= response["text"], creation_date=datetime.now(tz=ZoneInfo('Asia/Kolkata')), expiry_date=expiry_date)
        db_session.add(hashObj)
        db_session.flush()
        db_session.commit()
        return hash_key
    except Exception as e:
        logger.info("Exception: ", e)
        return hash_key
    
    
    
        
    