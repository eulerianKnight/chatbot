from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

from config import get_settings

settings = get_settings()

# Construct the database URL
DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_ENDPOINT}:{settings.DB_PORT}/{settings.DB_NAME}"

try:
    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Test the connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))  # Simple query to check connectivity
        if result.scalar() == 1:
            print("Successfully connected to PostgreSQL database!")

    # Create a session factory (for interacting with the database)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Sanity check for usage
    def get_data():
        db = SessionLocal()  # Create a database session
        try:
           # Example Query
            result = db.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"Postgres Version : {version}")
            return version
        except Exception as e:
            print(f"Error during database operation: {e}")
            return None
        finally:
            db.close()

    db_version = get_data()
    if db_version:
        print("Database interaction successful")
    else:
        print("Database interaction failed")

except Exception as e:
    print(f"Error connecting to the database: {e}")

# Example using context manager for session:
from contextlib import contextmanager
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def another_data_function():
    with get_db() as db:
        try:
            result = db.execute(text("SELECT current_database();")) # Example query
            current_db = result.scalar()
            print(f"Current database: {current_db}")
            return current_db
        except Exception as e:
            print(f"Error in database operation {e}")
            return None
current_db = another_data_function()
if current_db:
    print("Database interaction successful")
else:
    print("Database interaction failed")
