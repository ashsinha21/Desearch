'use client'

import { SearchProvider } from '@/contexts/SearchContext'

export function Providers({ children }: { children: React.ReactNode }) {
  return <SearchProvider>{children}</SearchProvider>
}
