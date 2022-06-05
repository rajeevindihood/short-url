from typing import Optional
from fastapi import APIRouter, Depends,HTTPException, status, Response,Request
from fastapi.param_functions import Form

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.db_config import get_db, async_database
from app.middleware.authorizer import create_token
import datetime
import os
import requests
from pydantic import BaseModel

from app.middleware.password import verify_password
router = APIRouter(prefix="/auth/v1", tags=["Authentication"])

async def get_user(username: str):
    qstr = "SELECT login_id,user_name,user_profile,user_email,user_password FROM t_users WHERE login_id= :user_name AND is_enabled='t'"
    row = await async_database.fetch_one(qstr,{"user_name":username})
    print("my",row)
    return dict(row) if row else None


async def authenticate_user(username: str, password: str):
    print(username,password)
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user["user_password"]):
        return False
    return user

@router.post("/login")
async def login(response:Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user)
    access_token_expires = datetime.timedelta(minutes=int(os.getenv("JWT_EXPIRY_MINUTES",60)))
    access_token = create_token(data=user, expires_delta=access_token_expires)
    print("access token generated")
    # refresh_token_expires = datetime.timedelta(minutes=1440) # 24-hours
    # refresh_token = create_token(data=user, expires_delta=refresh_token_expires)
    # refresh_token_expiry = datetime.datetime.now()+refresh_token_expires
    # response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, expires= int(refresh_token_expiry.strftime("%Y%m%d%H%M%S")))

    return {"access_token": access_token, "token_type": "bearer"}

TWO_FA_API_KEY=os.getenv("2FA_API_KEY")

class GenerateOTPData(BaseModel):
    canpebid:str
    alternate_number:Optional[str]=None

@router.post("/otp-generate")
async def generate_otp(request:Request, req_data:GenerateOTPData):
    phone = req_data.alternate_number
    if not phone:
        qstr = "SELECT phone FROM journey_borrower WHERE canpebid= :canpebid"
        row = await async_database.fetch_one(qstr,{'canpebid':req_data.canpebid})
        phone = row['phone']
    url = "http://2factor.in/API/V1/{api_key}/SMS/{phone}/AUTOGEN/".format(api_key=TWO_FA_API_KEY, phone=phone)
    res = requests.get(url)
    return res.json()


@router.post("/otp-validate")
def validate_otp(request:Request, otp_input:str=Form(...), session_id:str=Form(None), canpebid:str=Form(...)):

    # By Passing OTP == Today;s DDMMYY for Sales Guys
    if(otp_input == datetime.datetime.now().strftime("%d%m%y") ):
        access_token_expires = datetime.timedelta(minutes=10)
        access_token = create_token(data={"canpebid":canpebid},expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer","status_code":200}


    url = "http://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_input}".format(api_key=TWO_FA_API_KEY, session_id=session_id, otp_input=otp_input)
    res = requests.get(url)
    #TODO: create and return access token..
    # By Passing OTP == Today;s DDMMYY for Sales Guys
    if(res.status_code==200):
        access_token_expires = datetime.timedelta(minutes=10)
        access_token = create_token(data={"canpebid":canpebid},expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer","status_code":res.status_code}
    else:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect OTP input",
            headers={"WWW-Authenticate": "Bearer"},
        )

  
   
    
   

