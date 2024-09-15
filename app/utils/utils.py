import os
from typing import Annotated
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
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

retriever=PineconeVectorStore(embedding=embeddings, index_name="manifesto").as_retriever(search_kwargs={"k": 6})

llm=ChatGroq(model="llama-3.1-70b-versatile",
            temperature=0.5,
            max_tokens=None,
            timeout=None)


