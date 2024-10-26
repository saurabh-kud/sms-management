from app.services.response import APIResponse
from app.error.custom_exception import CustomException
from pymongo import MongoClient
import requests

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['sms_service']
collection = db['sms_analytics']



from pymongo import MongoClient
from app.services.response import APIResponse
from app.error.custom_exception import CustomException

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['sms_service']
collection = db['sms_analytics']



from pymongo import MongoClient
from app.services.response import APIResponse
from app.error.custom_exception import CustomException

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['sms_service']
collection = db['sms_analytics']



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



def get_metrics(country_code=None):
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
                    "timestamp": session["timestamp"].strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp
                }
                country_data[cc]["operators"].append(operator_entry)

    # Convert the structured data to a list for the response
    response_data = list(country_data.values())

    response.status = 200
    response.message = "Data fetched successfully"
    response.data = response_data
    return response
