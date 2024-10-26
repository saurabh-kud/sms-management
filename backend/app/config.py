import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "password"
POSTGRES_HOST = os.environ.get("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.environ.get("POSTGRES_PORT") or "5436"
POSTGRES_DB = os.environ.get("POSTGRES_DB") or "sms_management"


APP_NAME = os.environ.get("APP_NAME") or "sms-management"
APP_VERSION = os.environ.get("APP_VERSION") or "0.0.1"
APP_HOST = os.environ.get("APP_HOST") or "0.0.0.0"
PORT = os.environ.get("PORT") or "8080"
PYTHON_ENV = os.environ.get("PYTHON_ENV") or "development"
DOCS_ENABLED = os.environ.get("DOCS_ENABLED") or True
