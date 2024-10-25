from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Define the request body schema
class SessionRequest(BaseModel):
    country: str
    operator: str

MICRO1_URL = "http://sms_system:8001"  # Base URL of Microservice 1

@app.get("/sessions")
def list_sessions():
    # Call Microservice 1 to get the list of running sessions
    response = requests.get(f"{MICRO1_URL}/sessions")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch sessions from Microservice 1")
    return response.json()

@app.post("/start")
def start_session(request: SessionRequest):
    # Call Microservice 1 to start the session
    response = requests.post(f"{MICRO1_URL}/start_session", json=request.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/stop")
def stop_session(request: SessionRequest):
    # Call Microservice 1 to stop the session
    response = requests.post(f"{MICRO1_URL}/stop_session", json=request.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()
