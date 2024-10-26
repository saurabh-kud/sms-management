from fastapi import APIRouter
from fastapi import Depends
from app.services.metrics import metrics as services
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.auth.auth import current_user
from app.db.models import User
from app.api.routes.metrics.models import QueryRequest



router = APIRouter( tags=["realtime-metrics"])



@router.get("/metrics")
def get_sessions(
    user: User = Depends(current_user),
    query_req: QueryRequest= Depends()
) -> JSONResponse:
    country=query_req.country
    response=services.get_metrics(country_code=country)
    return JSONResponse(content=jsonable_encoder(response), status_code=response.status)

