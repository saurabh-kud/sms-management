import argparse
import time
import random
import time
from pymongo import MongoClient
# Argument parser for country and operator
parser = argparse.ArgumentParser()
# while True:
    # parser.add_argument("--country", required=True, help="Country name")
    # parser.add_argument("--operator", required=True, help="Operator name")
    # args = parser.parse_args()

    # # Simulate processing logic for country-operator pair
    # print(f"Processing data for {args.country} and {args.operator}...")
    # time.sleep(120)  # Wait for 2 minutes (120 seconds)
    # print("running")




client = MongoClient('mongodb://mongo:27017')
db = client['sms_service']
collection = db['countryOperator']

class SendSMS:
    def __init__(self, phone_number, proxy):
        self.phone_number = phone_number
        self.proxy = proxy

    def SendOtp(self):
        # Simulate sending an OTP message
        print(f"Sending OTP to {self.phone_number} using proxy {self.proxy}...")
        time.sleep(2)  # Simulating delay for sending SMS
        response = random.choice(['sent successfully', 'failed'])  # Randomly simulate success or failure
        if 'sent successfully' in response:
            print("OTP sent successfully.")
            return True
        else:
            print("OTP sending failed.")
            return False


class SubmitSMS:
    def SubmitOtp(self, trigger_id, SMS_code):
        # Simulate submitting the OTP
        print(f"Submitting OTP {SMS_code} for trigger ID {trigger_id}...")
        time.sleep(2)  # Simulating delay for submitting OTP
        response = random.choice(['submitted successfully', 'submission failed'])  # Randomly simulate success or failure
        if 'submitted successfully' in response:
            print("OTP submitted successfully.")
            return True
        else:
            print("OTP submission failed.")
            return False


# Function to store data in MongoDB
def store_data_in_mongodb(data):
    try:
        print(f"data: {data}")
        # Connect to MongoDB (adjust URI as per your configuration)
        client = MongoClient('mongodb://mongo:27017')

        db = client['sms_service']    
        collection = db['sms_analytics']
        
        # Insert the data into MongoDB
        
        collection.insert_one(data)
        print("Data successfully stored in MongoDB.")
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")

# Simulate OTP sending and submission with data storage
def simulate_sms_process(country,operator):
    phone_number = "1234567890"
    proxy = "proxy_server"
    program_name = "program1"
    operator = "airtel"
    country_code = "IN"
    
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
            if sms_submitter.SubmitOtp(trigger_id=f"trigger_{attempt}", SMS_code=f"otp_{attempt}"):
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
                "SMS_success_rate": 0,  # Placeholder, modify as needed
                "confirm_rate": confirm_rate
            }
        }
    }

    # Store the data in MongoDB
    store_data_in_mongodb(data)

# Continuous loop to run the process every 5 minutes
def run_process_every_5_minutes():
    parser.add_argument("--country", required=True, help="Country name")
    parser.add_argument("--operator", required=True, help="Operator name")
    args = parser.parse_args()
    while True:
        simulate_sms_process(args.country,args.operator)
        print("Waiting for 5 minutes before the next iteration...")
        time.sleep(300)  # Wait for 5 minutes (300 seconds)

# Start the loop
run_process_every_5_minutes()
