import os
from typing import Optional, Tuple
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time, datetime

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY") # "00f420cd446e4019ef5cc35ec5c08d59010ffd1a8489cc11b092086849d1312d92782981794b66fa434ea292bb5387f61a008c8212114862ac2f28e90e3b33f62df99a5afe63a72835b0932c5352a2e5d67fe97eea06e1580a527f3898adb7c28c06bfee221e97b0ebf97d8d624148da8b9fc966955232338b3fd15dc6a007f8"
ALGORITHM =  "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES")) #30

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("decoded_token:",decoded_token)
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        return None

def create_token(data:dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if "user_password" in to_encode:
        del to_encode['user_password']
    if expires_delta:
        expire = time.time() + expires_delta.total_seconds()
    else:
        expire = time.time() + datetime.timedelta(minutes=15).total_seconds()
    to_encode.update({"exp": expire,"iat":datetime.datetime.now()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        if 'x-forwarded-for' not in request.headers:
            return
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            decoded_JWT = decodeJWT(credentials.credentials)
            if not decoded_JWT:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            
            lst3 = [value for value in decoded_JWT.keys() if value in ['login_id','canpebid']]
            if len(lst3)==0:
                raise HTTPException(status_code=403, detail="Missing key in authorization code.")
            return decoded_JWT
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    # def verify_jwt(self, jwtoken: str) -> bool:
    #     isTokenValid: bool = False
    #     try:
    #         payload = decodeJWT(jwtoken)
    #     except:
    #         payload = None
    #     if payload:
    #         isTokenValid = True
    #     return isTokenValid
