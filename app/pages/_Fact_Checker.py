import os
import streamlit as st
from utils.factchecker import fact_checker

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
        file_path=os.path.join(temp_file_path, uploaded_file.name)
        with open(file_path, 'wb') as file_to_write:
            file_to_write.write(uploaded_file.read())

st.title("✅Fact Checker")
st.write("-----------------------------------------------------------------------------------------------------------") 
selected_party = st.selectbox(
    "Select the party to fact check",
    ("NPP", "NDC", "CPP", "PPP", "GUM", "GFP", "GCPP", "APC", "PNC", "LPG", "NDP", "Independent")
)

claim = st.text_input("Enter the claim as text to fact check. ")

if claim and selected_party:
    if st.button("Fact Check"):
        with st.spinner("Progress..."):
            generated_response, evaluation_response=fact_checker(claim=claim, party=selected_party)
            
            st.write(generated_response)
            st.write("---------------------------------------------------------------------------------------------------------------")
            st.write(evaluation_response)