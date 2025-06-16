# from google import genai
# from google.genai import types
# import wave
# from dotenv import load_dotenv
# import os

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# 1
# # Set up the wave file to save the output:
# def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
#    with wave.open(filename, "wb") as wf:
#       wf.setnchannels(channels)
#       wf.setsampwidth(sample_width)
#       wf.setframerate(rate)
#       wf.writeframes(pcm)

# client = genai.Client(api_key=GEMINI_API_KEY)

# response = client.models.generate_content(
#    model="gemini-2.5-flash-preview-tts",
#    contents="Say cheerfully: Have a wonderful day!",
#    config=types.GenerateContentConfig(
#       response_modalities=["AUDIO"],
#       speech_config=types.SpeechConfig(
#          voice_config=types.VoiceConfig(
#             prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                voice_name='Leda',
#             )
#          )
#       ),
#    )
# )

# data = response.candidates[0].content.parts[0].inline_data.data

# file_name='out.wav'
# wave_file(file_name, data) # Saves the file to current directory

from google import genai
from google.genai import types
import wave
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Save PCM audio to a .wav file
def save_wave_file(filename, pcm, channels=1, rate=8000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# Function to generate TTS audio using Gemini with dynamic tone
def generate_tts_audio(
    text, 
    voice_name='Leda', 
    output_filename='output.wav', 
):
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name,
                    )
                )
            ),
        )
    )

    # Extract PCM data and save
    pcm_data = response.candidates[0].content.parts[0].inline_data.data
    save_wave_file(output_filename, pcm_data)
    print(f"Audio saved to: {output_filename}")

