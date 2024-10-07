import os
import streamlit as st
from audiorecorder import audiorecorder
from utils.factchecker import fact_checker
from utils.utils import save_pdf_txt_on_temp_dir, load_into_vector_store, convert_img_to_text, stream_text

temp_file_path="temp/"

# App title
st.set_page_config(page_title="🤗💬 Election-Insight-App ")

#app side bar
with st.sidebar:
    st.subheader("Upload the manifesto of the candidate.")
    
    uploaded_files = st.file_uploader(
    "Choose a PDF, TXT files", accept_multiple_files=True)
    
    
    for uploaded_file in uploaded_files:
        st.write("filename:", uploaded_file.name)
        save_pdf_txt_on_temp_dir(uploaded_file=uploaded_file)
        
    if uploaded_files:
        with st.spinner("Processing..."):
            st.button("Upload to vector store.", on_click=load_into_vector_store)

st.title("⚖️ Fact Checker")
st.write("-----------------------------------------------------------------------------------------------------------") 
selected_party = st.selectbox(
    "Select the party to fact check :",
    ("National People's Power | NPP", "Samagi Jana Balawegaya | SJB", "Sri Lanka Podujana Peramuna | SLPP", "NDC", "CPP", "PPP", "GUM", "GFP", "GCPP", "APC", "PNC", "LPG", "NDP", "Independent")
)

image_claim=" "
text_claim=" "

text_claim = st.text_area("Enter the claim as text to fact check :")

st.write("or")

voice_claim_data = audiorecorder("Click to record", "Click to stop recording")

if len(voice_claim_data) > 0:
    # To play audio in frontend:
    st.audio(voice_claim_data.export().read())  

    # To save audio to a file, use pydub export method:
    voice_claim_data.export("audio.wav", format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    st.write(f"Frame rate: {voice_claim_data.frame_rate}, Frame width: {voice_claim_data.frame_width}, Duration: {voice_claim_data.duration_seconds} seconds")


if voice_claim_data is not None:
    with st.spinner("Extracting..."):
        pass

st.write("or")

uploaded_image_file = st.file_uploader("Choose a PDF, TXT, JPEG or PNG files", accept_multiple_files=False)

if uploaded_image_file:
    with st.spinner("Extracting..."):
        image_claim=convert_img_to_text(uploaded_image_file=uploaded_image_file)
    st.write("Text extracted from uploaded file.")
    st.write(image_claim)
    

if image_claim or text_claim:
    claim=image_claim+" "+text_claim

if claim and selected_party:
    if st.button("Fact Check"):
        with st.spinner("Thinking..."):
            generated_response, evaluation_response=fact_checker(claim=claim, party=selected_party)
            st.write("---------------------------------------------------------------------------------------------------------------")
            st.write_stream(stream_text(generated_response))
            st.write("---------------------------------------------------------------------------------------------------------------")
            st.write_stream(stream_text(evaluation_response))
