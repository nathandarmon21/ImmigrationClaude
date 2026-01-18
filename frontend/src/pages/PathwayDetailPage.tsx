import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useUserStore } from '../store/userStore'
import { immigrationApi } from '../services/api'
import { ArrowLeft, CheckCircle, XCircle, Clock, DollarSign, ExternalLink, FileText, Loader } from 'lucide-react'
import type { PathwayInfo } from '../types'

export default function PathwayDetailPage() {
  const { pathwayId } = useParams<{ pathwayId: string }>()
  const navigate = useNavigate()
  const { profile } = useUserStore()

  const [pathway, setPathway] = useState<PathwayInfo | null>(null)
  const [nextSteps, setNextSteps] = useState<string>('')
  const [documentChecklist, setDocumentChecklist] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      if (!pathwayId) return

      try {
        const [pathwayData, stepsData, checklistData] = await Promise.all([
          immigrationApi.getPathwayDetails(pathwayId),
          immigrationApi.getNextSteps(pathwayId, profile as any),
          immigrationApi.getDocumentChecklist(pathwayId, profile as any),
        ])

        setPathway(pathwayData)
        setNextSteps(stepsData)
        setDocumentChecklist(checklistData)
      } catch (error) {
        console.error('Failed to fetch pathway details:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [pathwayId, profile])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 flex items-center justify-center">
        <Loader className="animate-spin text-primary-600" size={48} />
      </div>
    )
  }

  if (!pathway) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-2xl font-bold mb-4">Pathway Not Found</h1>
          <button onClick={() => navigate('/results')} className="btn-primary">
            Back to Results
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-5xl">
        <button
          onClick={() => navigate(-1)}
          className="btn-secondary inline-flex items-center space-x-2 mb-6"
        >
          <ArrowLeft size={18} />
          <span>Back</span>
        </button>

        {/* Header */}
        <div className="card mb-6">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{pathway.name}</h1>
          <p className="text-xl text-gray-700 mb-4">{pathway.detailed_description}</p>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center space-x-2">
              <Clock size={18} className="text-gray-500" />
              <span className="text-sm">
                <span className="font-semibold">Timeline:</span> {pathway.typical_timeline}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <DollarSign size={18} className="text-gray-500" />
              <span className="text-sm">
                <span className="font-semibold">Cost:</span> {pathway.cost_range}
              </span>
            </div>
          </div>
        </div>

        {/* Requirements */}
        <div className="card mb-6">
          <h2 className="text-2xl font-bold mb-4">Requirements</h2>
          <div className="space-y-4">
            {pathway.requirements.map((req, idx) => (
              <div key={idx} className="border-l-4 border-primary-500 pl-4">
                <h3 className="font-semibold text-gray-900">{req.name}</h3>
                <p className="text-gray-600">{req.description}</p>
                {req.alternatives && req.alternatives.length > 0 && (
                  <p className="text-sm text-gray-500 mt-1">
                    <span className="font-medium">Alternatives:</span>{' '}
                    {req.alternatives.join('; ')}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Pros and Cons */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="card">
            <h2 className="text-2xl font-bold mb-4 flex items-center space-x-2">
              <CheckCircle className="text-green-600" />
              <span>Advantages</span>
            </h2>
            <ul className="space-y-2">
              {pathway.advantages.map((adv, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="text-green-600 mr-2">✓</span>
                  <span className="text-gray-700">{adv}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="card">
            <h2 className="text-2xl font-bold mb-4 flex items-center space-x-2">
              <XCircle className="text-red-600" />
              <span>Disadvantages</span>
            </h2>
            <ul className="space-y-2">
              {pathway.disadvantages.map((dis, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="text-red-600 mr-2">✗</span>
                  <span className="text-gray-700">{dis}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Success Factors */}
        <div className="card mb-6">
          <h2 className="text-2xl font-bold mb-4">Success Factors</h2>
          <ul className="grid md:grid-cols-2 gap-3">
            {pathway.success_factors.map((factor, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-primary-600 mr-2">•</span>
                <span className="text-gray-700">{factor}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Common Denials */}
        <div className="card mb-6 bg-red-50 border-red-200">
          <h2 className="text-2xl font-bold mb-4 text-red-900">Common Reasons for Denial</h2>
          <ul className="space-y-2">
            {pathway.common_denials.map((denial, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-red-600 mr-2">⚠</span>
                <span className="text-gray-700">{denial}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Next Steps (AI-Generated) */}
        {nextSteps && (
          <div className="card mb-6 bg-blue-50 border-blue-200">
            <h2 className="text-2xl font-bold mb-4">Personalized Action Plan</h2>
            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
              {nextSteps}
            </div>
          </div>
        )}

        {/* Document Checklist */}
        {documentChecklist && (
          <div className="card mb-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center space-x-2">
              <FileText className="text-primary-600" />
              <span>Document Checklist</span>
            </h2>
            <ul className="space-y-2">
              {documentChecklist.documents_required?.map((doc: string, idx: number) => (
                <li key={idx} className="flex items-start">
                  <input
                    type="checkbox"
                    className="mt-1 mr-3"
                    id={`doc-${idx}`}
                  />
                  <label htmlFor={`doc-${idx}`} className="text-gray-700">
                    {doc}
                  </label>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Official Resources */}
        <div className="card">
          <h2 className="text-2xl font-bold mb-4">Official Resources</h2>
          <div className="space-y-2">
            {pathway.official_links.map((link, idx) => (
              <a
                key={idx}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
              >
                <ExternalLink size={16} />
                <span>{link.title}</span>
              </a>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="mt-8 text-center">
          <button
            onClick={() => navigate('/chat')}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <span>Have Questions? Ask Our AI Advisor</span>
          </button>
        </div>
      </div>
    </div>
  )
}
