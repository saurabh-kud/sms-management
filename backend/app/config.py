import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "password"
POSTGRES_HOST = os.environ.get("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.environ.get("POSTGRES_PORT") or "5432"
POSTGRES_DB = os.environ.get("POSTGRES_DB") or "postgres"


APP_NAME = os.environ.get("APP_NAME") or "sms-management"
APP_VERSION = os.environ.get("APP_VERSION") or "0.0.1"
APP_HOST = os.environ.get("APP_HOST") or "0.0.0.0"
PORT = os.environ.get("PORT") or "8000"
PYTHON_ENV = os.environ.get("PYTHON_ENV") or "development"
DOCS_ENABLED = os.environ.get("DOCS_ENABLED") or True

JWT_SECRET = os.environ.get("JWT_SECRET") or "123456"

MONGO_HOST = os.environ.get("MONGO_HOST") or "mongo"
SMS_HOST = os.environ.get("SMS_HOST") or "sms_system"
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or ""
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") or ""
