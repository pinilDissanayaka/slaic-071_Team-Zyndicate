import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from utils.utils import get_llm
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

class CandidateAgent:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.engine = self._get_engine()
        self.db = SQLDatabase(self.engine)
        self.llm = get_llm()
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.tools = self.toolkit.get_tools()
        self.agent_executor = self._initialize_agent()

    def _get_engine(self):
        """Connect to the PostgreSQL database and create engine."""
        return create_engine(self.db_uri, poolclass=NullPool)

    def _initialize_agent(self):
        """Initialize the agent with the necessary tools and messages."""
        SQL_PREFIX = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        To start you should ALWAYS look at the tables in the database to see what you can query.
        Do NOT skip this step.
        Then you should query the schema of the most relevant tables."""

        system_message = SystemMessage(content=SQL_PREFIX)
        return create_react_agent(self.llm, self.tools, messages_modifier=system_message)

    def query_candidates(self, user_query):
        """Query the candidates based on the user's query."""
        query_message = HumanMessage(content=user_query)
        responses = []
        for response in self.agent_executor.stream({"messages": [query_message]}):
            responses.append(response)
        return responses

# Streamlit app
def agent():
    st.title("Election Insight App")
    db_uri = st.text_input("Enter the database URI:")
    if db_uri:
        agent = CandidateAgent(db_uri)
        user_query = st.text_area("Enter your query:")
        if st.button("Submit"):
            responses = agent.query_candidates(user_query)
            for response in responses:
                st.write(response)
                st.write("----")

