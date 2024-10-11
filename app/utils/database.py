import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from sqlalchemy.exc import SQLAlchemyError
from utils import get_llm
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

examples = [
    {"input": "List all candidates.", "query": "SELECT * FROM candidates;"},
    {
        "input": "Find all candidates from the 'SLPP' party.",
        "query": "SELECT * FROM candidates WHERE party = 'SLPP';",
    },
    {
        "input": "List all candidates from the 'Colombo' district.",
        "query": "SELECT * FROM candidates WHERE district = 'Colombo';",
    },
    {
        "input": "Find the total number of candidates in the election.",
        "query": "SELECT COUNT(*) FROM candidates;",
    },
    {
        "input": "List all candidates older than 50 years.",
        "query": "SELECT * FROM candidates WHERE age > 50;",
    },
    {
        "input": "How many candidates are from the 'UNP' party?",
        "query": "SELECT COUNT(*) FROM candidates WHERE party = 'UNP';",
    },
    {
        "input": "List the top 5 youngest candidates.",
        "query": "SELECT * FROM candidates ORDER BY age ASC LIMIT 5;",
    },
    {
        "input": "Find candidates with a 'Master's in Political Science'.",
        "query": "SELECT * FROM candidates WHERE education = 'Master''s in Political Science';",
    },
    {
        "input": "List all candidates who contributed to 'economic development'.",
        "query": "SELECT * FROM candidates WHERE contributions LIKE '%economic development%';",
    },
    {
        "input": "Which candidates have no education information?",
        "query": "SELECT * FROM candidates WHERE education IS NULL;",
    },
    {
        "input": "How many candidates belong to the 'JVP' party?",
        "query": "SELECT COUNT(*) FROM candidates WHERE party = 'JVP';",
    },
    {
        "input": "List all candidates with 'Lawyer' in their qualifications.",
        "query": "SELECT * FROM candidates WHERE qualifications LIKE '%Lawyer%';",
    },
]

def create_sql_agent_module():
    db = SQLDatabase.from_uri("postgresql://Denuwan:rsqY2Jbj7CZQ@ep-dark-frog-a5hpd82n.us-east-2.aws.neon.tech/Election?sslmode=require")
    print("Dialect:", db.dialect)
    try:
        tables = db.get_usable_table_names()
        print("Tables:", tables)
    except SQLAlchemyError as e:
        print(f"Error fetching table names: {e}")

    try:
        result = db.run("SELECT * FROM candidates LIMIT 10;")
        print("Query Result:", result)
    except SQLAlchemyError as e:
        print(f"Query Execution Error: {e}")

    llm = get_llm()

    tool_kit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )

    example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
    prompt = FewShotPromptTemplate(
        examples=examples[:5],
        example_prompt=example_prompt,
        prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
        suffix="User input: {input}\nSQL query: ",
        input_variables=["input", "top_k", "table_info"],
    )
    
    
    

    # Define the verdict_chain
    verdict_prompt = PromptTemplate.from_template(prompt)
    sql_chain = (
        {"input": RunnablePassthrough()}
        | verdict_prompt
        | llm
        | StrOutputParser()
    )

    return agent_executor, verdict_chain

if __name__ == "__main__":
    agent, verdict_chain = create_sql_agent_module()
    
    def answer_question(question):
        try:
            res = agent.invoke(question, handle_parsing_errors=True)
            return res
        except OutputParserException as e:
            print(f"Output Parsing Error: {e}")
            try:
                res = agent.invoke("List all candidates with their details.", handle_parsing_errors=True)
                return res
            except OutputParserException as retry_e:
                print(f"Retry Output Parsing Error: {retry_e}")
                return "I don't know."

    # Example usage
    question = "List all candidates from the 'Colombo' district with their details."
    answer = answer_question(question)
    print("Answer:", answer)