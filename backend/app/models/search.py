from pydantic import BaseModel, Field
from typing import List, Optional

class SearchQuery(BaseModel):
    q: Optional[str] = Field(None, min_length=0, max_length=200, description="Search query string")
    platform: Optional[str] = Field(None, description="Filter by platform (e.g., 'LeetCode')")
    difficulty: Optional[str] = Field(None, description="Filter by difficulty level")
    tags: Optional[str] = Field(None, description="Comma-separated list of tags to filter by")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of results to return")