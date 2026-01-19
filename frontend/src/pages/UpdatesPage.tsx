import { useState, useEffect } from 'react'
import { ExternalLink, Calendar, ChevronDown, ChevronUp, AlertCircle } from 'lucide-react'
import api from '../services/api'
import { useUserStore } from '../store/userStore'

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
  const [error, setError] = useState<string | null>(null)
  const [expandedId, setExpandedId] = useState<number | null>(null)
  const { recommendations } = useUserStore()

  useEffect(() => {
    fetchUpdates()
  }, [recommendations])

  const fetchUpdates = async () => {
    try {
      // Get top 3 pathway IDs from recommendations
      const pathwayIds = recommendations.slice(0, 3).map(rec => rec.pathway_id)

      // Build query params
      const params: any = { limit: 10 }
      if (pathwayIds.length > 0) {
        params.pathways = pathwayIds.join(',')
      }

      console.log('Fetching updates with pathways:', pathwayIds)
      const response = await api.get('/updates/latest', { params })
      console.log('Updates response:', response.data)
      setUpdates(response.data.updates || [])
      setError(null)
    } catch (error: any) {
      console.error('Failed to fetch updates:', error)
      console.error('Error details:', error.response?.data || error.message)
      setError(error.response?.data?.detail || error.message || 'Failed to load updates')
    } finally {
      setLoading(false)
    }
  }

  const toggleExpanded = (index: number) => {
    setExpandedId(expandedId === index ? null : index)
  }

  const formatFullText = (text: string) => {
    // Split by sentences and add line breaks for readability
    return text
      .replace(/\. /g, '.\n\n')  // Add double line break after periods
      .replace(/: /g, ':\n')     // Add line break after colons
      .replace(/\(\d+\)/g, '\n$&')  // Add line break before numbered items like (1), (2)
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

        {error && (
          <div className="card bg-red-50 border-red-200 mb-6">
            <div className="flex items-center text-red-800">
              <AlertCircle size={20} className="mr-2" />
              <div>
                <p className="font-semibold">Error loading updates</p>
                <p className="text-sm mt-1">{error}</p>
                <p className="text-sm mt-2">API URL: {api.defaults.baseURL || 'Not configured'}</p>
              </div>
            </div>
          </div>
        )}

        {updates.length === 0 && !error ? (
          <div className="card text-center py-12">
            <p className="text-gray-600">No updates available at this time.</p>
          </div>
        ) : !error ? (
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

                {update.full_text && (
                  <>
                    <button
                      onClick={() => toggleExpanded(index)}
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
                        <div className="bg-gray-50 p-6 rounded-lg">
                          <h4 className="font-semibold text-gray-900 mb-4 text-base">Full Legal Text:</h4>
                          <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-line max-h-96 overflow-y-auto">
                            {formatFullText(update.full_text)}
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>
            ))}
          </div>
        ) : null}

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
