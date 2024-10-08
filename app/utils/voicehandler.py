import os
import streamlit as st
from groq import Groq
import wave

os.environ['GROQ_API_KEY']=st.secrets['GROQ_API_KEY']

temp_dir="temp"


def save_voice_on_dir(wav_audio_data, file_name, folder=temp_dir):
    try:
        if os.path.exists(folder):
            os.mkdir(folder)

        voice_file_path = os.path.join(folder, file_name + format)
        
        with wave.open(voice_file_path, "wb") as wav_file:
            n_channels = 1  # Mono (2 for stereo)
            sampwidth = 2   # Sample width in bytes (2 = 16-bit audio)
            framerate = 44100  # Sampling rate (44.1kHz for CD-quality audio)
            n_frames = len(wav_audio_data) // sampwidth  # Number of frames in the audio
            
            # Set the file's parameters
            wav_file.setnchannels(n_channels)
            wav_file.setsampwidth(sampwidth)
            wav_file.setframerate(framerate)

            # Write the byte data to the WAV file
            wav_file.writeframes(wav_audio_data)
            
        return voice_file_path
    except Exception as e:
        st.error(e.args) 


def voice_to_text(voice_file_path): 
    try:
        client=Groq()
        
        with open(voice_file_path, "rb") as voice_file:
        
            transcription = client.audio.transcriptions.create(
                file=(voice_file_path, voice_file.read()), # Required audio file
                model="distil-whisper-large-v3-en", # Required model to use for transcription
                prompt="Specify context or spelling",  # Optional
                response_format="json",  # Optional
                language="en",  # Optional
                temperature=0.0  # Optional
        )

        return transcription.text
    except Exception as e:
        st.exception(e.args)

