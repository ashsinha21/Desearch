import os
import logging
import time
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from meilisearch_python_sdk import Client, AsyncClient
from meilisearch_python_sdk.models.settings import MeilisearchSettings, TypoTolerance, MinWordSizeForTypos, Pagination

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def get_env_variable(name: str, default: Optional[str] = None) -> str:
    """Get environment variable or raise an error if not found and no default provided."""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value

def initialize_meilisearch_client(max_retries: int = 3, retry_delay: int = 2):
    """Initialize MeiliSearch client with retry logic."""
    MEILI_HOST = get_env_variable("MEILI_HOST", "http://meilisearch:7700")
    MEILI_MASTER_KEY = get_env_variable("MEILI_MASTER_KEY", "")
    
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to MeiliSearch (Attempt {attempt + 1}/{max_retries})")
            
            # Initialize clients
            sync_client = Client(MEILI_HOST, MEILI_MASTER_KEY, timeout=10)
            async_client = AsyncClient(MEILI_HOST, MEILI_MASTER_KEY, timeout=10)
            
            # Test the connection
            sync_client.health()
            
            logger.info("Successfully connected to MeiliSearch")
            return sync_client, async_client
            
        except Exception as e:
            last_exception = e
            logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    logger.error("Max retries reached. Could not connect to MeiliSearch.")
    raise ConnectionError(f"Failed to connect to MeiliSearch after {max_retries} attempts") from last_exception

# Initialize clients
try:
    meili_client, async_meili_client = initialize_meilisearch_client()
except Exception as e:
    logger.critical(f"Critical: Could not initialize MeiliSearch clients: {str(e)}")
    raise

# Index names
QUESTION_INDEX = "questions"

async def init_meilisearch() -> None:
    """Initialize MeiliSearch index with proper settings.
    
    Creates the index if it doesn't exist and configures the settings.
    """
    try:
        logger.info("Initializing MeiliSearch index")
        
        # Check if index exists
        try:
            index = meili_client.get_index(QUESTION_INDEX)
            logger.info(f"Index {QUESTION_INDEX} already exists")
            return
        except Exception:
            # Index doesn't exist, create it
            pass
        
        # Create index with primary key
        logger.info(f"Creating index: {QUESTION_INDEX}")
        meili_client.create_index(uid=QUESTION_INDEX, primary_key='id')
        
        # Configure index settings with proper typing
        settings = MeilisearchSettings(
            filterable_attributes=[
                'platform',
                'difficulty',
                'tags'
            ],
            sortable_attributes=[
                'created_at'
            ],
            searchable_attributes=[
                'title',
                'content',
                'tags',
                'platform'
            ],
            # Performance optimizations
            typo_tolerance=TypoTolerance(
                enabled=True,
                min_word_size_for_typos=MinWordSizeForTypos(one_typo=5, two_typos=9)
            ),
            pagination=Pagination(max_total_hits=1000)
        )
        
        # Update settings
        index = meili_client.index(QUESTION_INDEX)
        index.update_settings(settings)
        
        logger.info(f"Successfully configured index: {QUESTION_INDEX}")
        
    except Exception as e:
        logger.error(f"Failed to initialize MeiliSearch: {str(e)}", exc_info=True)
        raise
