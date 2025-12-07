// frontend/src/contexts/SearchContext.tsx
'use client'

import { createContext, useContext, ReactNode, useState } from 'react'

export type Difficulty = 'Easy' | 'Medium' | 'Hard' | ''

interface SearchResult {
  id: string
  title: string
  platform: string
  difficulty: string
  url: string
  tags?: string[]
  description?: string
}

interface SearchContextType {
  results: SearchResult[]
  isLoading: boolean
  error: string | null
  search: (query: string, difficulty?: Difficulty, tags?: string[]) => Promise<void>
  selectedDifficulty: Difficulty
  setSelectedDifficulty: (difficulty: Difficulty) => void
  selectedTags: string[]
  toggleTag: (tag: string) => void
}

const SearchContext = createContext<SearchContextType | undefined>(undefined)

export function SearchProvider({ children }: { children: ReactNode }) {
  const [results, setResults] = useState<SearchResult[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty>('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag) 
        : [...prev, tag]
    )
  }

  const search = async (query: string, difficulty?: Difficulty, tags?: string[]) => {
    if (!query.trim()) return
    
    try {
      setIsLoading(true)
      setError(null)
      
      const params = new URLSearchParams({ q: query.trim() })
      
      if (difficulty) {
        params.append('difficulty', difficulty)
      }
      
      if (tags && tags.length > 0) {
        params.append('tags', tags.join(','))
      }
      
      const response = await fetch(`${API_BASE_URL}/api/search?${params.toString()}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setResults(data.hits || [])
    } catch (err) {
      console.error('Search failed:', err)
      setError(err instanceof Error ? err.message : 'An error occurred during search')
      setResults([])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <SearchContext.Provider value={{ 
      results, 
      isLoading, 
      error, 
      search, 
      selectedDifficulty, 
      setSelectedDifficulty,
      selectedTags,
      toggleTag
    }}>
      {children}
    </SearchContext.Provider>
  )
}

export function useSearch() {
  const context = useContext(SearchContext)
  if (context === undefined) {
    throw new Error('useSearch must be used within a SearchProvider')
  }
  return context
}