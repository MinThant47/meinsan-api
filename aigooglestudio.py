from google import genai
from google.genai import types
import wave
from dotenv import load_dotenv
from pydub import AudioSegment
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Save PCM audio to a .wav file
def save_wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# Function to generate TTS audio using Gemini with dynamic tone
def generate_tts_audio(
    text, 
    voice_name='Zephyr', 
    output_filename='output', 
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
    # save_wave_file(output_filename + ".wav", pcm_data)
    save_wave_file(f"{output_filename}.wav", pcm_data)

    audio = AudioSegment.from_wav(output_filename + ".wav")

    # audio.export(f"{output_filename+".mp3"}", format="mp3", bitrate="32k")
    audio.export(f"{output_filename}.mp3", format="mp3", bitrate="32k")

    print(f"Audio saved to: {output_filename}")
