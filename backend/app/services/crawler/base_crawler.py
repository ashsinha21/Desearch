from abc import ABC, abstractmethod
from typing import List, Dict, Any
import aiohttp
import logging

logger = logging.getLogger(__name__)

class BaseCrawler(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def fetch_questions(self, **kwargs) -> List[Dict[str, Any]]:
        """Fetch questions from the target platform"""
        pass

    @abstractmethod
    def normalize_question(self, raw_question: Dict[str, Any]) -> Dict[str, Any]:
        """Convert platform-specific question format to our standard format"""
        pass

    async def _make_request(self, url: str, method: str = 'GET', **kwargs) -> Any:
        """Helper method to make HTTP requests"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with")
            
        try:
            async with self.session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Error making request to {url}: {str(e)}")
            raise
