import streamlit as st
from utils.candidates import CandidateAgent 
from utils.utils import save_img_on_dir, save_pdf_txt_on_temp_dir, load_into_vector_store, stream_text

# App title
st.set_page_config(page_title="🤗💬 ElectWise")

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


# Set up the Streamlit page
st.title("👤 Election Candidate")

# User input for location
location = st.text_input("Enter the location (e.g., Colombo):", "")

# Initialize the CandidateAgent with the database URI
db_uri = "postgresql://Denuwan:rsqY2Jbj7CZQ@ep-dark-frog-a5hpd82n.us-east-2.aws.neon.tech/Election?sslmode=require"
candidate_agent = CandidateAgent(db_uri)

# Query and display results when user provides a location
if st.button("Query Candidates"):
    if location:
        with st.spinner(f"Querying candidates from {location}..."):
            for response in candidate_agent.agent_executor.stream({"messages": [f"Who are the candidates from {location}?"]}):
                st.write(response)
                st.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    else:
        st.warning("Please enter a valid location.")


