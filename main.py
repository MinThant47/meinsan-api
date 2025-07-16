from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from schema import chatbot
from langchain.schema import HumanMessage, AIMessage
from get_chathistory import save_chat_to_redis, load_chat_from_redis
# import speech_recognition as sr
from audio_transcribe import transcribe_audio
# from tts_func import run_tts_pipeline
from aigooglestudio import generate_tts_audio
import shutil
import os

app = FastAPI()
# recognizer = sr.Recognizer()

@app.get("/")
def home():
    return {"message": "မေစံ API is running!"}


@app.post("/uploadandreturn")
async def upload_audio(file: UploadFile = File(...)):
   
    with open("temp.wav", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # with sr.AudioFile("temp.wav") as source:
        #     audio_data = recognizer.record(source)
        #     recognized_text = recognizer.recognize_google(audio_data, language="my-MM")
        recognized_text = transcribe_audio("temp.wav")
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
        print("Response finished")
        
        generate_tts_audio(
            text = result['response']['answer'],
            voice_name="Leda",
            output_filename="response",
        )
        
        # run_tts_pipeline(result['response']['answer'])


    return {
        "status": "success",
        "recognized_text": recognized_text,
        "response_text": result['response']['answer'],
        "command": result['command'],
        "audio_url": "https://meinsan-api.onrender.com/get_response_audio"
    }

    # return {"text": recognized_text}

# @app.get("/get_response_audio")
# def get_response_audio():
#     return FileResponse("response.wav", media_type="audio/wav", filename="response.wav")

@app.get("/get_response_audio")
def get_response_audio():
    return FileResponse(
        "response.mp3", 
        media_type="audio/mp3", 
        filename="response.mp3",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

#uvicorn main:app --host 0.0.0.0 --port 8000 --reload