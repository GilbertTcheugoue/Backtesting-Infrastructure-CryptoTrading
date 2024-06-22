from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import configparser

# Load the connection string from alembic.ini
config = configparser.ConfigParser()
config.read('../alembic.ini')  # Adjust the path if necessary
connection_string = config.get('alembic', 'sqlalchemy.url')

# Attempt to connect to the database
try:
  engine = create_engine(connection_string)
  with engine.connect() as connection:
    print("Successfully connected to the database.")
    # You can also perform a simple query if necessary
    # Example: connection.execute("SELECT 1")
except SQLAlchemyError as e:
  print(f"An error occurred: {e}")

# The connection is automatically closed when exiting the 'with' block