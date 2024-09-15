from langgraph.graph import END, StateGraph, START
from typing import List, TypedDict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from utils.utils import retriever, llm


class State(TypedDict):
  question: str
  documents: List[str]
  generation: str


response:str

        
def retrieve_node(state:State):    
    question=f'''Compare the manifestos focusing on the key issues of given {state['question']} '''
    
    retrieve_documents=retriever.invoke(question)
    
    return {"documents": retrieve_documents, "question" : state['question']}
    

def generate_node(state:State):
    question_prompt_template=  """You are an assistant with access to the full manifestos of all candidates in the upcoming election.
    Answer question question : {question}. Provide accurate, fact-based responses using the manifestos, and offer comparisons if asked.
    using only given context : {context}
    Ensure that all answers are concise, neutral, and factually based on the information provided in the manifestos.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
    """

    question_prompt=ChatPromptTemplate.from_template(question_prompt_template)

    question_chain = (
        {"question":RunnablePassthrough(), "context": RunnablePassthrough()}
        | question_prompt
        | llm
        | StrOutputParser()
        )
    
    global response

    response=question_chain.invoke({"question": state["question"], "context": state["documents"]})
    
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


    
