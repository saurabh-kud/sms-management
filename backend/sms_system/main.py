from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from pymongo import MongoClient
import subprocess
import random

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://mongo:27017")
db = client["sms_service"]
collection = db["countryOperator"]


# Define the request body schema
class SessionRequest(BaseModel):
    country: str
    operator: str


# Function to start a screen session
def start_screen_session(country, operator):
    session_name = f"{country}_{operator}"
    print(f"session_name start : {session_name}")
    # Check if the session already exists
    existing_sessions = subprocess.run(
        ["screen", "-ls"], capture_output=True, text=True
    ).stdout
    print(f"existing sessions: {existing_sessions}")
    if session_name in existing_sessions:
        print(f"Session {session_name} is already running")
    else:
        print(f"Session {session_name} is not running, starting it")
        # Start the screen session in detached mode
        try:
            # subprocess.run(f"screen -dmS {session_name} python3 /app/your_python_script.py --country {country} --operator {operator}", shell=True, check=True)
            subprocess.run(
                [
                    "screen",
                    "-dmS",
                    session_name,
                    "python3",
                    "script.py",
                    "--country",
                    country,
                    "--operator",
                    operator,
                ]
            )
            collection.update_one(
                {"country": country, "operator": operator},
                {"$set": {"status": "Active"}},
            )

            print(f"Started session for {session_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error starting session for {session_name}: {e}")
        except Exception as e:
            print(f"Unexpected error starting session for {session_name}: {e}")


# Function to stop a screen session
def stop_screen_session(country, operator):
    session_name = f"{country}_{operator}"

    try:
        print(f"session_name start : {session_name}")

        # subprocess.run(["screen", "-S", session_name, "-X" "quit"])
        os.system(f"screen -S {session_name} -X quit")

        collection.update_one(
            {"country": country, "operator": operator}, {"$set": {"status": "Inactive"}}
        )

    except subprocess.CalledProcessError as e:
        print(f"Error starting session for {session_name}: {e}")
    except Exception as e:
        print(f"Unexpected error starting session for {session_name}: {e}")
    # print(f"Stopped session for {session_name}")


# Insert default country-operator pairs into MongoDB if empty
def initialize_database():
    print("initialize_database")
    if collection.count_documents({}) == 0:
        default_pairs = [
            {
                "country": "India",
                "operator": "Airtel",
                "status": "Inactive",
                "priority": "High",
            },
            {
                "country": "India",
                "operator": "JIO",
                "status": "Inactive",
                "priority": "Low",
            },
            {
                "country": "India",
                "operator": "VI",
                "status": "Inactive",
                "priority": "Low",
            },
            {
                "country": "India",
                "operator": "Tata-Docomo",
                "status": "Inactive",
                "priority": "Low",
            },
            {
                "country": "Uzbekistan",
                "operator": "UzMobile",
                "status": "Inactive",
                "priority": "High",
            },
            {
                "country": "Ukraine",
                "operator": "3Mob",
                "status": "Inactive",
                "priority": "High",
            },
            {
                "country": "Tajikistan",
                "operator": "MegaFon",
                "status": "Inactive",
                "priority": "High",
            },
        ]
        collection.insert_many(default_pairs)
        print("Inserted default country-operator pairs.")


# On startup, connect to MongoDB, insert default data, and start sessions
@app.on_event("startup")
async def startup_event():
    print("startup_event")
    # Initialize database with default country-operator pairs if empty
    initialize_database()
    print("after initialized database")
    # Fetch country-operator pairs and start sessions
    country_operator_pairs = collection.find()
    for pair in country_operator_pairs:
        print(f"pair: {pair}")
        country = pair["country"]
        operator = pair["operator"]
        start_screen_session(country, operator)


# API to list all running screen sessions
@app.get("/sessions")
def list_sessions():
    existing_sessions = subprocess.run(
        ["screen", "-ls"], capture_output=True, text=True
    ).stdout
    print(f"existing_sessions: {existing_sessions}")
    return {"running_sessions": existing_sessions}


# API to start a new session
@app.post("/start_session")
def start_session(request: SessionRequest):
    start_screen_session(request.country, request.operator)
    return {"message": f"Started session for {request.country} - {request.operator}"}


# API to stop a session
@app.post("/stop_session")
def stop_session(request: SessionRequest):
    stop_screen_session(request.country, request.operator)
    return {"message": f"Stopped session for {request.country} - {request.operator}"}


# API to stop a session
@app.post("/restart_session")
def stop_session(request: SessionRequest):
    stop_screen_session(request.country, request.operator)
    start_screen_session(request.country, request.operator)
    return {"message": f"restarted session for {request.country} - {request.operator}"}


@app.get("/get-analytics")
def get_analytics():
    # get data from mongodb
    collection = db["sms_analytics"]
    data = collection.find()
    return {"message": "get_analytics", "data": data}
