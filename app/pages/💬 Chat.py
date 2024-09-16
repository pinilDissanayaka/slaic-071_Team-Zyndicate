import streamlit as st
import os
from utils.chatbot import chat_with_manifesto
from utils.utils import load_into_vector_store

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
            
    if uploaded_files:
        with st.spinner("Thinking..."):
            st.button("Upload to vector store.", on_click=load_into_vector_store)



st.title("🤖 AI Chatbot for Manifesto & Election Queries")
st.write("-----------------------------------------------------------------------------------------------------------")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you? 👋"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input):
    return chat_with_manifesto(user_input=prompt_input)


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)