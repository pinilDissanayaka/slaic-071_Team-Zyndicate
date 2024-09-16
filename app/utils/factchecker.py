from utils.utils import embeddings, retriever, llm
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List

class FactChecker(TypedDict):
    claim: str
    party: str
    score: str
    verdict: str
    documents: List[str]

response:str

def fact_retrieve_node(fact:FactChecker):
    question=f'''Retrieve relevant documents from the vector database based on the following inputs: {fact['claim']} and a 
    selected party {fact['party']}. Ensure the documents focus on the selected party, providing insights 
    into the policies or statements made by the specified candidates or parties'''
    
    retrieve_documents=retriever.invoke(question)
    
    return {"documents": retrieve_documents}

def fact_generate_node(fact:FactChecker):
    percentage_prompt_template=  """You are a supporter who has access to the full manifesto of all candidates in the upcoming election.
        Decide on the facts presented : {FACTS}. Provide accurate, fact-based responses using policy statements, and offer comparisons if asked.
        Provide as a percentage how much truth there is for the final conclusion
        Using only the given context : {CONTEXT}
        Ensure that all answers are concise, neutral and based on the information provided in the policy statements.
        If the answer cannot be found in the context, please state "I don't know". Do not try to prepare an answer."""

    question_prompt=ChatPromptTemplate.from_template(percentage_prompt_template)

    question_chain = (
        {"FACTS":RunnablePassthrough(), "CONTEXT": RunnablePassthrough()}
        | question_prompt
        | llm
        | StrOutputParser()
        )
    
    global percentage_response

    percentage_response=question_chain.invoke({"FACT": fact["claim"], "CONTEXT": fact["documents"]})
    
    return {'score' :percentage_response}

def fact_verdict_node(fact:FactChecker):
    verdict_prompt_template=  """You are a fact checker tasked with providing a final conclusion percentage: {SCORE} based on a specific party: {PARTY}.
    Provide a score out of 10 for each candidate or party based on the provided evidence.
    Indicate as a percentage how much truth there is in the final conclusion.final conclusion provide as english,sinhala and tamil languages.

    - If the score is less than 50%, output: "This party cheats or provides misleading information."
    - If the score is between 50% and 75%, output: "This party can contribute something positive to the country, but there are concerns."
    - If the score is greater than 75%, output: "This party's claims are almost entirely truthful."

    Score: {SCORE}
    Party: {PARTY}
    Final Conclusion:
        1. English
        2. Sinhala
        3. Tamil
    """

    verdict_prompt=ChatPromptTemplate.from_template(verdict_prompt_template)

    verdict_chain = (
        {"SCORE":RunnablePassthrough(), "PARTY": RunnablePassthrough()}
        | verdict_prompt
        | llm
        | StrOutputParser()
        )
    
    global verdict_response

    verdict_response=verdict_chain.invoke({"SCORE": fact["score"], "PARTY": fact["party"]})
    
    return {'verdict' : verdict_response}


factFlow=StateGraph(FactChecker)
factFlow.add_node("fact_retrieve_node", fact_retrieve_node)
factFlow.add_node("fact_generate_node", fact_generate_node)
factFlow.add_node("fact_verdict_node", fact_verdict_node)

factFlow.add_edge(START, "fact_retrieve_node")
factFlow.add_edge("fact_retrieve_node", "fact_generate_node")
factFlow.add_edge("fact_generate_node", "fact_verdict_node")
factFlow.add_edge("fact_verdict_node", END)

graph=factFlow.compile()


def fact_checker(party:str, claim:str):
   for i in graph.stream({"party": party, "claim": claim}):
       pass
   global verdict_response
   global percentage_response

   return verdict_response, percentage_response   

