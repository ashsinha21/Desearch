import os
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from meilisearch_python_sdk import Client, AsyncClient
from meilisearch_python_sdk.models.settings import MeilisearchSettings, TypoTolerance, MinWordSizeForTypos, Pagination

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get environment variables with validation
def get_env_variable(name: str, default: Optional[str] = None) -> str:
    """Get environment variable or raise an error if not found and no default provided."""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value

# Load configuration
MEILI_HOST = get_env_variable("MEILI_HOST", "http://localhost:7700")
MEILI_MASTER_KEY = get_env_variable("MEILI_MASTER_KEY", "masterKey")

# Initialize clients with error handling
try:
    meili_client = Client(MEILI_HOST, MEILI_MASTER_KEY, timeout=10)
    async_meili_client = AsyncClient(MEILI_HOST, MEILI_MASTER_KEY, timeout=10)
    logger.info("Successfully initialized MeiliSearch clients")
except Exception as e:
    logger.error(f"Failed to initialize MeiliSearch clients: {str(e)}")
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
