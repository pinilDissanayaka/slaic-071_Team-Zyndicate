import streamlit as st
from utils.candidates import CandidateAgent 

# Set up the Streamlit page
st.title("Election Candidate Query")

# User input for location
location = st.text_input("Enter the location (e.g., Colombo):", "")

# Initialize the CandidateAgent with the database URI
db_uri = "postgresql://<uri>.aws.neon.tech/Election?sslmode=require"
candidate_agent = CandidateAgent(db_uri)

# Query and display results when user provides a location
if st.button("Query Candidates"):
    if location:
        with st.spinner(f"Querying candidates from {location}..."):
            for response in candidate_agent.agent_executor.stream({"messages": [f"Who are the candidates from {location}?"]}):
                st.write(response)
                st.write("----")
    else:
        st.warning("Please enter a valid location.")


