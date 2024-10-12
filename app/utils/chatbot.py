from langgraph.graph import END, StateGraph, START
from typing import List, TypedDict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from utils.utils import get_retriever, get_llm


class State(TypedDict):
    question: str
    documents: List[str]
    generation: str


response:str

        
def retrieve_node(state:State):    
    question=f"""{state['question']} """
    
    retrieve_documents=get_retriever().invoke(question)
    
    return {"documents": retrieve_documents, "question" : state['question']}
    

def generate_node(state:State):
    question_prompt_template=  """You are an assistant with access to the full manifestos of all candidates in the upcoming election.
    Answer question question : {QUESTION}. Provide accurate, fact-based responses using the manifestos, and offer comparisons if asked.
    using only given context : {CONTEXT}
    Ensure that all answers are concise, neutral, and factually based on the information provided in the manifestos.
    """

    question_prompt=ChatPromptTemplate.from_template(question_prompt_template)

    question_chain = (
        {"QUESTION":RunnablePassthrough(), "CONTEXT": RunnablePassthrough()}
        | question_prompt
        | get_llm()
        | StrOutputParser()
        )
    
    global response

    response=question_chain.invoke({"QUESTION": state["question"], "CONTEXT": state["documents"]})
    
    return {'generation' : response}



work_flow=StateGraph(State)
work_flow.add_node("retrieve_node", retrieve_node)
work_flow.add_node("generate_node", generate_node)

work_flow.add_edge(START, "retrieve_node")
work_flow.add_edge("retrieve_node", "generate_node")
work_flow.add_edge("generate_node", END)

graph=work_flow.compile()


def chat_with_manifesto(user_input):
    for event in graph.stream({"question": user_input}):
        pass

    return response

