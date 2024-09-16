import os
from typing import Annotated
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_groq.chat_models import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langgraph.graph import END, StateGraph, START
from langchain_pinecone import PineconeVectorStore
from pydantic import BaseModel, Field
from typing import List, TypedDict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages

load_dotenv()


os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')
os.environ['PINECONE_API_KEY']=os.getenv('PINECORN_API_KEY')
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ["GOOGLE_API_KEY"]=os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_PROJECT_ID"]=os.getenv('GOOGLE_PROJECT_ID')


embeddings=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

retriever=PineconeVectorStore(embedding=embeddings, index_name="manifesto").as_retriever(search_kwargs={"k": 10})

llm=ChatGroq(model="llama-3.1-70b-versatile",
            temperature=0.5,
            max_tokens=None,
            timeout=None)


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

def store(doc_splits, index_name='manifesto'):
    pinecone_vectore_store=PineconeVectorStore.from_documents(documents=doc_splits, embedding=embeddings, index_name="manifesto")
    return pinecone_vectore_store


def load_into_vector_store(directory="/temp"):
    list_of_dirs=os.listdir(directory)
    
    for dir in list_of_dirs:
        relative_path=os.path.join(directory, dir)
        if os.path.splitext(dir)[1] == 'pdf':
            store(split(load_pdf(relative_path)))
        elif os.path.splitext(dir)[1] == 'txt':
            store(split(load_txt(relative_path)))
            

