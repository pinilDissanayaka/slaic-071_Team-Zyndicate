import os
import streamlit as st
from utils.comparator import manifesto_comparator

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
        file_path=os.path.join(temp_file_path, uploaded_file.name)
        with open(file_path, 'wb') as file_to_write:
            file_to_write.write(uploaded_file.read())
            
st.title("🔍 Manifesto Comparator")
st.write("-----------------------------------------------------------------------------------------------------------")

selected_category = st.selectbox(
    "Which category do you want to compare",
    ("Economic Growth", "IMF Programme", "Taxation", "Governance", "Social Protection", "Supplementary", "Infrastructure", "Trade and Export", "Agriculture", "Education", "Law and Order", "Health", "Reconciliation", "Corruption", "Labour"),
)

candidates = st.text_input("Enter candidate names or party to compare.")

if candidates and selected_category:
    if st.button("compare"):
        with st.spinner("Progress..."):
            generated_response, evaluation_response=manifesto_comparator(domain=selected_category, candidates=candidates)
            
            st.write(generated_response)
            st.write("---------------------------------------------------------------------------------------------------------------")
            st.write(evaluation_response)
            
            





