from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.services.db import get_db, SearchMetric
from app.services.indexer import Indexer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
import logging
import traceback

router = APIRouter()
indexer = Indexer()
logger = logging.getLogger(__name__)

@router.get("/search")
async def search_questions(
    q: str = Query(..., min_length=1, max_length=200),
    platform: Optional[str] = None,
    difficulty: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for questions across all platforms
    """
    try:
        logger.info(f"Search request - query: {q}, platform: {platform}, difficulty: {difficulty}, tags: {tags}")
        
        # Build filters
        filters = []
        if platform:
            platform_filter = f"platform = '{platform}'"
            logger.debug(f"Adding platform filter: {platform_filter}")
            filters.append(platform_filter)
            
        if difficulty:
            # Convert to title case to match the stored data
            difficulty = difficulty.title()
            difficulty_filter = f"difficulty = '{difficulty}'"
            logger.debug(f"Adding difficulty filter: {difficulty_filter}")
            filters.append(difficulty_filter)
            
        if tags:
            tags_filter = " OR ".join([f"tags CONTAINS '{tag}'" for tag in tags])
            tags_filter = f"({tags_filter})"
            logger.debug(f"Adding tags filter: {tags_filter}")
            filters.append(tags_filter)
        
        filter_str = " AND ".join(filters) if filters else None
        logger.info(f"Final filter string: {filter_str}")
        
        # Search in Meilisearch
        search_results = await indexer.search_questions(q, filter_str)
        logger.info(f"Search successful. Found {len(search_results.get('hits', []))} results")
        
        # Log the search
        try:
            search_metric = SearchMetric(
                query=q,
                results_count=len(search_results.get('hits', [])),
                created_at=datetime.utcnow()
            )
            db.add(search_metric)
            await db.commit()
        except Exception as db_error:
            logger.error(f"Error logging search metric: {str(db_error)}")
            await db.rollback()
            # Don't fail the request if metric logging fails
        
        return {
            "query": q,
            "hits": search_results.get('hits', []),
            "estimated_total_hits": search_results.get('estimatedTotalHits', 0),
            "processing_time_ms": search_results.get('processingTimeMs', 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Search error: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
