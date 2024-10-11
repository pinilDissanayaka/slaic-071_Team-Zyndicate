import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy.exc import SQLAlchemyError
from langchain_groq.chat_models import ChatGroq
from langchain_google_genai import GoogleGenerativeAI
from utils import get_llm



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
agent_executor = create_sql_agent(llm, toolkit=tool_kit, verbose=True)
res=agent_executor.invoke("List the candidates who nominated from ratnapura ",handle_parsing_errors=True)
print(res)