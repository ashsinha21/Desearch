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

    async def search_questions(
        self, 
        query: str, 
        filters: Optional[str] = None, 
        limit: int = 10
    ) -> dict:
        try:
            # Prepare the search payload
            payload = {
                'q': query,
                'limit': limit,
                'showMatchesPosition': True,
                'matchingStrategy': 'all'
            }
            
            # Add filters if provided
            if filters:
                payload['filter'] = filters
            
            # Execute the search using the HTTP client directly
            response = await self.async_index._http_requests.post(
                f"indexes/{self.async_index.uid}/search",
                body=payload
            )
            
            # Parse the response
            result = response.json()
            
            # Log search metrics
            logger.info(
                f"Search completed - Query: '{query}', "
                f"Found: {len(result.get('hits', []))} results, "
                f"Took: {result.get('processingTimeMs', 0)}ms"
            )
            
            # Return results in the expected format
            return {
                'hits': result.get('hits', []),
                'estimated_total_hits': result.get('estimatedTotalHits', 0),
                'processing_time_ms': result.get('processingTimeMs', 0),
                'query': query
            }
            
        except Exception as e:
            error_msg = f"Search error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'hits': [],
                'estimated_total_hits': 0,
                'processing_time_ms': 0,
                'query': query,
                'error': error_msg
            }