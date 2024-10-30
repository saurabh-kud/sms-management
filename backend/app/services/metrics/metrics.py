from app.services.response import APIResponse
from app.error.custom_exception import CustomException
from pymongo import MongoClient
import requests


from app.config import MONGO_HOST

# MongoDB connection
client = MongoClient(f"mongodb://{MONGO_HOST}:27017")
db = client["sms_service"]
collection = db["sms_analytics"]
import pytz


# def get_metrics():
#     response = APIResponse()
#     sessions = collection.find({})

#     # Initialize an empty dictionary to store data grouped by country
#     country_data = {}

#     # Iterate through each document in the collection
#     for session in sessions:
#         for country_code, operator_data in session.items():
#             if country_code == "_id" or country_code == "timestamp":
#                 continue  # Skip the MongoDB document ID and handle timestamp separately

#             # Ensure the country exists in the final structure
#             if country_code not in country_data:
#                 country_data[country_code] = {"country_code": country_code, "operators": []}

#             # Add each operator's data under the respective country
#             for operator, metrics in operator_data.items():
#                 operator_entry = {
#                     "operator": operator,
#                     "attempts": metrics.get("attempts", 0),
#                     "sent": metrics.get("sent", 0),
#                     "received": metrics.get("received", 0),
#                     "confirmed": metrics.get("confirmed", 0),
#                     "success_rate": metrics.get("success_rate", 0),
#                     "SMS_success_rate": metrics.get("SMS_success_rate", 0),
#                     "confirm_rate": metrics.get("confirm_rate", 0),
#                     "timestamp": session["timestamp"].strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp
#                 }
#                 country_data[country_code]["operators"].append(operator_entry)

#     # Convert the structured data to a list for the response
#     response_data = list(country_data.values())

#     response.status = 200
#     response.message = "Data fetched successfully"
#     response.data = response_data
#     return response


# Define metrics for tracking SMS actions
from prometheus_client import Gauge

# Define metrics with labels for country and operator
sms_attempts = Gauge("sms_attempts", "Number of SMS attempts", ["country", "operator"])
sms_sent = Gauge("sms_sent", "Number of SMS sent", ["country", "operator"])
sms_received = Gauge("sms_received", "Number of SMS received", ["country", "operator"])
sms_confirmed = Gauge(
    "sms_confirmed", "Number of SMS confirmed", ["country", "operator"]
)
sms_success_rate = Gauge(
    "sms_success_rate", "Success rate of SMS", ["country", "operator"]
)
sms_confirm_rate = Gauge(
    "sms_confirm_rate", "Confirm rate of SMS", ["country", "operator"]
)


def get_metrics_old(country_code=None):
    response = APIResponse()
    sessions = collection.find({})
    print(country_code)
    # Initialize an empty dictionary to store data grouped by country
    country_data = {}

    # Iterate through each document in the collection
    for session in sessions:
        for cc, operator_data in session.items():
            if cc == "_id" or cc == "timestamp":
                continue  # Skip the MongoDB document ID and handle timestamp separately

            # If a specific country_code is provided, check if it matches
            if country_code and cc != country_code:
                continue  # Skip other countries if filtering by country_code

            # Ensure the country exists in the final structure
            if cc not in country_data:
                country_data[cc] = {"country_code": cc, "operators": []}

            # Add each operator's data under the respective country
            for operator, metrics in operator_data.items():
                operator_entry = {
                    "operator": operator,
                    "attempts": metrics.get("attempts", 0),
                    "sent": metrics.get("sent", 0),
                    "received": metrics.get("received", 0),
                    "confirmed": metrics.get("confirmed", 0),
                    "success_rate": metrics.get("success_rate", 0),
                    "SMS_success_rate": metrics.get("SMS_success_rate", 0),
                    "confirm_rate": metrics.get("confirm_rate", 0),
                    "timestamp": session["timestamp"].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),  # Format timestamp
                }
                country_data[cc]["operators"].append(operator_entry)

                sms_attempts.labels(country=cc, operator=operator).set(
                    metrics.get("attempts", 0)
                )
                sms_sent.labels(country=cc, operator=operator).set(
                    metrics.get("sent", 0)
                )
                sms_received.labels(country=cc, operator=operator).set(
                    metrics.get("received", 0)
                )
                sms_confirmed.labels(country=cc, operator=operator).set(
                    metrics.get("confirmed", 0)
                )
                sms_success_rate.labels(country=cc, operator=operator).set(
                    metrics.get("success_rate", 0)
                )
                sms_confirm_rate.labels(country=cc, operator=operator).set(
                    metrics.get("confirm_rate", 0)
                )

    # Convert the structured data to a list for the response
    response_data = list(country_data.values())

    response.status = 200
    response.message = "Data fetched successfully"
    response.data = response_data
    return response


