# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install MongoDB client, jq, screen
RUN apt-get update && apt-get install -y \
    jq \
    screen

# Set working directory
WORKDIR /app

# Copy Python script and API service to the container
# COPY your_python_script.py /app/your_python_script.py
# COPY api_service_micro1.py /app/api_service_micro1.py

# COPY ./sms_system.py /app/sms_system.py
# COPY ./sms_sender.py /app/sms_sender.py

# Correct the file paths
COPY ./sms_system.py /app/sms_system.py
COPY ./sms_sender.py /app/sms_sender.py


# Install Python dependencies
RUN pip install fastapi uvicorn pymongo

# Expose the FastAPI API for Microservice 1 on port 8001
EXPOSE 8001

# Run the FastAPI server
CMD ["uvicorn", "sms_system:app", "--host", "0.0.0.0", "--port", "8001"]
