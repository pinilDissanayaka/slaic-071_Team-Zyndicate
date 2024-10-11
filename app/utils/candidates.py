import os
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from utils import get_llm
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

def get_engine_for_postgres_db():
    """Connect to the PostgreSQL database and create engine."""
    postgres_uri = os.getenv("DB")
    if not postgres_uri:
        raise ValueError("DB environment variable is not set")
    return create_engine(postgres_uri, poolclass=NullPool)

def candidate_finder(user_query: str):
    try:
        engine = get_engine_for_postgres_db()
        db = SQLDatabase(engine)
        llm = get_llm()

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        tools = toolkit.get_tools()

        SQL_PREFIX = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct SQL query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the PostgreSQL database.
        Only use the below tools and the information returned by them to construct your final answer.
        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        Always start by looking at the schema of the relevant tables."""

        system_message = SystemMessage(content=SQL_PREFIX)
        agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)

        responses = agent_executor.invoke({"messages": [HumanMessage(content=user_query)]})
        
        # Process the final response
        final_answer = responses['messages'][-1].content if responses['messages'] else "No response generated"
        return final_answer

    except ValueError as ve:
        return f"Configuration error: {str(ve)}"
    except Exception as e:
        return f"Error during query execution: {str(e)}"


if __name__ == "__main__":
    user_query = "List down all candidates and their eduction qulifications"
    results = candidate_finder(user_query)
    print(results)
