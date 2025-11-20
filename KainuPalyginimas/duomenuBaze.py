# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modeliaiSQL import Base

# Create the SQLite database
engine = create_engine("sqlite:///prices.db", echo=False)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """
    Creates all database tables.
    Call this once when the program starts.
    """
    Base.metadata.create_all(bind=engine)