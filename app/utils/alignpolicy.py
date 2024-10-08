from utils.utils import embeddings, retriever, llm
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables import RunnablePassthrough
import matplotlib.pyplot as plt
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List
from pydantic import BaseModel, Field


class Graph_State(TypedDict):
  documents: List[str]
  generation: str
  policies: List[str]
  
class Candidate(BaseModel):
    candidate: List[str]=Field(description="Which Presidential Candidates Aligns Most with Your Policy Choices")
    score:List[float]=Field(description="Alignment Score")
    manifesto:List[str]=Field(description="In their manifesto, what the candidate's policies align with your policy choices")
generated_response:Candidate

def retrieve_node(state:Graph_State):
  retrieved_documents=retriever.invoke(state['policies'])

  return {"documents": retrieved_documents, "policies":state['policies']}


def generate_node(state:Graph_State):
    get_align_candidate_prompt_template="""You are an expert political analyst. 
    Based on the user’s policy preferences, 
    analyze the manifestos of the presidential candidates and determine which candidate aligns most closely with the user’s policy choices. 
    Provide a detailed breakdown of the match, specifying how each candidate's policies align with the user’s preferences.
        User's Policy Preferences:{POLICIES}

    Context: {CONTEXT}

    Based on this information, return the candidate with the highest alignment percentage, 
    along with an explanation of how each candidate's policies match the user's preferences.
    If the answer is not found in the context, kindly state "I don't know." 
    Don't try to make up an answer.
    """
    

    get_align_candidate_prompt=ChatPromptTemplate.from_template(get_align_candidate_prompt_template)
    
    structured_llm=llm.with_structured_output(Candidate)


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

def draw_pie_plot(labels, sizes):
    fig, ax=plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')
    
    return fig
    


def get_align_candidate(policies):
    for event in graph.stream({"policies": policies}):
      pass
    
    global generated_response


    return generated_response.candidate, generated_response.score, generated_response.manifesto