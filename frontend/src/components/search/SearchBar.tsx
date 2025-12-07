'use client'

import { Search } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useState, useRef, useEffect } from 'react'
import { useSearch } from '@/contexts/SearchContext'

export default function SearchBar() {
  const [query, setQuery] = useState('')
  const { search, isLoading } = useSearch()
  const searchButtonRef = useRef<HTMLButtonElement>(null)

  const handleSearch = () => {
    if (!query.trim()) return
    search(query)
  }

  // Handle Enter key press
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

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
          onKeyDown={handleKeyDown}
        />
        <Button 
          ref={searchButtonRef}
          className="absolute right-2 top-1/2 -translate-y-1/2"
          onClick={handleSearch}
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? 'Searching...' : 'Search'}
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