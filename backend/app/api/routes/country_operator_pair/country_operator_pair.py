from fastapi import APIRouter
from fastapi import Depends
from app.db.engine import get_session
from sqlalchemy.orm import Session
from app.services.country_operator_pair import country_operator_pair as services
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.auth.auth import current_user
from app.db.models import User
from app.api.routes.sessions.models import SessionRequest
from app.api.routes.country_operator_pair.models import CountryOperatorPairRequest


router = APIRouter( tags=["country-operator-pair"])


@router.get("/country")
def get_sessions(
    user: User = Depends(current_user),
) -> JSONResponse:
    response=services.get_sessios()
    return JSONResponse(content=jsonable_encoder(response), status_code=response.status)


@router.post("/country/create")
def create_country_operator_pair(
    user: User = Depends(current_user),
    country_request: CountryOperatorPairRequest= CountryOperatorPairRequest
) -> JSONResponse:
    country= country_request.country
    operator= country_request.operator
    priority=country_request.priority
    response=services.create_country_operator_pair(country=country,operator=operator,priority=priority)
    return JSONResponse(content=jsonable_encoder(response), status_code=200)


@router.put("/country/update")
def update_country_operator_pair(
    user: User = Depends(current_user),
    country_request: CountryOperatorPairRequest= CountryOperatorPairRequest

) -> JSONResponse:
    country= country_request.country
    operator= country_request.operator
    priority=country_request.priority
    response=services.update_country_operator_pair(country=country,operator=operator,priority=priority)
    return JSONResponse(content=jsonable_encoder(response), status_code=200)


@router.post("/country/delete")
def delete_country_operator_pair(
    user: User = Depends(current_user),
    session_request: SessionRequest= SessionRequest
) -> JSONResponse:
    country= session_request.country
    operator= session_request.operator
    response=services.delete_country_operator_pair(country=country,operator=operator)
    return JSONResponse(content=jsonable_encoder(response), status_code=200)