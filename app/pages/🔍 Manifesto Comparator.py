import os
import streamlit as st
from utils.comparator import manifesto_comparator
from utils.utils import load_into_vector_store, save_pdf_txt_on_temp_dir, stream_text

temp_file_path="temp/"

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
        
st.title("🔍 Manifesto Comparator")
st.write("Quickly compare candidate manifestos side-by-side on key issues like the economy 💰, healthcare 🏥, and education 📚. Discover the promises, goals, and policies that matter most to you, all in one place.")
st.write("-----------------------------------------------------------------------------------------------------------")

selected_category = st.selectbox(
    "Which category do you want to compare :",
    ("Economic Growth", "IMF Programme", "Taxation", "Governance", "Social Protection", "Supplementary", "Infrastructure", "Trade and Export", "Agriculture", "Education", "Law and Order", "Health", "Reconciliation", "Corruption", "Labour"),
    help="Every promise has an associated topic. In this section, select which topics you wish to focus on, under each of your chosen themes. A topic is a distinct subject area that classifies individual promises. Each theme has multiple topics, though not all topics are represented under every theme."

)

candidates = st.text_input("Enter candidate names or party to compare :")

if candidates and selected_category:
    if st.button("Compare"):
        try:
            with st.spinner("Thinking..."):
                generated_response, evaluation_response=manifesto_comparator(domain=selected_category, candidates=candidates)
                
                st.write_stream(stream_text(generated_response))
                st.write("---------------------------------------------------------------------------------------------------------------")
                st.write_stream(stream_text(evaluation_response))            
        except Exception as e:
            st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")






