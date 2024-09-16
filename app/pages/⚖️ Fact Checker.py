import os
import streamlit as st
from utils.factchecker import fact_checker
from utils.utils import save_pdf_txt_on_temp_dir, load_into_vector_store

temp_file_path="temp/"

# App title
st.set_page_config(page_title="🤗💬 Election-Insight-App ")

#app side bar
with st.sidebar:
    st.subheader("Upload the content to fact check.")
    
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

claim = st.text_area("Enter the claim as text to fact check :")

if claim and selected_party:
    if st.button("Fact Check"):
        with st.spinner("Thinking..."):
            generated_response, evaluation_response=fact_checker(claim=claim, party=selected_party)
            
            st.write(generated_response)
            st.write("---------------------------------------------------------------------------------------------------------------")
            st.write(evaluation_response)