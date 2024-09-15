from utils.utils import embeddings, retriever, llm
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List

generated_response:str
evaluation_response:str


class Graph_State(TypedDict):
  evaluation: str
  documents: List[str]
  generation: str
  candidates: str
  domain: str
  

def retrieve_node(state:Graph_State):
  question=f"Compare the manifestos of {state['candidates']} focusing on the key issues of {state['domain']}"

  retrieved_documents=retriever.invoke(question)

  return {"documents": retrieved_documents}


def generate_node(state:Graph_State):
  summary_prompt_template='''
        Compare the manifestos of all candidates focusing on the key issues of given : {DOMAIN} with candidate names.
        using only given context : {CONTEXT}
        Provide a side-by-side breakdown of their promises, highlighting similarities, differences, and unique approaches.
        Summarize the main goals and policies for each candidate and offer an analysis of how these align with their past statements or voting records,
        If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer."
    '''

  summary_prompt=ChatPromptTemplate.from_template(summary_prompt_template)


  summary_chain = (
    {"DOMAIN":RunnablePassthrough(), "CONTEXT": retriever}
    | summary_prompt
    | llm
    | StrOutputParser()
    )

  generation=summary_chain.invoke(state['domain'])
  global generated_response
  generated_response=generation

  return {"generation": generation}


def evaluate_node(state:Graph_State):
  evaluate_prompt_template='''
  Evaluate the manifesto of all candidate on a scale of 1 to 10 based on the following criteria Using given context : {CONTEXT} in the given : {DOMAIN}
    please provide the score with candidate name ,separate scores using \n.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
    Don't try to calculate average score.
  '''

  evaluate_prompt=ChatPromptTemplate.from_template(evaluate_prompt_template)


  evaluate_chain = (
    {"CONTEXT": RunnablePassthrough(), "DOMAIN" :  RunnablePassthrough()}
    | evaluate_prompt
    | llm
    | StrOutputParser()
    )

  evaluation=evaluate_chain.invoke({"CONTEXT": state['generation'], "DOMAIN": state['domain']})
  
  global evaluation_response
  
  evaluation_response=evaluation

  return {"evaluation": evaluation}


workflow = StateGraph(Graph_State)

# Define the nodes
workflow.add_node("retrieve_node", retrieve_node)  # retrieve
workflow.add_node("generate_node", generate_node)  # generate
workflow.add_node("evaluate_node", evaluate_node)  # evaluate


workflow.add_edge(START, "retrieve_node")
workflow.add_edge("retrieve_node", "generate_node")
workflow.add_edge("generate_node", "evaluate_node")
workflow.add_edge("evaluate_node", END)

graph=workflow.compile()



def manifesto_comparator(domain:str, candidates:str):
    for event in graph.stream({"domain": domain, "candidates": candidates}):
        pass
    
    global evaluation_response
    global generated_response

    return generated_response, evaluation_response
    


