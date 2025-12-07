from typing import List, Dict, Any, Optional
from .meili_client import meili_client, async_meili_client, QUESTION_INDEX
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class Indexer:
    def __init__(self):
        self.index = meili_client.index(QUESTION_INDEX)
        self.async_index = async_meili_client.index(QUESTION_INDEX)

    async def index_question(self, question: Dict[str, Any]) -> None:
        """Index a single question document"""
        await self.async_index.add_documents([question])

    async def batch_index_questions(self, questions: List[Dict[str, Any]]) -> None:
        """Index multiple questions in a batch"""
        if questions:
            await self.async_index.add_documents(questions)

    async def search_questions(self, query: str, filters: Optional[str] = None, limit: int = 10) -> dict:
        """Search questions with optional filters"""
        try:
            # For MeiliSearch v1.0+ compatibility
            params = {
                'q': query,
                'limit': limit,
                'attributesToRetrieve': ['*'],
                'showMatchesPosition': True
            }
            
            if filters:
                params['filter'] = filters
            
            # Use the search method with explicit parameters
            response = await self.async_index._http_requests.post(
                f"indexes/{self.async_index.uid}/search",
                body=params
            )
            
            # Parse the response
            result = response.json()
                        
            # Convert to the expected format
            return {
                'hits': result.get('hits', []),  # Using .get() for safety
                'estimated_total_hits': result.get('estimatedTotalHits', 0),  # camelCase
                'processing_time_ms': result.get('processingTimeMs', 0),  # camelCase
                'query': query
            }
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise  # Re-raise to be handled by the API route
