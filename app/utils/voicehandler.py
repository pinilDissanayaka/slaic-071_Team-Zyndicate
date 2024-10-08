import os
import streamlit as st
from groq import Groq

os.environ['GROQ_API_KEY']=st.secrets['GROQ_API_KEY']

temp_dir="temp"


def save_voice_on_dir(wav_audio_data, file_name, folder=temp_dir, format=".wav"):
    try:
        if os.path.exists(folder):
            os.mkdir(folder)

        voice_file_path = os.path.join(folder, file_name + format)
        
        with open(voice_file_path, "wb") as voice_file:
            voice_file.write(wav_audio_data)
            
        return voice_file_path
    except Exception as e:
        st.error(e.args) 


def voice_to_text(voice_file_path): 
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

    print(transcription.text)