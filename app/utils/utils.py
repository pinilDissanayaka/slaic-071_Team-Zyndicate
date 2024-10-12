import os
import logging
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
from langchain_groq.chat_models import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from groq import Groq
from time import sleep
import base64

load_dotenv()


os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')
os.environ['PINECONE_API_KEY']=os.getenv('PINECORN_API_KEY')
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ["GOOGLE_API_KEY"]=os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_PROJECT_ID"]=os.getenv('GOOGLE_PROJECT_ID')


llm_model="llama3-groq-70b-8192-tool-use-preview"
vision_model="llava-v1.5-7b-4096-preview"
embedding_model="models/text-embedding-004"
vector_store_index_name="manifesto"
search_k=4
temperature=0.6
temp_dir="temp"


def get_embeddings(embedding_model=embedding_model):
    embeddings=GoogleGenerativeAIEmbeddings(model=embedding_model)
    return embeddings

def get_retriever(search_k=search_k):
    retriever=PineconeVectorStore(embedding=get_embeddings(), index_name=vector_store_index_name).as_retriever(search_kwargs={"k": search_k})
    return retriever

def get_llm(llm_model=llm_model, temperature=temperature):
    llm=ChatGroq(model=llm_model,
                temperature=temperature,
                max_tokens=None,
                timeout=None)
    return llm


def load_pdf(path):
    manifesto_data=PyPDFLoader(path).load()
    return manifesto_data

def load_txt(path):
    manifesto_data=TextLoader(path).load()
    return manifesto_data

def split(docs):
    doc_splits = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=390,
        length_function=len,
        is_separator_regex=False,
    ).split_documents(docs)

    return doc_splits

def store(doc_splits, index_name=vector_store_index_name):
    pinecone_vectore_store=PineconeVectorStore.from_documents(documents=doc_splits, embedding=get_embeddings(), index_name=index_name)
    return pinecone_vectore_store


def load_into_vector_store(directory=temp_dir):
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)

        list_of_dirs=os.listdir(directory)
    
        for dir in list_of_dirs:
            relative_path=os.path.join(directory, dir)
            if os.path.splitext(dir)[1] == 'pdf':
                store(split(load_pdf(relative_path)))
            elif os.path.splitext(dir)[1] == 'txt':
                store(split(load_txt(relative_path)))
        
        st.success("Vector store created successfully.", icon="✅")

    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")

            
            
            
def save_pdf_txt_on_temp_dir(uploaded_file, temp_file_path=temp_dir):
    try:
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        file_path=os.path.join(temp_file_path, uploaded_file.name)
        with open(file_path, 'wb') as file_to_write:
            file_to_write.write(uploaded_file.read())
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")

        
def save_img_on_dir(uploaded_image_file, temp_file_path=temp_dir):
    try:
        if not os.path.exists(temp_file_path):
            os.mkdir(temp_file_path)
        file_path=os.path.join(temp_file_path, uploaded_image_file.name)
        with open(file_path, 'wb') as file_to_write:
            file_to_write.write(uploaded_image_file.read())
        return file_path
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")
            
            
def encode_image(image_path):
    try:
        if image_path:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")


def convert_img_to_text(uploaded_image_file):
    try:
        image_path=save_img_on_dir(uploaded_image_file=uploaded_image_file)
        base64_image = encode_image(image_path)

        client = Groq()

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please extract and display all visible text from the image dont extract images. Ensure the text is captured exactly as it appears, including any formatting, spacing, and special characters. If the image contains text in multiple areas or sections, maintain the relative structure and order in which the text appears."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model=vision_model,
        )   
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")


def get_post_to_text(url:str):
    try:
        post_list=[]
        post=WebBaseLoader(web_path=url).load()
        
        for post_chunk in post:
            post_list.append(post_chunk.page_content.replace("\n", ""))
            
        post_text=" ".join(post_list)
        
        return post_text
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")


def stream_text(text:str, delay=0.05):
    for word in text.split(" "):
        yield word + " "
        sleep(delay)
