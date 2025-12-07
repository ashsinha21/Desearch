'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { Search } from 'lucide-react'

export default function SearchResults() {
  const isLoading = false
  const results: any[] = []

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <Card key={i} className="hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <Skeleton className="h-6 w-3/4 mb-2" />
              <Skeleton className="h-4 w-1/2" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-muted-foreground mb-4">
          <Search className="h-12 w-12 mx-auto opacity-20" />
        </div>
        <h3 className="text-lg font-medium">No results found</h3>
        <p className="text-muted-foreground text-sm mt-1">
          Try adjusting your search or filter to find what you're looking for.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {results.map((result) => (
        <Card 
          key={result.id} 
          className="hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => window.open(result.url, '_blank')}
        >
          <CardContent className="p-6">
            <h3 className="font-medium mb-1">{result.title}</h3>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>{result.platform}</span>
              <span>•</span>
              <span>{result.difficulty}</span>
              <span>•</span>
              <span>{result.topics?.join(', ')}</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}