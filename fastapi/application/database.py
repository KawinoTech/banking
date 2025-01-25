from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

# Generate a random secret key for cryptographic purposes
SECRET_KEY = os.urandom(32)

# Build the database URI from the configuration settings
SQLALCHEMY_DATABASE_URI = f'mysql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}'

# Create an engine with connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_size=20,          # Number of connections to maintain in the pool
    max_overflow=0,        # Max overflow connections beyond the pool_size
    pool_timeout=30,       # Timeout for getting a connection from the pool
    pool_recycle=3600,     # Time (in seconds) before a connection is recycled
    echo=True              # Enable SQL query logging (for debugging purposes)
)

# Create a session maker, which binds the session to the engine
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    """
    Yields a database session object. This function is intended for dependency injection
    in FastAPI routes.
    The session is automatically closed after use, even if an exception occurs.
    """
    db = session()  # Start a new session
    try:
        yield db  # Allow use of the session in database operations
    finally:
        db.close()  # Ensure the session is closed after the operation, even in case of an error

