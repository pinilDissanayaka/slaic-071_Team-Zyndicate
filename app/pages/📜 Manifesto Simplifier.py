import os
import streamlit as st
from utils.utils import save_img_on_dir, save_pdf_txt_on_temp_dir, load_into_vector_store, stream_text
from utils.simplifier import get_simplify_manifesto

# App title
st.set_page_config(page_title="🤗💬 ElectWise")

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


selected_party = st.selectbox(
    "Select the party to fact check :",
    ("National People's Power | NPP", "Samagi Jana Balawegaya | SJB", "Sri Lanka Podujana Peramuna | SLPP", "NDC", "CPP", "PPP", "GUM", "GFP", "GCPP", "APC", "PNC", "LPG", "NDP", "Independent")
)

if selected_party =="Independent":
    selected_party=st.text_input("Enter the Independent group name:")
else:
    selected_party=selected_party


if selected_party:
    selected_category = st.multiselect(
        label="Which category do you want to compare :",
        options=("Economic Growth", "IMF Programme", "Taxation", "Governance", "Social Protection", "Supplementary", "Infrastructure", "Trade and Export", "Agriculture", "Education", "Law and Order", "Health", "Reconciliation", "Corruption", "Labour"),
        help="Every promise has an associated topic. In this section, select which topics you wish to focus on, under each of your chosen themes. A topic is a distinct subject area that classifies individual promises. Each theme has multiple topics, though not all topics are represented under every theme.",
        placeholder="Choose at least one theme"
    )
    
if selected_party and selected_category:
    if st.button("Simplify"):
        try:
            with st.spinner("Processing..."):
                simplified_manifesto=get_simplify_manifesto(domain=selected_category, candidate=selected_party)
                
                st.write_stream(stream_text(simplified_manifesto))
                
        except Exception as e:
            st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")