local_tz = pytz.timezone("Asia/Kolkata")


def get_metrics(country_code=None):
    response = APIResponse()
    sessions = collection.find({})
    # Initialize an empty dictionary to store data grouped by country
    country_data = {}
    # Dictionary to track latest entry for each operator
    latest_operator_data = {}

    # Iterate through each document in the collection
    for session in sessions:
        timestamp = session.get("timestamp")
        local_timestamp = timestamp.replace(tzinfo=pytz.UTC).astimezone(local_tz)

        for cc, operator_data in session.items():
            if cc == "_id" or cc == "timestamp":
                continue

            # If a specific country_code is provided, check if it matches
            if country_code and cc != country_code:
                continue

            # Ensure the country exists in the final structure
            if cc not in country_data:
                country_data[cc] = {"country_code": cc, "operators": []}

            # Process each operator's data
            for operator, metrics in operator_data.items():
                # Create a unique key for each country-operator combination
                operator_key = f"{cc}-{operator}"

                # Create operator entry
                operator_entry = {
                    "operator": operator,
                    "attempts": metrics.get("attempts", 0),
                    "sent": metrics.get("sent", 0),
                    "received": metrics.get("received", 0),
                    "confirmed": metrics.get("confirmed", 0),
                    "success_rate": metrics.get("success_rate", 0),
                    "SMS_success_rate": metrics.get("SMS_success_rate", 0),
                    "confirm_rate": metrics.get("confirm_rate", 0),
                    "timestamp": local_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }

                # Update only if this is the first entry or if timestamp is more recent
                if (
                    operator_key not in latest_operator_data
                    or timestamp > latest_operator_data[operator_key]["timestamp"]
                ):
                    latest_operator_data[operator_key] = {
                        "data": operator_entry,
                        "timestamp": timestamp,
                        "country_code": cc,
                        "metrics": metrics,  # Store the raw metrics for Prometheus
                    }

    # Rebuild the country_data structure with only the latest entries
    # and update Prometheus metrics with only the latest data
    country_data = {}
    for operator_key, entry in latest_operator_data.items():
        cc = entry["country_code"]
        if cc not in country_data:
            country_data[cc] = {"country_code": cc, "operators": []}
        country_data[cc]["operators"].append(entry["data"])

        # Update Prometheus metrics with only the latest data
        metrics = entry["metrics"]
        operator = entry["data"]["operator"]

        # Update all Prometheus metrics at once with the latest values
        sms_attempts.labels(country=cc, operator=operator).set(
            metrics.get("attempts", 0)
        )
        sms_sent.labels(country=cc, operator=operator).set(metrics.get("sent", 0))
        sms_received.labels(country=cc, operator=operator).set(
            metrics.get("received", 0)
        )
        sms_confirmed.labels(country=cc, operator=operator).set(
            metrics.get("confirmed", 0)
        )
        sms_success_rate.labels(country=cc, operator=operator).set(
            metrics.get("success_rate", 0)
        )
        sms_confirm_rate.labels(country=cc, operator=operator).set(
            metrics.get("confirm_rate", 0)
        )

    # Convert the structured data to a list for the response
    response_data = list(country_data.values())
    response.status = 200
    response.message = "Data fetched successfully"
    response.data = response_data
    return response


def get_metrics_for_prometheus():
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

            # Add each operator's data under the respective country
            for operator, metrics in operator_data.items():
                # operator_entry = {
                #     "operator": operator,
                #     "attempts": metrics.get("attempts", 0),
                #     "sent": metrics.get("sent", 0),
                #     "received": metrics.get("received", 0),
                #     "confirmed": metrics.get("confirmed", 0),
                #     "success_rate": metrics.get("success_rate", 0),
                #     "SMS_success_rate": metrics.get("SMS_success_rate", 0),
                #     "confirm_rate": metrics.get("confirm_rate", 0),
                #     "timestamp": session["timestamp"].strftime(
                #         "%Y-%m-%d %H:%M:%S"
                #     ),  # Format timestamp
                # }
                # country_data[cc]["operators"].append(operator_entry)

                sms_attempts.labels(country=cc, operator=operator).set(
                    metrics.get("attempts", 0)
                )
                sms_sent.labels(country=cc, operator=operator).set(
                    metrics.get("sent", 0)
                )

                sms_confirmed.labels(country=cc, operator=operator).set(
                    metrics.get("confirmed", 0)
                )
                sms_success_rate.labels(country=cc, operator=operator).set(
                    metrics.get("success_rate", 0)
                )
                sms_confirm_rate.labels(country=cc, operator=operator).set(
                    metrics.get("confirm_rate", 0)
                )
