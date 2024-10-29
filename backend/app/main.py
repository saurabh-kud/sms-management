from fastapi import FastAPI, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.error.custom_exception import CustomException
from app.error.handler import validation_exception_handler
from app.error.handler import value_error_handler
from app.error.handler import custom_error_handler
import time
import uvicorn

# from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client
from fastapi import Response


startTime = time.time()
from app.config import APP_NAME
from app.config import APP_HOST
from app.config import PYTHON_ENV
from app.config import APP_VERSION
from app.config import PORT
from app.config import DOCS_ENABLED
from app.utils import custom_handler
from app.utils.uptime import getUptime

from app.api.main import api_router
from app.services.alert_service.alert_service import DatabaseMonitor


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="advanced chatbot for your files",
    docs_url="/api/docs" if DOCS_ENABLED else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

monitor = DatabaseMonitor()


@app.on_event("startup")
async def startup_event():
    try:
        monitor.start_monitoring()
    except Exception as e:
        print(f"Failed to start monitoring: {e}")
        raise e


# @app.exception_handler(custom_handler.CustomException)
# async def handle_custom_exception(request, exc: custom_handler.CustomException):
#     return JSONResponse(status_code=exc.status_code, content={"error": exc.msg})


app.add_exception_handler(CustomException, custom_error_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Route"])
async def health_route(req: Request):
    """
    Health Route : Returns App details.
    """
    return JSONResponse(
        {
            "app": APP_NAME,
            "version": "v" + APP_VERSION,
            "ip": req.client.host,
            "uptime": getUptime(startTime),
            # "database": "connected" if is_db_connected() else "disconnected",
            "mode": PYTHON_ENV,
        }
    )


app.include_router(api_router)


@app.get("/metrics")
def get_metrics():
    return Response(
        content=prometheus_client.generate_latest(), media_type="text/plain"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
