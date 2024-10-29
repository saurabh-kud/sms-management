from pymongo import MongoClient


from app.config import MONGO_HOST
from app.config import TELEGRAM_BOT_TOKEN
from app.config import TELEGRAM_CHAT_ID


# MongoDB connection
client = MongoClient(f"mongodb://{MONGO_HOST}:27017")
db = client["sms_service"]
collection = db["sms_analytics"]


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

            sessions = collection.find({})
            # Initialize an empty dictionary to store data grouped by country
            country_data = {}

            # Iterate through each document in the collection
            for session in sessions:
                for cc, operator_data in session.items():
                    if cc == "_id" or cc == "timestamp":
                        continue  # Skip the MongoDB document ID and handle timestamp separately

                    # Ensure the country exists in the final structure
                    if cc not in country_data:
                        country_data[cc] = {"country_code": cc, "operators": []}

                    for operator, metrics in operator_data.items():

                        operator_list = country_data.get(cc).get("operators")
                        logger.info(f"operator list {operator_list}")

                        if operator not in operator_list:
                            logger.info(f"operator list inside if {operator_list}")

                            success_rate = metrics.get("success_rate", 0)
                            if success_rate and success_rate < 50:
                                message = (
                                    f"⚠️ Alert! Threshold exceeded!\n"
                                    f"Current value: {success_rate}\n"
                                    f"Threshold: {self.threshold}\n"
                                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                )
                                message = (
                                    f"⚠️ Alert! Low Success Rate\n\n"
                                    f"Country: {cc}\n"
                                    f"Operator: {operator}\n"
                                    f"Success Rate: {success_rate}%\n"
                                    f"Attempts: {metrics.get('attempts', 0)}\n"
                                    f"Sent: {metrics.get('sent', 0)}\n"
                                    f"Confirmed: {metrics.get('confirmed', 0)}\n"
                                    f"Time: {session['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
                                )
                                logger.info(f"\n\nteligram message sent {message}\n\n")
                                # Create event loop for async telegram message
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                                loop.run_until_complete(
                                    self.send_telegram_alert(message)
                                )
                                loop.close()

                            country_data[cc]["operators"].append(operator)

                        # final_data[operator] = metrics

                        # if counter > 0:
                        #     break
                        # counter += 1

                        # success_rate = metrics.get("success_rate", 0)
                        # logger.info(f"success rate: {success_rate}")

                        # if success_rate and success_rate < 50:
                        #     message = (
                        #         f"⚠️ Alert! Threshold exceeded!\n"
                        #         f"Current value: {success_rate}\n"
                        #         f"Threshold: {self.threshold}\n"
                        #         f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        #     )
                        #     message = (
                        #         f"⚠️ <b>Low Success Rate Alert</b>\n\n"
                        #         f"Country: {cc}\n"
                        #         f"Operator: {operator}\n"
                        #         f"Success Rate: {success_rate}%\n"
                        #         f"Attempts: {metrics.get('attempts', 0)}\n"
                        #         f"Sent: {metrics.get('sent', 0)}\n"
                        #         f"Confirmed: {metrics.get('confirmed', 0)}\n"
                        #         f"Time: {session['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
                        #     )
                        # Create event loop for async telegram message
                        # loop = asyncio.new_event_loop()
                        # asyncio.set_event_loop(loop)
                        # loop.run_until_complete(self.send_telegram_alert(message))
                        # loop.close()
        except Exception as e:
            logger.error(f"Database query failed: {e}")

    def start_monitoring(self):
        """Start the monitoring schedule."""
        try:
            self.scheduler.add_job(
                self.check_database, "interval", minutes=1, id="database_monitor"
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
