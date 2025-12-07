'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { Search, ExternalLink } from 'lucide-react'
import { useSearch } from '@/contexts/SearchContext'

export default function SearchResults() {
  const { results, isLoading, error } = useSearch()

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <Card key={i} className="hover:shadow-md transition-shadow">
            <CardContent className="p-4">
              <Skeleton className="h-5 w-3/4 mb-1.5" />
              <Skeleton className="h-3.5 w-1/2" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12 text-destructive">
        <h3 className="text-lg font-medium">Error loading results</h3>
        <p className="text-sm mt-1">{error}</p>
      </div>
    )
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-muted-foreground mb-4">
          <Search className="h-12 w-12 mx-auto opacity-20" />
        </div>
        <h3 className="text-lg font-medium">
          {isLoading ? 'Searching...' : 'No results found'}
        </h3>
        {!isLoading && (
          <p className="text-muted-foreground text-sm mt-1">
            Try adjusting your search or filter to find what you're looking for.
          </p>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {results.map((result: any) => (
        <Card 
          key={result.id} 
          className="hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => window.open(result.url, '_blank')}
        >
          <CardContent className="p-4">
            <h3 className="font-medium text-base mb-1 line-clamp-1">{result.title}</h3>
            <div className="flex items-center justify-between mt-1">
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <span className="font-medium text-foreground">{result.platform}</span>
                <span>•</span>
                <span className={`${
                  result.difficulty === 'Easy' ? 'text-green-500' : 
                  result.difficulty === 'Medium' ? 'text-yellow-500' : 
                  'text-red-500'
                }`}>
                  {result.difficulty}
                </span>
                {result.tags?.length > 0 && (
                  <>
                    <span>•</span>
                    <span className="text-xs bg-muted px-2 py-0.5 rounded-full">
                      {result.tags[0]}
                      {result.tags.length > 1 ? '...' : ''}
                    </span>
                  </>
                )}
              </div>
              <ExternalLink className="h-3.5 w-3.5 text-muted-foreground" />
            </div>
            {result.description && (
              <p className="text-xs text-muted-foreground mt-1.5 line-clamp-1">
                {result.description}
              </p>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}