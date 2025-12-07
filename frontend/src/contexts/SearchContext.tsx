'use client'

import { createContext, useContext, ReactNode, useState } from 'react'

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
  search: (query: string) => Promise<void>
}

const SearchContext = createContext<SearchContextType | undefined>(undefined)

export function SearchProvider({ children }: { children: ReactNode }) {
  const [results, setResults] = useState<SearchResult[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

  const search = async (query: string) => {
    if (!query.trim()) return
    
    try {
      setIsLoading(true)
      setError(null)
      
      const searchParams = new URLSearchParams({ q: query.trim() })
      const response = await fetch(`${API_BASE_URL}/api/search?${searchParams.toString()}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      console.log(data);
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
    <SearchContext.Provider value={{ results, isLoading, error, search }}>
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
