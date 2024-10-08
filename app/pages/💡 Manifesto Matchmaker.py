import os
import streamlit as st
from utils.utils import save_pdf_txt_on_temp_dir, load_into_vector_store, stream_text
from utils.topics import get_topics
from utils.manifestomatchmaker import get_relevant_policies

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

st.text("Select Your Themes", help="Every promise has an associated topic. In this section, select which topics you wish to focus on, under each of your chosen themes. A topic is a distinct subject area that classifies individual promises. Each theme has multiple topics, though not all topics are represented under every theme.")

selected_themes=st.multiselect(label="", 
                               options=["Infrastructure", "Social Protection", "Trade and Export", "Labour", "Governance", "Law and Order", "Corruption", "Agriculture", "Health", "Taxation", "Education", "Supplementary", "Economic Growth", "IMF Programme", "Reconciliation"]
                               )

if selected_themes:
    st.text("Select Your Topics", help="Every promise has an associated topic. In this section, select which topics you wish to focus on, under each of your chosen themes. A topic is a distinct subject area that classifies individual promises. Each theme has multiple topics, though not all topics are represented under every theme.")
    col1, col2 = st.columns(2)
    
    half_point = len(selected_themes) // 2
    
    themes_col1 = selected_themes[:half_point] 
    themes_col2 = selected_themes[half_point:]
    
    themes={}

    with col1:
        for theme in themes_col1:
            st.subheader(theme)
            themes[theme]=st.multiselect(label="Select Your Topics", options=get_topics(theme))
    with col2:
        for theme in themes_col2:
            st.subheader(theme)
            themes[theme]=st.multiselect(label="Select Your Topics", options=get_topics(theme))
            
    if themes:
        with st.spinner("Processing..."):
            for theme in themes:
                with st.expander(theme):
                    st.write(get_relevant_policies(topic=theme))
            


