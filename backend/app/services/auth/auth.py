
from sqlalchemy.orm import Session
from app.db.models import User
from app.db import auth as DB
import bcrypt
from app.services.response import APIResponse
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.error.custom_exception import CustomException
from fastapi import Depends
from app.db.engine import get_session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    """
    Function to hash password
    """
    try:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    except Exception as e:
        raise e


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Pure function to verify password using bcrypt with error handling
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        raise e


def create_access_token(
    email: str,
) -> str:
    """Pure function to create JWT token with error handling"""
    try:
        expires_delta: timedelta = timedelta(days=7)
        expire = datetime.utcnow() + expires_delta
        payload = {"sub":email, "exp":expire}
        return jwt.encode(payload, "123456", algorithm="HS256")
    except Exception as e:
        print(str(e))


def decode_jwt(token: str) -> dict:
    """Decode the JWT token and return payload if valid."""
    try:
        payload = jwt.decode(token, "123456", algorithms="HS256")
        return payload
    except Exception as e:
        print(str(e))


def user_resposne(user:User,token:str= None):
    data= {
        "name": user.name,
        "email":user.email,
        "token": token
    }
    return data


def register(name: str, email: str,password: str,  db_session: Session):
    response = APIResponse()

    is_already_registered= DB.get_user_by_email(email=email,db_session=db_session)
    if is_already_registered:
        response.status=409
        response.message="User already registered try to sign-in"
        return response

    hassed_password =hash_password(password=password)
    user= DB.register(name=name,email=email,password=hassed_password,db_session=db_session)
    token= create_access_token(email=email)
    response.status = 201
    response.message = "User registered successfully!!"
    response.data = user_resposne(user=user,token=token)
    return response


def login(email: str,password: str,  db_session: Session):
    response = APIResponse()

    is_already_registered= DB.get_user_by_email(email=email,db_session=db_session)
    if is_already_registered is None:
        response.status=404
        response.message="User doesn't exist try to sign-Un"
        return response
    
    
    hassed_password =verify_password(plain_password=password,hashed_password=is_already_registered.password)
    if not hassed_password:
        response.status=401
        response.message="Email or password doesn't match"
        return response
    
    token= create_access_token(email=email)
    response.status = 200
    response.message = "User login successfully!!"
    response.data = user_resposne(user=is_already_registered,token=token)
    return response


async def current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_session)) -> User:
    """Middleware to get current user based on JWT token."""
    payload = decode_jwt(token)
    if payload is None:
        raise CustomException(status=401,message="Invalid token or token has expired")

    email: str = payload.get("sub")
    if email is None:
        raise CustomException(status=401,message="Invalid token payload")
    
    user= DB.get_user_by_email(email=email,db_session=db_session)
    
    if user is None:
        raise CustomException(status=401,message="User doesn't exist")
    return user