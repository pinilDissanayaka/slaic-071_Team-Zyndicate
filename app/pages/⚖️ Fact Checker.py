import os
import streamlit as st
from st_audiorec import st_audiorec
from utils.factchecker import fact_checker
from utils.utils import save_pdf_txt_on_temp_dir, load_into_vector_store, convert_img_to_text, stream_text, get_post_to_text

temp_file_path="temp/"

image_claim=""
text_claim=""
post_claim=""
claim=""

# App title
st.set_page_config(page_title="🤗💬 Election-Insight-App ")

#app side bar
with st.sidebar:
    st.subheader("Upload the manifesto of the candidate.")
    
    uploaded_files = st.file_uploader(
    "Choose a PDF, TXT files", accept_multiple_files=True, type=["pdf", "txt"])
    
    
    for uploaded_file in uploaded_files:
        st.write("filename:", uploaded_file.name)
        save_pdf_txt_on_temp_dir(uploaded_file=uploaded_file)
        
    if uploaded_files:
        with st.spinner("Processing..."):
            st.button("Upload to vector store.", on_click=load_into_vector_store())

st.title("⚖️ Fact Checker")
st.write("Tired of false claims? Our AI verifies campaign statements in real-time to help you separate fact from fiction. No more falling for exaggerated promises! 🚨")
st.write("-----------------------------------------------------------------------------------------------------------") 
selected_party = st.selectbox(
    "Select the party to fact check :",
    ("National People's Power | NPP", "Samagi Jana Balawegaya | SJB", "Sri Lanka Podujana Peramuna | SLPP", "NDC", "CPP", "PPP", "GUM", "GFP", "GCPP", "APC", "PNC", "LPG", "NDP", "Independent")
)

if selected_party =="Independent":
    selected_party=st.text_input("Enter the Independent group name:")

text_claim = st.text_area("Enter the claim as text to fact check :")

st.write("or")

url=st.text_input("Enter the URL of the post to fact check :")

if url:
    with st.spinner("Extracting..."):
        post_claim=get_post_to_text(url=url)

st.write("or")

uploaded_image_file = st.file_uploader("Choose a PNG, JPEG, GIF, BMP, TIFF or WebP files", accept_multiple_files=False, type=["jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp", "webp"])

if uploaded_image_file:
    try:
        with st.spinner("Extracting..."):
            st.image(image=uploaded_image_file)
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")

if uploaded_image_file:
    try:
        with st.spinner("Extracting..."):
            image_claim=convert_img_to_text(uploaded_image_file=uploaded_image_file)
        if image_claim != "":
            st.write("Text extracted from uploaded file.")
            st.write(image_claim)
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")
        st.warning(e.args, icon="🚨")
        
    

if image_claim != "" or text_claim != "" or post_claim != "":
    claim=image_claim+" "+text_claim+" "+post_claim

if claim and selected_party:
    try:
        if st.button("Fact Check"):
            with st.spinner("Thinking..."):
                generated_response, evaluation_response=fact_checker(claim=claim, party=selected_party)
                st.write("---------------------------------------------------------------------------------------------------------------")
                st.write_stream(stream_text(generated_response))
                st.write("---------------------------------------------------------------------------------------------------------------")
                st.write_stream(stream_text(evaluation_response))
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")
        st.warning(e.args, icon="🚨")
        
