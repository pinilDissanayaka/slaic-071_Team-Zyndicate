import streamlit as st
from utils.utils import get_embeddings, get_retriever, get_llm
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables import RunnablePassthrough
import plotly.express as px
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List
from pydantic import BaseModel, Field


class Graph_State(TypedDict):
  documents: List[str]
  generation: str
  policies: List[str]
  
class Candidate(BaseModel):
    candidates: List[str]=Field(description="Which Presidential Candidates Aligns Most with Your Policy Choices")
    scores:List[float]=Field(description="Alignment percentage")
    description:str=Field(description="Explain the objectives and highlight the key points from each manifesto or policy statement")

generated_response:Candidate

def retrieve_node(state:Graph_State):
  policies=state['policies']
  retrieved_documents=[]
  for policy in policies:
    retrieved_documents.append(get_retriever(search_k=3).invoke(policy))
    
  return {"documents": retrieved_documents, "policies":state['policies']}


def generate_node(state:Graph_State):
    get_align_candidate_prompt_template="""You are an expert political analyst. 
    Based on the user’s policy preferences, 
    analyze the manifestos of the presidential candidates and determine which candidate aligns most closely with the user’s policy choices. 
    Provide a detailed breakdown of the match, specifying how each candidate's policies align with the user’s preferences.
        User's Policy Preferences:{POLICIES}

    Context: {CONTEXT}

    Based on this information, return the candidate with the highest alignment percentage out of 100%, 
    along with an explanation of how each candidate's policies match the user's preferences.
    If the answer is not found in the context, kindly state "I don't know." 
    Don't try to make up an answer.Don't try to make up an answer.
    """
    

    get_align_candidate_prompt=ChatPromptTemplate.from_template(get_align_candidate_prompt_template)
    
    structured_llm=get_llm().with_structured_output(Candidate)


    get_relevant_policies_prompt_chain = (
    {"CONTEXT": RunnablePassthrough(), "POLICIES": RunnablePassthrough()}   
    | get_align_candidate_prompt
    | structured_llm
    )

    generation=get_relevant_policies_prompt_chain.invoke({"CONTEXT": state["documents"], "POLICIES": state["policies"]})
  
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

def get_align_candidate(policies):
  for event in graph.stream({"policies": policies}):
    pass
  
  global generated_response
  return generated_response.candidates, generated_response.scores, generated_response.description

def draw_pie_plot(labels, sizes):
  try:
    st.subheader("Which Presidential Candidate Aligns Most with Your Policy Choices?")
    pie_chart=px.pie(values=sizes, names=labels)
  
    return pie_chart
  except Exception as e:
    st.warning(f"An unexpected error occurred. Please try again.", icon="⚠️")