from app.services.response import APIResponse
from app.error.custom_exception import CustomException
from pymongo import MongoClient
import requests

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['sms_service']
collection = db['countryOperator']

MICRO1_URL = "http://localhost:8001"  # Base URL of Microservice 1




def get_sessios():
    response = APIResponse()
    sessions=collection.find({})
    serialized_sessions = [
        {**session, "_id": str(session["_id"])} for session in sessions
    ]
    response.status = 200
    response.message = "session fetched successfully"
    response.data = serialized_sessions
    return response


def start_session(country:str,operator:str):
    response = APIResponse()
    request={"country":country,"operator":operator}
    sessions=collection.find_one(request)
    if sessions ==None:
        raise CustomException(status=404,message="Country operator pair not found")
    
    res = requests.post(f"{MICRO1_URL}/start_session", json=request)
    if res.status_code != 200:
        raise CustomException(status=res.status_code,message="Error while starting the session")

    response.status = 200
    response.message = "session started successfully"
    return response


def stop_session(country: str, operator: str):
    response = APIResponse()
    request = {"country": country, "operator": operator}
    
    # Check if the session exists
    session = collection.find_one(request)
    if session is None:
        raise CustomException(status=404, message="Country operator pair not found")
    
    # Check if the session's priority is "High"
    if session.get("priority") == "High":
        raise CustomException(status=400, message="High priority session can't stop")
    
    # Stop the session by making a request to the microservice
    res = requests.post(f"{MICRO1_URL}/stop_session", json=request)
    if res.status_code != 200:
        raise CustomException(status=500, message="Error while stopping the session")

    # Prepare a success response
    response.status = 200
    response.message = "Session stopped successfully"
    return response



def restart_session(country:str,operator: str):
    response = APIResponse()
    request={"country":country,"operator":operator}
    sessions=collection.find_one(request)
    if sessions ==None:
        raise CustomException(status=404,message="Country operator pair not found")
    
    res = requests.post(f"{MICRO1_URL}/restart_session", json=request)
    if res.status_code != 200:
        raise CustomException(status=500,message="Error while restarting the session")

    response.status = 200
    response.message = "session restarted successfully"
    return response