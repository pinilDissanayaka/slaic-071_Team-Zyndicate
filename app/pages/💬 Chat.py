import streamlit as st
from utils.chatbot import chat_with_manifesto
from utils.utils import load_into_vector_store, save_pdf_txt_on_temp_dir, stream_text


def clear_state():
    st.session_state.clear()

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
            
    st.button("Clear Chat History !", on_click=clear_state)


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
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt) 
                st.write_stream(stream_text(response))
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    except Exception as e:
        st.warning("Internal Server Error.", icon="⚠️")
        st.warning(e.args, icon="🚨")

