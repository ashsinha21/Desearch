// frontend/src/components/search/SearchBar.tsx
'use client'

import { Search } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useState, useRef, useEffect } from 'react'
import { useSearch } from '@/contexts/SearchContext'

// Common tags that appear in coding questions
const COMMON_TAGS = [
  'Array', 'String', 'Hash Table', 'Dynamic Programming', 'Math',
  'Sorting', 'Greedy', 'Depth-First Search', 'Binary Search'
]

export default function SearchBar() {
  const [query, setQuery] = useState('')
  const { 
    search, 
    isLoading, 
    selectedDifficulty, 
    setSelectedDifficulty,
    selectedTags,
    toggleTag
  } = useSearch()
  const searchButtonRef = useRef<HTMLButtonElement>(null)

  const handleSearch = () => {
    if (!query.trim()) return
    search(query, selectedDifficulty, selectedTags)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="relative mb-8 w-full max-w-4xl mx-auto">
      {/* Search Input */}
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

      {/* Filters Section - Minimal Style */}
      <div className="mt-4 space-y-3">
        {/* Difficulty Filter */}
        <div>
          <div className="flex items-center space-x-2 text-sm">
            <span className="text-muted-foreground">Difficulty:</span>
            {(['Easy', 'Medium', 'Hard'] as const).map((level) => (
              <button
                key={level}
                className={`px-2 py-1 rounded text-sm ${
                  selectedDifficulty === level 
                    ? 'bg-primary text-primary-foreground' 
                    : 'hover:bg-muted'
                }`}
                onClick={() => setSelectedDifficulty(
                  selectedDifficulty === level ? '' : level
                )}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        {/* Tags Filter */}
        <div>
          <div className="flex items-center flex-wrap gap-1 text-sm">
            <span className="text-muted-foreground mr-2">Tags:</span>
            {COMMON_TAGS.map((tag) => (
              <button
                key={tag}
                className={`px-2 py-1 rounded text-sm ${
                  selectedTags.includes(tag)
                    ? 'bg-primary text-primary-foreground' 
                    : 'hover:bg-muted'
                }`}
                onClick={() => toggleTag(tag)}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}