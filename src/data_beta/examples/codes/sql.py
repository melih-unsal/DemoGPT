# SQL
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# Create an SQLDatabase object from the URI of the SQLite database
db = SQLDatabase.from_uri("sqlite:///../../../../notebooks/Chinook.db")

# Create an OpenAI object with the desired temperature and verbosity
llm = OpenAI(temperature=0, verbose=True)

# Create an SQLDatabaseChain object from the OpenAI object and the SQLDatabase object
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Run a query on the database
result = db_chain.run("How many employees are there?")
print(result)
