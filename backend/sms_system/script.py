import argparse
import time
from datetime import datetime
import random
from pymongo import MongoClient
import random
import time

# Argument parser for country and operator
parser = argparse.ArgumentParser()
parser.add_argument("--country", required=True, help="Country name")
parser.add_argument("--operator", required=True, help="Operator name")
args = parser.parse_args()
print(f"Processing data for {args.country} and {args.operator}...")

client = MongoClient("mongodb://mongo:27017")
db = client["sms_service"]
collection = db["countryOperator"]


class SendSMS:
    def __init__(self, phone_number, proxy):
        self.phone_number = phone_number
        self.proxy = proxy

    def SendOtp(self):
        # Set a high success rate of 90%
        success_rate = (
            0.9 if random.random() < 0.95 else 0.5
        )  # 95% of the time, it uses 90% success rate
        success = random.random() < success_rate
        print(
            f"Sending OTP to {self.phone_number} using proxy {self.proxy}... Result: {'Success' if success else 'Failure'}"
        )
        time.sleep(2)  # Simulating delay for sending SMS
        return success


class SubmitSMS:
    def SubmitOtp(self, trigger_id, SMS_code):
        # Set a high confirm rate of 90%
        confirm_rate = (
            0.9 if random.random() < 0.95 else 0.5
        )  # 95% of the time, it uses 90% confirm rate
        success = random.random() < confirm_rate
        print(
            f"Submitting OTP {SMS_code} for trigger ID {trigger_id}... Result: {'Success' if success else 'Failure'}"
        )
        time.sleep(2)  # Simulating delay for submitting OTP
        return success


# Function to store data in MongoDB
def store_data_in_mongodb(data):
    try:
        print(f"Processing data for {args.country} and {args.operator}...")
        print(f"Data: {data}")
        # Connect to MongoDB
        client = MongoClient("mongodb://mongo:27017")
        db = client["sms_service"]
        collection = db["sms_analytics"]

        # Insert the data into MongoDB
        data["timestamp"] = datetime.utcnow()
        collection.insert_one(data)
        print("Data successfully stored in MongoDB.")
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")


# Function to store data in MongoDB
def store_alert_data_in_mongodb(data):
    try:
        print(f"Processing data for {args.country} and {args.operator}...")
        print(f"Data: {data}")
        # Connect to MongoDB
        client = MongoClient("mongodb://mongo:27017")
        db = client["sms_service"]
        collection = db["alert"]

        # Insert the data into MongoDB
        data["timestamp"] = datetime.utcnow()
        collection.insert_one(data)
        print("Data successfully stored in MongoDB.")
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")


# Simulate OTP sending and submission with data storage
def simulate_sms_process():
    phone_number = "1234567890"
    proxy = "proxy_server"
    operator = args.operator
    country_code = args.country

    # Initialize SMS sender and submitter
    sms_sender = SendSMS(phone_number, proxy)
    sms_submitter = SubmitSMS()

    # Track attempts and results
    attempts = 30
    sent_count = 0
    received_count = 0
    confirmed_count = 0

    # Simulate OTP sending process
    for attempt in range(attempts):
        if sms_sender.SendOtp():
            sent_count += 1
            # Simulate OTP submission process
            if sms_submitter.SubmitOtp(
                trigger_id=f"trigger_{attempt}", SMS_code=f"otp_{attempt}"
            ):
                confirmed_count += 1

    # Calculate success rates
    success_rate = (sent_count / attempts) * 100
    confirm_rate = (confirmed_count / sent_count) * 100 if sent_count > 0 else None

    # Prepare data for MongoDB
    data = {
        country_code: {
            operator: {
                "attempts": attempts,
                "sent": sent_count,
                "received": received_count,
                "confirmed": confirmed_count,
                "success_rate": success_rate,
                "SMS_success_rate": 0,
                "confirm_rate": confirm_rate,
            }
        }
    }

    # Store the data in MongoDB
    store_data_in_mongodb(data)
    if success_rate <= 70:
        alert_data = {
            "country": country_code,
            "operator": operator,
            "attempts": attempts,
            "sent": sent_count,
            "confirmed": confirmed_count,
            "success_rate": success_rate,
            "confirm_rate": confirm_rate,
        }
        store_alert_data_in_mongodb(data=alert_data)


# Continuous loop to run the process every 5 minutes
def run_process_every_2_minutes():
    while True:
        simulate_sms_process()
        print("Waiting for 5 minutes before the next iteration...")
        time.sleep(120)  # Wait for 2 minutes (120 seconds)


# Start the loop
run_process_every_2_minutes()
