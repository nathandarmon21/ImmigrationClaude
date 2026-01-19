import { useState, useEffect } from 'react'
import { ExternalLink, Calendar, ChevronDown, ChevronUp, AlertCircle } from 'lucide-react'

interface Update {
  title: string
  date: string
  source: string
  source_url: string
  summary: string
  full_text?: string
  category: string
}

export default function UpdatesPage() {
  const [updates, setUpdates] = useState<Update[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<number | null>(null)
  const [fullTextCache, setFullTextCache] = useState<{[key: number]: any}>({})

  useEffect(() => {
    fetchUpdates()
  }, [])

  const fetchUpdates = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/updates/latest`)
      const data = await response.json()
      setUpdates(data.updates || [])
    } catch (error) {
      console.error('Failed to fetch updates:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchFullText = async (updateIndex: number, sourceUrl: string) => {
    if (fullTextCache[updateIndex]) {
      return // Already fetched
    }

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || ''}/updates/details?source_url=${encodeURIComponent(sourceUrl)}`
      )
      const data = await response.json()
      setFullTextCache(prev => ({ ...prev, [updateIndex]: data }))
    } catch (error) {
      console.error('Failed to fetch full text:', error)
    }
  }

  const toggleExpanded = (index: number, sourceUrl: string) => {
    if (expandedId === index) {
      setExpandedId(null)
    } else {
      setExpandedId(index)
      fetchFullText(index, sourceUrl)
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'executive_order':
        return 'bg-red-100 text-red-800'
      case 'policy_update':
        return 'bg-blue-100 text-blue-800'
      case 'visa_bulletin':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'executive_order':
        return 'Executive Order'
      case 'policy_update':
        return 'Policy Update'
      case 'visa_bulletin':
        return 'Visa Bulletin'
      default:
        return 'Update'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading latest updates...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold text-gray-900 mb-3">
            Immigration Law Updates
          </h1>
          <p className="text-lg text-gray-600">
            Stay informed about the latest changes in US immigration policy, visa bulletins, and executive orders.
          </p>
          <div className="mt-4 flex items-center text-sm text-gray-500">
            <AlertCircle size={16} className="mr-2" />
            <span>Updates are refreshed every 6 hours from official government sources</span>
          </div>
        </div>

        {updates.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600">No updates available at this time.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {updates.map((update, index) => (
              <div key={index} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${getCategoryColor(update.category)}`}>
                        {getCategoryLabel(update.category)}
                      </span>
                      <span className="text-sm text-gray-500 flex items-center">
                        <Calendar size={14} className="mr-1" />
                        {new Date(update.date).toLocaleDateString()}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {update.title}
                    </h3>
                    <p className="text-gray-600 mb-3">
                      {update.summary}
                    </p>
                    <div className="flex items-center gap-3">
                      <span className="text-sm text-gray-500">Source: {update.source}</span>
                      <a
                        href={update.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-700 text-sm flex items-center gap-1"
                      >
                        View Official Source
                        <ExternalLink size={14} />
                      </a>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => toggleExpanded(index, update.source_url)}
                  className="mt-4 flex items-center text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  {expandedId === index ? (
                    <>
                      <ChevronUp size={18} className="mr-1" />
                      Hide Full Details
                    </>
                  ) : (
                    <>
                      <ChevronDown size={18} className="mr-1" />
                      Show Full Legal Text
                    </>
                  )}
                </button>

                {expandedId === index && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    {fullTextCache[index] ? (
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-semibold mb-2">Full Text:</h4>
                        <div className="text-sm text-gray-700 whitespace-pre-wrap max-h-96 overflow-y-auto">
                          {fullTextCache[index].full_text || 'Full text not available. Visit the official source for complete details.'}
                        </div>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                        <span className="ml-3 text-gray-600">Loading full text...</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Last refreshed: {new Date().toLocaleString()}</p>
          <p className="mt-2">
            For the most up-to-date information, always refer to official government sources.
          </p>
        </div>
      </div>
    </div>
  )
}
