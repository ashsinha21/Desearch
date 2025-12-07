'use client'

import { Search } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useState } from 'react'

// Get the API URL from environment variables or fallback to localhost
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    try {
      setIsSearching(true);
      const searchParams = new URLSearchParams({ q: query.trim() });
      const response = await fetch(`${API_BASE_URL}/api/search?${searchParams.toString()}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Search results:', data);
      // Handle search results here
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  // Rest of your component remains the same
  return (
    <div className="relative mb-8">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          type="search"
          placeholder="Search questions..."
          className="pl-10 pr-24 py-6 text-base"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <Button 
          className="absolute right-2 top-1/2 -translate-y-1/2"
          onClick={handleSearch}
          disabled={isSearching || !query.trim()}
        >
          {isSearching ? 'Searching...' : 'Search'}
        </Button>
      </div>
      
      <div className="flex flex-wrap gap-4 mt-4">
        <div className="flex-1 min-w-[200px]">
          <label className="text-sm font-medium mb-1 block">Topics</label>
          <select className="w-full p-2 border rounded">
            <option>All Topics</option>
            <option>Algorithms</option>
            <option>Data Structures</option>
            <option>System Design</option>
          </select>
        </div>
        
        <div className="w-32">
          <label className="text-sm font-medium mb-1 block">Difficulty</label>
          <select className="w-full p-2 border rounded">
            <option>Any</option>
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
        </div>
      </div>
    </div>
  )
}