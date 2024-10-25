from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Jenkins API configuration (rekommenderat att använda miljövariabler för säkerhet)
JENKINS_URL = os.getenv("JENKINS_URL", "http://localhost:8080/job/github-triggered-job/build")
JENKINS_USER = os.getenv("JENKINS_USER", "pinguME")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN", "1159e425c2d16a466f11e84e4997e46b64")

# Define a storage file for logging the webhook data
WEBHOOK_LOG_FILE = "webhook_log.json"

#hej
# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Webhook Service"}

# Webhook endpoint to capture GitHub events and trigger Jenkins job
@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Capture the webhook payload from GitHub
        payload = await request.json()

        # Extract repository name and topics
        repo_name = payload.get("repository", {}).get("name", "Unknown Repo")
        topics = payload.get("repository", {}).get("topics", [])

        # Log the payload and check for the 'jenkins-cdc' topic
        if "jenkins-cdc" in topics:
            log_webhook_event(payload, "Success - Jenkins-cdc topic found")
            
            # Trigger Jenkins build if the 'jenkins-cdc' topic exists
            response = trigger_jenkins_build()
            
            if response.status_code == 201:
                return {"message": f"Build triggered successfully for {repo_name}"}
            else:
                return {"error": "Failed to trigger Jenkins job", "status": response.status_code, "response": response.text}
        else:
            log_webhook_event(payload, "Failed - jenkins-cdc topic not found")
            return {"error": "jenkins-cdc topic not found in the repository topics"}

    except Exception as e:
        # Return and log an error if something goes wrong
        log_webhook_event(None, f"Error - {str(e)}")
        return {"error": str(e)}

# Function to trigger Jenkins job
def trigger_jenkins_build():
    try:
        # Send POST request to Jenkins to trigger the build
        response = requests.post(JENKINS_URL, auth=(JENKINS_USER, JENKINS_API_TOKEN))
        return response
    except Exception as e:
        print(f"Failed to trigger Jenkins job: {str(e)}")
        return None

# Function to log webhook events into a JSON file
def log_webhook_event(payload, status):
    log_data = {
        "status": status,
        "payload": payload,
        "event": "GitHub Webhook Event",
    }
    
    # Append to the log file
    try:
        with open(WEBHOOK_LOG_FILE, "a") as log_file:
            log_file.write(json.dumps(log_data, indent=4) + "\n")
    except Exception as e:
        print(f"Failed to log webhook event: {str(e)}")
