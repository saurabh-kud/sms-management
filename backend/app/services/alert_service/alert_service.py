from pymongo import MongoClient


from app.config import MONGO_HOST
from app.config import TELEGRAM_BOT_TOKEN
from app.config import TELEGRAM_CHAT_ID


# MongoDB connection
client = MongoClient(f"mongodb://{MONGO_HOST}:27017")
db = client["sms_service"]
collection = db["alert"]


from apscheduler.schedulers.background import BackgroundScheduler
from telegram.request import HTTPXRequest
import telegram
import asyncio
from datetime import datetime
import logging

trequest = HTTPXRequest(connection_pool_size=20)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseMonitor:
    def __init__(self):
        # Telegram configuration
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.bot = telegram.Bot(token=self.bot_token, request=trequest)

        # Threshold configuration
        self.threshold = 50

        # Initialize scheduler
        self.scheduler = BackgroundScheduler()

    async def send_telegram_alert(self, message):
        """Send alert message to Telegram."""
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            logger.info("Alert sent successfully")
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")

    def check_database(self):
        """Query database and check against threshold."""
        print("db called")
        try:

            alerts_data = collection.find({})
            logger.info(f"alert data all {alerts_data}")

            serialized_alerts = [
                {**alert, "_id": str(alert["_id"])} for alert in alerts_data
            ]

            for alert in serialized_alerts:
                country = alert.get("country")
                operator = alert.get("operator")
                success_rate = alert.get("success_rate", 0)
                attempts = alert.get("attempts", 0)
                sent_count = alert.get("sent", 0)
                if success_rate <= 70:
                    message = (
                        f"⚠️ Alert! Low Success Rate\n\n"
                        f"Country: {country}\n"
                        f"Operator: {operator}\n"
                        f"Success Rate: {success_rate}%\n"
                        f"Attempts: {attempts}\n"
                        f"Sent: {sent_count}\n"
                    )
                    logger.info(f"\n\nteligram message sent {message}\n\n")
                    # Create event loop for async telegram message
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.send_telegram_alert(message))
                    loop.close()

            collection.delete_many({})
        except Exception as e:
            logger.error(f"Database query failed: {e}")

    def start_monitoring(self):
        """Start the monitoring schedule."""
        try:
            self.scheduler.add_job(
                self.check_database, "interval", minutes=10, id="database_monitor"
            )
            self.scheduler.start()
            logger.info("Monitoring started successfully")
        except Exception as e:
            logger.error(f"Failed to start monitoring: {e}")

    def stop_monitoring(self):
        """Stop the monitoring schedule."""
        self.scheduler.shutdown()
        logger.info("Monitoring stopped")


# Usage example
