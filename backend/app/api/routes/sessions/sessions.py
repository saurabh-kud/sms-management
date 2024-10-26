from fastapi import APIRouter
from fastapi import Depends
from app.services.sessions import sessions as services
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.auth.auth import current_user
from app.db.models import User
from app.api.routes.sessions.models import SessionRequest


router = APIRouter( tags=["sessions"])


@router.get("/sessions")
def get_sessions(
    user: User = Depends(current_user),
) -> JSONResponse:
    response=services.get_sessios()
    return JSONResponse(content=jsonable_encoder(response), status_code=response.status)


@router.post("/session/start")
def start_session(
    user: User = Depends(current_user),
    session_request: SessionRequest= SessionRequest
) -> JSONResponse:
    country= session_request.country
    operator= session_request.operator
    response=services.start_session(country=country,operator=operator)
    return JSONResponse(content=jsonable_encoder(response), status_code=200)


@router.post("/session/stop")
def stop_session(
    user: User = Depends(current_user),
    session_request: SessionRequest= SessionRequest
) -> JSONResponse:
    country= session_request.country
    operator= session_request.operator
    response=services.stop_session(country=country,operator=operator)
    return JSONResponse(content=jsonable_encoder(response), status_code=200)


@router.post("/session/restart")
def restart_session(
    user: User = Depends(current_user),
    session_request: SessionRequest= SessionRequest
) -> JSONResponse:
    country= session_request.country
    operator= session_request.operator
    response=services.restart_session(country=country,operator=operator)
    return JSONResponse(content=jsonable_encoder(response), status_code=200)