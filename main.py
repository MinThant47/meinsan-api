from fastapi import FastAPI, File, UploadFile
from schema import chatbot
from langchain.schema import HumanMessage, AIMessage
from get_chathistory import save_chat_to_redis, load_chat_from_redis
import speech_recognition as sr
import shutil
import os

app = FastAPI()
recognizer = sr.Recognizer()

@app.get("/")
def home():
    return {"message": "မေစံ API is running!"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
   
    with open("temp.wav", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            recognized_text = recognizer.recognize_google(audio_data, language="my-MM")
    except Exception as e:
        os.remove("temp.wav")
        return {
            "status": "failed",
            "response_text": f"I am sorry, I don't understand the audio. {e}",
            "command": "stop"
        }

    os.remove("temp.wav")

    # Process recognized text

    chat_history = load_chat_from_redis()
    
    result = chatbot.invoke({'question': recognized_text, 'chat_history': chat_history})

    if result:
        chat_history.append(HumanMessage(content=recognized_text))
        chat_history.append(AIMessage(content=result['response']['answer']))
        save_chat_to_redis(chat_history)

    return {
        "status": "completed",
        "response_text": result['response']['answer'],
        "command": result['command']
    }

    # return {"text": recognized_text}


#uvicorn main:app --host 0.0.0.0 --port 8000 --reload