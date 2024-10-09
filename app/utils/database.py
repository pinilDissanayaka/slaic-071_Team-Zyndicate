from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from sqlalchemy.exc import SQLAlchemyError
from utils.utils import get_llm

# Create the SQLDatabase object
db = SQLDatabase.from_uri("postgresql://Denuwan:rsqY2Jbj7CZQ@ep-dark-frog-a5hpd82n.us-east-2.aws.neon.tech/Election?sslmode=require")

# Print the SQL dialect being used (optional)
print("Dialect:", db.dialect)

# Get table names
try:
    tables = db.get_usable_table_names()
    print("Tables:", tables)
except SQLAlchemyError as e:
    print(f"Error fetching table names: {e}")

# Run the query
try:
    result = db.run("SELECT * FROM candidates LIMIT 10;")
    print("Query Result:", result)
except SQLAlchemyError as e:
    print(f"Query Execution Error: {e}")

llm = get_llm()
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
res = agent_executor.invoke(
    "List the total sales per country. Which country's customers spent the most?"
)