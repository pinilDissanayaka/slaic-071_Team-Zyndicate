import os
import streamlit as st
from utils.utils import save_pdf_txt_on_temp_dir, load_into_vector_store, convert_img_to_text, stream_text

temp_file_path="temp/"

image_claim=""
text_claim=""
claim=""

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
            st.button("Upload to vector store.", on_click=load_into_vector_store())

st.title("💡 Manifesto Matchmaker")
st.write("-----------------------------------------------------------------------------------------------------------") 

selected_themes=st.multiselect(label="Select Your Themes", 
                               options=["Infrastructure", "Social Protection", "Trade and Export", "Labour", "Governance", "Law and Order", "Corruption", "Agriculture", "Health", "Taxation", "Education", "Supplementary", "Economic Growth", "IMF Programme", "Reconciliation"],
                               help="We have categorized all presidential candidate manifesto promises into 15 distinct themes. In this section, you have to select which themes you wish to prioritize in your manifesto. A theme is a core policy area that captures a large number of promises. Select all the themes you wish to prioritize in your manifesto. You can select multiple themes.")

if selected_themes:
    for selected_theme in selected_themes:
        theme_cols=st.columns(len(selected_themes))

