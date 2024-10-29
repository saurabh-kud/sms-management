from app.services.response import APIResponse
from app.error.custom_exception import CustomException
from pymongo import MongoClient
import requests


from app.config import MONGO_HOST
from app.config import SMS_HOST

# MongoDB connection
# MongoDB connection
client = MongoClient(f"mongodb://{MONGO_HOST}:27017")
db = client["sms_service"]
collection = db["countryOperator"]

MICRO1_URL = f"http://{SMS_HOST}:8001"  # Base URL of Microservice 1


def get_sessios():
    response = APIResponse()
    sessions = collection.find({})
    serialized_sessions = [
        {**session, "_id": str(session["_id"])} for session in sessions
    ]
    response.status = 200
    response.message = "Country operator fetched successfully"
    response.data = serialized_sessions
    return response


def create_country_operator_pair(country: str, operator: str, priority: str | None):
    response = APIResponse()
    request = {"country": country, "operator": operator}
    sessions = collection.find_one(request)
    if sessions:
        raise CustomException(status=409, message="Country operator pair already found")

    res = collection.insert_one(
        {
            "country": country,
            "operator": operator,
            "status": "Inactive",
            "priority": "High" if priority else "Low",
        }
    )

    if res == None:
        raise CustomException(
            status=500, message="Error while creating country operator pair"
        )
    # Retrieve the inserted document by its ID
    data = collection.find_one({"_id": res.inserted_id})
    if data is None:
        raise CustomException(
            status=500, message="Error while creating country operator pair"
        )

    # Convert `_id` to string to make it JSON serializable
    data["_id"] = str(data["_id"])

    started_session = requests.post(f"{MICRO1_URL}/start_session", json=request)

    response.status = 201
    response.message = "Country operator pair created successfully"
    response.data = data
    return response


def update_country_operator_pair(country: str, operator: str, priority: str):
    response = APIResponse()
    request = {"country": country, "operator": operator}
    session = collection.find_one(request)
    if session == None:
        raise CustomException(status=404, message="Country operator pair not found")

    res = collection.update_one(
        {"country": country, "operator": operator},
        {"$set": {"priority": priority if priority else "Low"}},
    )
    # Check if the update affected any document
    if res.matched_count == 0:
        raise CustomException(
            status=500, message="Error while updating country operator pair"
        )

    # Retrieve the updated document by its `_id`
    data = collection.find_one({"_id": session["_id"]})
    if data is None:
        raise CustomException(
            status=500, message="Error retrieving updated country operator pair"
        )

    # Convert `_id` to a string to make it JSON serializable
    data["_id"] = str(data["_id"])
    response.status = 200
    response.message = "Country operator pair updated successfully"
    response.data = data
    return response


def delete_country_operator_pair(country: str, operator: str):
    response = APIResponse()
    request = {"country": country, "operator": operator}

    # Check if the pair exists
    session = collection.find_one(request)
    if session is None:
        raise CustomException(status=404, message="Country operator pair not found")

    # Delete the document
    res = collection.delete_one(request)

    # Check if the delete operation was successful
    if res.deleted_count == 0:
        raise CustomException(
            status=500, message="Error while deleting country operator pair"
        )

    deleted_session = requests.post(f"{MICRO1_URL}/stop_session", json=request)

    # Prepare the response
    response.status = 200
    response.message = "Country operator pair deleted successfully"
    return response
