from pydub import AudioSegment

def flac_to_wav(flac_file, wav_file):
    audio = AudioSegment.from_file(flac_file, format="flac")
    audio.export(wav_file, format="wav")