from utils.utils import embeddings, retriever, llm
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List
from pydantic import BaseModel, Field


class Graph_State(TypedDict):
  documents: List[str]
  generation: str
  topic: str
  
class Topic(BaseModel):
    policies: List[str]=Field(description="policies related to the topic")
  
generated_response:Topic

def retrieve_node(state:Graph_State):
  question=f"""You are an expert in retrieving information from a vector database. 
    I need you to find and extract all the policies related to the topic {state['topic']} from the given database. 
    The database contains vectorized representations of political manifestos.
    Topic: {state['topic']}

    Search the vector database, extract the relevant policies, and return them in a structured format.
    """

  retrieved_documents=retriever.invoke(question)

  return {"documents": retrieved_documents, "topic":state['topic']}


def generate_node(state:Graph_State):
    get_relevant_policies_prompt_template="""You are an expert in analyzing political manifestos. 
    Given the following manifesto text, identify and extract all the policies related to the topic.
    Provide the policies in a Python list format.
    Make sure the policies are related to the topic and more meaningful and readable.
    Manifesto Text: {CONTEXT}
    Return the policies related to the topic as a Python list.
    If the answer is not found in the context, kindly state "I don't know." 
    Don't try to make up an answer.
    """
    
    structured_llm=llm.with_structured_output(Topic)

    get_relevant_policies_prompt=ChatPromptTemplate.from_template(get_relevant_policies_prompt_template)


    get_relevant_policies_prompt_chain = (
    {"CONTEXT": RunnablePassthrough()}
    | get_relevant_policies_prompt
    | structured_llm
    )

    generation=get_relevant_policies_prompt_chain.invoke({"CONTEXT": state["documents"]})
  
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



def get_relevant_policies(themes:List[str]):
  list_of_policies=[]
  for theme in themes:
    for event in graph.stream({"topic": theme}):
            pass
          
    global generated_response
    
    list_of_policies.append(generated_response.policies)
  
  return list_of_policies


