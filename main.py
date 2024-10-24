from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Jenkins API configuration (rekommenderat att använda miljövariabler för säkerhet)
JENKINS_URL = os.getenv("JENKINS_URL", "http://localhost:8080/job/github-triggered-job/build")
JENKINS_USER = os.getenv("JENKINS_USER", "pinguME")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN", "1159e425c2d16a466f11e84e4997e46b64")

@app.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()
        repo_name = payload.get("repository", {}).get("name", "Unknown Repo")

        # Log the received payload for debugging
        print(f"Webhook received from {repo_name}")

        # Trigger Jenkins build when webhook is received
        response = requests.post(JENKINS_URL, auth=(JENKINS_USER, JENKINS_API_TOKEN))

        # Check the response status
        if response.status_code == 201:
            return {"message": f"Build triggered successfully for {repo_name}"}
        else:
            return {
                "error": "Failed to trigger Jenkins job",
                "status": response.status_code,
                "response": response.text
            }
    except Exception as e:
        # Return an error if something went wrong
        return {"error": str(e)}

