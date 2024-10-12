import streamlit as st
from utils.utils import get_embeddings, get_retriever, get_llm
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables import RunnablePassthrough
import plotly.express as px
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List


generated_response:str

class Graph_State(TypedDict):
    candidate:str
    documents: List[str]
    generation: str
    domain: List[str]

def retrieve_node(state:Graph_State):
    question=f"""{state["domain"]}, {state["candidate"]}"""
    
    retrieved_documents=get_retriever(search_k=3).invoke(question)
    
    return {"documents": retrieved_documents}


def generate_node(state:Graph_State):
    
    get_simplify_manifesto_prompt_template="""Given the following manifesto text from the {CANDIDATE} related to {DOMAIN}, 
    simplify it by converting complex or jargon-heavy language into easy-to-understand terms while retaining the original meaning. 
    Break down any detailed policy proposals into concise and clear bullet points, and explain key concepts in a voter-friendly manner.
    If possible, include simple real-world examples to clarify the impact of the policies.
        Party: {CANDIDATE}
        Domain: {DOMAIN}
        Manifesto Text:{CONTEXT}
    Output Requirements:
        Simplify complex language.
        Present key points as bullet points.
        Maintain original meaning and intent.
        Provide explanations or examples for difficult concepts.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
    """

    get_simplify_manifesto_prompt=ChatPromptTemplate.from_template(get_simplify_manifesto_prompt_template)
    
    get_simplify_manifesto_chain = (
    {"CONTEXT": RunnablePassthrough(), "CANDIDATE": RunnablePassthrough(), "DOMAIN": RunnablePassthrough()}   
    | get_simplify_manifesto_prompt
    | get_llm()
    | StrOutputParser()
    )

    generation=get_simplify_manifesto_chain.invoke({"CONTEXT": state["documents"], "CANDIDATE": state["candidate"], "DOMAIN": state["domain"]})
  
    global generated_response
  
    generated_response=generation

    return {"generation": generation}


workflow = StateGraph(Graph_State)

# Define the nodes
workflow.add_node("retrieve_node", retrieve_node)  # retrieve
workflow.add_node("generate_node", generate_node)  # generate

workflow.add_edge(START, "retrieve_node")
workflow.add_edge("retrieve_node", "generate_node")
workflow.add_edge("generate_node", END)

graph=workflow.compile()

def get_simplify_manifesto(domain:list, candidate:str):
  for event in graph.stream({"domain": domain, "candidate": candidate}):
    pass
  
  global generated_response
  
  return generated_response
