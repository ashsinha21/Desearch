from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, text
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.services.db import get_db, SearchMetric
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/metrics")
async def get_metrics(
    days: int = 30,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get search metrics including:
    - Total searches
    - Searches per day
    - Top search queries
    - Hit rate
    """
    try:
        # Total searches
        total_searches = await db.scalar(
            select(func.count(SearchMetric.id))
        ) or 0
        
        # Searches per day
        days_ago = datetime.utcnow() - timedelta(days=days)
        
        searches_per_day = await db.execute(
            select([
                func.date_trunc('day', SearchMetric.created_at).label('day'),
                func.count(SearchMetric.id).label('count')
            ])
            .where(SearchMetric.created_at >= days_ago)
            .group_by('day')
            .order_by('day')
        )
        
        # Top search queries
        top_queries = await db.execute(
            select([
                SearchMetric.query,
                func.count(SearchMetric.id).label('count')
            ])
            .group_by(SearchMetric.query)
            .order_by(text('count DESC'))
            .limit(limit)
        )
        
        # Hit rate (searches with results / total searches)
        successful_searches = await db.scalar(
            select(func.count(SearchMetric.id))
            .where(SearchMetric.results_count > 0)
        ) or 0
        
        hit_rate = (successful_searches / total_searches * 100) if total_searches > 0 else 0
        
        return {
            "total_searches": total_searches,
            "searches_per_day": [
                {"date": day.strftime('%Y-%m-%d'), "count": count}
                for day, count in searches_per_day.all()
            ],
            "top_queries": [
                {"query": query, "count": count}
                for query, count in top_queries.all()
            ],
            "hit_rate": round(hit_rate, 2)
        }
        
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")
