
from sqlalchemy.orm import Session
from app.db.models import User
from app.error.custom_exception import CustomException
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import RowMapping

def register(
    name: str,
    email: str,
    password:str,
    db_session: Session,
) -> User:
    """Function to create a user record"""
    try:
        user= User(name=name,email=email,password=password)
        db_session.add(user)
        db_session.commit()
        return user
    except Exception as e:
        print(e)
        raise CustomException()


def get_user_by_email(email: str,db_session:Session) -> User:

    """Function to get user  by email"""
    try:
        query= select(User).where(User.email==email)
        result = db_session.execute(query).scalars().one_or_none()
        return result
    
    except Exception as e:
        print(e)
        raise CustomException()