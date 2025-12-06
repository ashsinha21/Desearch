from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func, Text, ARRAY
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables from .env.local if it exists, otherwise .env
env_path = Path('.') / '.env.local'
if not env_path.exists():
    env_path = Path('.') / '.env'

load_dotenv(env_path)

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set")
    raise ValueError("DATABASE_URL environment variable is required")

try:
    # Configure SQLAlchemy engine
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,  # Set to False in production
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800,
    )
    
    # Create async session factory
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    
    logger.info("Database engine and session configured successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize database connection: {str(e)}")
    raise
Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    tags = Column(PG_ARRAY(String), default=[])
    url = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SearchMetric(Base):
    __tablename__ = "search_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    results_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency
def get_db() -> AsyncSession:
    db = async_session()
    try:
        yield db
    finally:
        db.close()
