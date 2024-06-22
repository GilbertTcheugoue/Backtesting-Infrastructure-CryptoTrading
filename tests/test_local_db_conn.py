import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import configparser

def get_database_url():
  """Parse the alembic.ini file to extract the database connection string."""
  config = configparser.ConfigParser()
  config.read('alembic.ini')  # Adjust the path if necessary
  return config.get('alembic', 'sqlalchemy.url')


def test_database_connection():
  """Test the database connection using the URL from alembic.ini."""
  database_url = get_database_url()
  try:
    engine = create_engine(database_url)
    with engine.connect() as connection:
      # Use the text construct for the query
      result = connection.execute(text("SELECT 1"))
      assert result.fetchone() is not None
  except SQLAlchemyError as e:
    pytest.fail(f"Database connection failed: {e}")