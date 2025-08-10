from google.genai import types
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
AUDIO_GOOGLE_API_KEY = os.getenv("AUDIO_GOOGLE_API_KEY")

def transcribe_audio(filename):
  with open(filename, 'rb') as f:
      audio_bytes = f.read()

  client = genai.Client(api_key=AUDIO_GOOGLE_API_KEY)

  response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      """Transcribe this audio clip. It may contain both Burmese and English. Output only the plain transcription without any additional explanation or formatting.""",
      types.Part.from_bytes(
        data=audio_bytes,
        mime_type='audio/wav',
      )
    ]
  )
  return response.text

