import os
import streamlit as st
from utils.utils import save_img_on_dir, save_pdf_txt_on_temp_dir, load_into_vector_store

# App title
st.set_page_config(page_title="🤗💬 Election-Insight-App ")

#app side bar
with st.sidebar:
    try:
        st.subheader("Upload the manifesto of the candidate.")
        
        uploaded_files = st.file_uploader(
        "Choose a PDF, TXT files", accept_multiple_files=True, type=["pdf", "txt"])
        
        
        for uploaded_file in uploaded_files:
            st.write("filename:", uploaded_file.name)
            save_pdf_txt_on_temp_dir(uploaded_file=uploaded_file)
            
        if uploaded_files:
            with st.spinner("Processing..."):
                st.button("Upload to vector store.", on_click=load_into_vector_store())
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")

st.title("📜 Manifesto Simplifier")
st.write("Easily understand complex political promises! The Manifesto Simplifier breaks down lengthy, jargon-filled manifesto texts into simple, easy-to-read summaries. Get clear, concise explanations of candidate policies to help you make informed decisions.")
st.write("-----------------------------------------------------------------------------------------------------------") 
