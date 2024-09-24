import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLite database connection - change the absolute path to the database file, if required
SQLALCHEMY_DATABASE_URL = "sqlite:///D:/youtube_analytics_backend/data/analytics_db.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the session for each request
def sql_db():
    """
    Dependency that provides a session to interact with the database.
    Ensuring that the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {e}")
    finally:
        db.close()
