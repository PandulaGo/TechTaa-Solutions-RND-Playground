import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker # - Importing the necessary modules from SQLAlchemy to create a database engine, define a base class for models, and manage database sessions. 

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@localhost:5432/tasks",) # - Retrieve the database URL from environment variables, or use a default PostgreSQL connection string if not set. This URL specifies the database dialect, driver, username, password, host, port, and database name.

engine = create_engine(DATABASE_URL) # - Create a SQLAlchemy engine using the specified database URL. The engine is responsible for managing the connection pool and executing SQL statements against the database.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # - Create a session factory (SessionLocal) that will generate new Session objects when called. The sessions are configured to not autocommit changes and not autoflush pending changes to the database automatically.

class Base(DeclarativeBase): # - Define a base class for all ORM models. This class will be used as a superclass for all model classes, allowing SQLAlchemy to map them to database tables.
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # - Close the database session to free up resources and avoid connection leaks.