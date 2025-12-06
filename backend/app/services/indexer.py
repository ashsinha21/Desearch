from typing import List, Dict, Any, Optional
from .meili_client import meili_client, async_meili_client, QUESTION_INDEX
from datetime import datetime

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
            search_params = {
                'limit': limit,
                'attributes_to_retrieve': ['*'],
                'show_matches_position': True,
                'show_ranking_score': False  # Disable ranking score to avoid compatibility issues
            }
            
            if filters:
                print(f"Applying filters: {filters}")
                search_params['filter'] = filters
            
            # Use the search method with explicit parameters
            print(f"Searching with params: {search_params}")
            result = await self.async_index.search(
                query,
                limit=limit,
                filter=filters,
                attributes_to_retrieve=['*'],
                show_matches_position=True
            )
            
            print(f"Search result count: {len(result.hits) if result.hits else 0}")
            
            # Convert to the expected format
            return {
                'hits': result.hits,
                'estimated_total_hits': result.estimated_total_hits,
                'processing_time_ms': result.processing_time_ms,
                'query': query
            }
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            print(f"Query: {query}, Filters: {filters}")
            raise
