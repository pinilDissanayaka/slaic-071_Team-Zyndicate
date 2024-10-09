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
  question=f"""{state['candidates']}, {state['domain']}"""

  retrieved_documents=retriever.invoke(question)

  return {"documents": retrieved_documents, "candidates":state['candidates']}


def generate_node(state:Graph_State):
  summary_prompt_template="""You are an assistant tasked with comparing only given election candidates {CANDIDATES} or political parties based on specific categories. 
  The user will provide the category {DOMAIN} and the context want to compare. {CONTEXT}
  Your job is to present a clear, fact-based comparison of how each given candidate or party addresses the selected category. 
  Be objective and highlight the key points from each manifesto or policy statement. 
  Ensure the comparison is concise and provides meaningful insights for the user to evaluate.
  Summarize the main goals and policies for each candidate and offer an analysis of how these align with their past statements or voting records.
  final conclusion provide as english,sinhala and tamil languages.
  If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
  """

  summary_prompt=ChatPromptTemplate.from_template(summary_prompt_template)


  summary_chain = (
    {"CANDIDATES":RunnablePassthrough() , "DOMAIN":RunnablePassthrough(), "CONTEXT": RunnablePassthrough()}
    | summary_prompt
    | llm
    | StrOutputParser()
    )

  generation=summary_chain.invoke({"CANDIDATES": state["candidates"], "DOMAIN": state["domain"], "CONTEXT": state["documents"]})
  global generated_response
  generated_response=generation

  return {"generation": generation}


def evaluate_node(state:Graph_State):
  evaluate_prompt_template="""
  You are an evaluator tasked with reviewing the comparison of given context : {CONTEXT} based on a specific category {DOMAIN}. 
  Provide a score out of 10 for each candidate or party, 
  based on how well their manifesto or policy addresses the selected category. Justify the score with a brief explanation, 
  highlighting strengths and weaknesses in each candidate's or party's approach.
  If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
  """

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
    


