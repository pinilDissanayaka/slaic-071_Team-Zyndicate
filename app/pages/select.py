import streamlit as st


with st.sidebar:
    st.subheader("Upload the manifesto of the candidate.")
    
    uploaded_files = st.file_uploader(
    "Choose a PDF, TXT files", accept_multiple_files=True)
    
if "selected_themes" in st.session_state:
    st.write(st.session_state["selected_themes"])