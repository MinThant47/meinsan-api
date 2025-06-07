import time
import requests
from dotenv import load_dotenv
import os
from flac_2_wav import flac_to_wav

load_dotenv()

API_KEY = os.getenv("CAMB")
BASE_URL = "https://client.camb.ai/apis/tts"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def initiate_tts(text, voice_id=20305, language=104, gender=2, age=2):
    # Validate text input
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # You might need to adjust these parameters based on API documentation
    payload = {
        "text": text.strip(),
        "voice_id": voice_id,
        "language": language,
        "gender": gender,
        "age": age
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data.get("task_id")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {response.text}")
        raise

# def initiate_tts(text, voice_id=20305, language=104, gender=2, age=2):
#     payload = {
#         "text": text,
#         "voice_id": voice_id,
#         "language": language,
#         "gender": gender,
#         "age": age
#     }
#     response = requests.post(BASE_URL, json=payload, headers=HEADERS)
#     response.raise_for_status()
#     data = response.json()
#     return data.get("task_id")


def wait_for_completion(task_id, poll_interval=2):
    status = ""
    run_id = None
    url = f"{BASE_URL}/{task_id}"
    headers = {"x-api-key": API_KEY}

    while status != "SUCCESS":
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        run_id = data.get("run_id")
        if status != "SUCCESS":
            time.sleep(poll_interval)
    return run_id


def download_tts_result(run_id, filename="response_output.flac"):
    url = f"https://client.camb.ai/apis/tts-result/{run_id}"
    response = requests.get(url, headers={"x-api-key": API_KEY}, stream=True)
    response.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    print(f"TTS audio saved as {filename}")


def run_tts_pipeline(text):
    task_id = initiate_tts(text)
    print("Task ID:", task_id)
    run_id = wait_for_completion(task_id)
    print("Run ID:", run_id)
    if run_id:
        download_tts_result(run_id)
        flac_to_wav("response_output.flac","response.wav")
