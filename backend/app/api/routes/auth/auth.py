from fastapi import APIRouter
from fastapi import Depends
from app.db.engine import get_session
from sqlalchemy.orm import Session
from app.api.routes.auth.models import RegisterRequest
from app.api.routes.auth.models import LoginRequest
from app.services.auth import auth as services
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.auth.auth import current_user
from app.db.models import User


router = APIRouter( tags=["Auth"])


@router.post("/register")
def register(
    db_session: Session = Depends(get_session),
    register_request: RegisterRequest = RegisterRequest,
) -> JSONResponse:
    name=register_request.name
    email= register_request.email
    password= register_request.password
    response=services.register(name=name,email=email,password=password,db_session=db_session)
    return JSONResponse(content=jsonable_encoder(response), status_code=response.status)


@router.post("/login")
def register(
    db_session: Session = Depends(get_session),
    login_request: LoginRequest = LoginRequest,
) -> JSONResponse:
    email= login_request.email
    password= login_request.password
    response=services.login(email=email,password=password,db_session=db_session)
    return JSONResponse(content=jsonable_encoder(response), status_code=response.status)


@router.get("/me")
def register(
    user: User = Depends(current_user),
) -> JSONResponse:
    user_updated={"name":user.name,"email": user.email}
    return JSONResponse(content=jsonable_encoder(user_updated), status_code=200)