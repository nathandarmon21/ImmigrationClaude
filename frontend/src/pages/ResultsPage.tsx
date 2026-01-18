import { useNavigate } from 'react-router-dom'
import { useUserStore } from '../store/userStore'
import { CheckCircle, XCircle, Clock, DollarSign, TrendingUp, ArrowRight } from 'lucide-react'

export default function ResultsPage() {
  const navigate = useNavigate()
  const { recommendations, togglePathwaySelection, selectedPathways } = useUserStore()

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-4xl text-center">
          <h1 className="text-3xl font-bold mb-4">No Recommendations Yet</h1>
          <p className="text-gray-600 mb-8">
            Please complete the assessment first to get personalized recommendations.
          </p>
          <button onClick={() => navigate('/assessment')} className="btn-primary">
            Start Assessment
          </button>
        </div>
      </div>
    )
  }

  const getFeasibilityColor = (feasibility: string) => {
    switch (feasibility) {
      case 'high':
        return 'text-green-600 bg-green-50'
      case 'medium':
        return 'text-yellow-600 bg-yellow-50'
      case 'low':
        return 'text-red-600 bg-red-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Your Immigration Pathways
          </h1>
          <p className="text-lg text-gray-600">
            Based on your profile, here are your personalized recommendations
          </p>
        </div>

        {selectedPathways.length > 0 && (
          <div className="mb-6 card bg-primary-50 border-primary-200">
            <div className="flex items-center justify-between">
              <p className="text-primary-900">
                {selectedPathways.length} pathway(s) selected for comparison
              </p>
              <button
                onClick={() => navigate('/compare')}
                className="btn-primary inline-flex items-center space-x-2"
              >
                <span>Compare Selected</span>
                <ArrowRight size={18} />
              </button>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {recommendations.map((rec) => (
            <div
              key={rec.pathway_id}
              className={`card cursor-pointer transition-all ${
                selectedPathways.includes(rec.pathway_id)
                  ? 'ring-2 ring-primary-500'
                  : ''
              }`}
              onClick={() => togglePathwaySelection(rec.pathway_id)}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-2xl font-bold text-gray-900">
                      {rec.pathway_name}
                    </h3>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${getFeasibilityColor(
                        rec.feasibility
                      )}`}
                    >
                      {rec.feasibility.toUpperCase()} Feasibility
                    </span>
                  </div>
                  <div className="flex items-center space-x-2 mb-4">
                    <TrendingUp size={18} className="text-primary-600" />
                    <span className="text-lg font-semibold text-primary-600">
                      {rec.fit_score.toFixed(0)}% Match
                    </span>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={selectedPathways.includes(rec.pathway_id)}
                  onChange={() => {}}
                  className="w-6 h-6 text-primary-600 rounded"
                  onClick={(e) => e.stopPropagation()}
                />
              </div>

              <p className="text-gray-700 mb-4">{rec.reasoning}</p>

              <div className="grid md:grid-cols-2 gap-4 mb-4">
                <div className="flex items-start space-x-2">
                  <Clock size={18} className="text-gray-500 mt-1 flex-shrink-0" />
                  <div>
                    <div className="text-sm font-semibold text-gray-700">Timeline</div>
                    <div className="text-sm text-gray-600">{rec.estimated_timeline}</div>
                  </div>
                </div>
                <div className="flex items-start space-x-2">
                  <DollarSign size={18} className="text-gray-500 mt-1 flex-shrink-0" />
                  <div>
                    <div className="text-sm font-semibold text-gray-700">Cost</div>
                    <div className="text-sm text-gray-600">{rec.estimated_cost}</div>
                  </div>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6 mb-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2 flex items-center space-x-2">
                    <CheckCircle size={18} className="text-green-600" />
                    <span>Advantages</span>
                  </h4>
                  <ul className="space-y-1">
                    {rec.pros.slice(0, 3).map((pro, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-start">
                        <span className="mr-2">•</span>
                        <span>{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2 flex items-center space-x-2">
                    <XCircle size={18} className="text-red-600" />
                    <span>Disadvantages</span>
                  </h4>
                  <ul className="space-y-1">
                    {rec.cons.slice(0, 3).map((con, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-start">
                        <span className="mr-2">•</span>
                        <span>{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <button
                onClick={(e) => {
                  e.stopPropagation()
                  navigate(`/pathway/${rec.pathway_id}`)
                }}
                className="btn-secondary w-full mt-4"
              >
                View Full Details
              </button>
            </div>
          ))}
        </div>

        <div className="mt-8 card bg-blue-50 border-blue-200">
          <h3 className="text-lg font-semibold mb-2">Need More Guidance?</h3>
          <p className="text-gray-700 mb-4">
            Ask our AI advisor questions about these pathways or your specific situation.
          </p>
          <button
            onClick={() => navigate('/chat')}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <span>Ask Questions</span>
            <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  )
}
