// frontend/src/app/page.tsx
import SearchBar from '@/components/search/SearchBar'
import SearchResults from '@/components/search/SearchResults'

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-2">DeSearch</h1>
        <p className="text-muted-foreground text-center mb-8">
          Search programming questions across multiple platforms
        </p>
        
        <SearchBar />
        <SearchResults />
      </div>
    </div>
  )
}