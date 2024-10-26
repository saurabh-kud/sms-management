from fastapi import APIRouter
from app.api.routes.auth import auth
from app.api.routes.sessions import sessions
from app.api.routes.country_operator_pair import country_operator_pair
from app.api.routes.metrics import metrics


api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(sessions.router)
api_router.include_router(country_operator_pair.router)
api_router.include_router(metrics.router)