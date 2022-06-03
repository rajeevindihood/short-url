from cgitb import reset
import logging
from urllib import request

from sqlalchemy.sql.elements import and_
logger= logging.getLogger(__file__)

from fastapi import APIRouter, Depends, HTTPException, Request, params, status, Query, Request, Form
from fastapi.responses import RedirectResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.core.db_config import get_db
from app.models import model
router = APIRouter(prefix="/hash", tags=["Hash"])

import hashlib

from datetime import datetime

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
        hashQuery = db_session.query(model.Hash).filter(model.Hash.hash_key == hash).first()
        if not hashQuery:
            logger.error("Hash not found for :{}".format(hash))
            raise HTTPException(status_code=404, detail="Hash not found for :{}".format(hash))
        return hashQuery.original_key

    except Exception as e:
        print(e)
        raise HTTPException(e)

@router.post("/hashing")
async def send_zeropay_payment_request(request: Request, db_session:Session=Depends(get_db)):
    try:
        body = await request.body()
        print(body)
        response = json.loads(body.decode('utf-8'))
        hash_key = generateHash(response["text"])
        print(hash_key)
        hashObj = Hash(hash_key= hash_key, original_key= response["text"])
        db_session.add(hashObj)
        db_session.flush()
        db_session.commit()
        return hash_key
    except Exception as e:
        print(e)
        raise HTTPException(e)
