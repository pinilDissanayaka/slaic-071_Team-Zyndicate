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


class State(TypedDict):
  messages:Annotated[list, add_messages]
  documents: List[str]
  generation: str


response=list()
embeddings=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
retriever=PineconeVectorStore(embedding=embeddings, index_name="manifesto").as_retriever(search_kwargs={"k": 6})
llm=ChatGroq(model="llama-3.1-8b-instant")
        
def retrieve_node(question):    
    question=f'''Compare the manifestos focusing on the key issues of given {question} '''
    
    retrieve_documents=retriever.invoke(question)
    
    #return {"documents": retrieve_documents}
    
    return retrieve_documents

def generate_node(question):
    question_prompt_template="""
        Given the following context and a question, generate an answer based on this context only.
        In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
        If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

        CONTEXT: {context}

        QUESTION: {question}
        
      """

    question_prompt=ChatPromptTemplate.from_template(question_prompt_template)

    question_chain = (
        {"question":RunnablePassthrough(), "context": retriever}
        | question_prompt
        | llm
        | StrOutputParser()
        )

    generation=question_chain.invoke(question)

    return generation

    
