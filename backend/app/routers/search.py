from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.services.db import get_db, SearchMetric
from app.services.indexer import Indexer
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.search import SearchQuery 
from sqlalchemy import insert
import logging
import traceback

router = APIRouter()
indexer = Indexer()
logger = logging.getLogger(__name__)

@router.get("/search")
async def search_questions(
    search_query: SearchQuery = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Search request - {search_query.model_dump()}")
        
        # Build filters
        filters = []
        if search_query.platform:
            filters.append(f"platform = '{search_query.platform}'")
            
        if search_query.difficulty:
            filters.append(f"difficulty = '{search_query.difficulty}'")
            
        if search_query.tags:
            tag_list = [tag.strip() for tag in search_query.tags.split(',')]
            tag_filters = [f"tags IN ['{tag}']" for tag in tag_list]
            filters.append(f"({' OR '.join(tag_filters)})")
            
        filter_query = " AND ".join(filters) if filters else None
        
        result = await indexer.search_questions(
            query=search_query.q,
            filters=filter_query,
            limit=search_query.limit
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your search"
        )