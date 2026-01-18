import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useUserStore } from '../store/userStore'
import { immigrationApi } from '../services/api'
import { Loader } from 'lucide-react'

export default function ComparePage() {
  const navigate = useNavigate()
  const { selectedPathways, profile, recommendations } = useUserStore()
  const [comparisonData, setComparisonData] = useState<any>(null)
  const [narrative, setNarrative] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (selectedPathways.length === 0) {
      navigate('/results')
      return
    }

    const fetchComparison = async () => {
      try {
        const data = await immigrationApi.comparePathways(
          selectedPathways,
          profile as any
        )
        setComparisonData(data.comparison_data)
        setNarrative(data.narrative)
      } catch (error) {
        console.error('Failed to fetch comparison:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchComparison()
  }, [selectedPathways, profile, navigate])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 flex items-center justify-center">
        <Loader className="animate-spin text-primary-600" size={48} />
      </div>
    )
  }

  const selectedRecs = recommendations.filter((r) =>
    selectedPathways.includes(r.pathway_id)
  )

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Pathway Comparison
          </h1>
          <p className="text-lg text-gray-600">
            Detailed comparison of your selected immigration pathways
          </p>
        </div>

        {/* AI-Generated Narrative */}
        {narrative && (
          <div className="card mb-8 bg-blue-50 border-blue-200">
            <h2 className="text-2xl font-bold mb-4 text-gray-900">
              Expert Analysis
            </h2>
            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
              {narrative}
            </div>
          </div>
        )}

        {/* Comparison Table */}
        <div className="card overflow-x-auto">
          <h2 className="text-2xl font-bold mb-6">Quick Comparison</h2>
          <table className="w-full">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left py-4 px-4 font-semibold">Criteria</th>
                {selectedRecs.map((rec) => (
                  <th
                    key={rec.pathway_id}
                    className="text-left py-4 px-4 font-semibold"
                  >
                    {rec.pathway_name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              <tr>
                <td className="py-4 px-4 font-medium">Fit Score</td>
                {selectedRecs.map((rec) => (
                  <td key={rec.pathway_id} className="py-4 px-4">
                    <span className="inline-block px-3 py-1 bg-primary-100 text-primary-700 rounded-full font-semibold">
                      {rec.fit_score.toFixed(0)}%
                    </span>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-4 px-4 font-medium">Feasibility</td>
                {selectedRecs.map((rec) => (
                  <td key={rec.pathway_id} className="py-4 px-4 capitalize">
                    {rec.feasibility}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-4 px-4 font-medium">Timeline</td>
                {selectedRecs.map((rec) => (
                  <td key={rec.pathway_id} className="py-4 px-4">
                    {rec.estimated_timeline}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="py-4 px-4 font-medium">Estimated Cost</td>
                {selectedRecs.map((rec) => (
                  <td key={rec.pathway_id} className="py-4 px-4">
                    {rec.estimated_cost}
                  </td>
                ))}
              </tr>
              {comparisonData?.employer_sponsorship && (
                <tr>
                  <td className="py-4 px-4 font-medium">Employer Sponsorship</td>
                  {selectedRecs.map((rec) => (
                    <td key={rec.pathway_id} className="py-4 px-4">
                      {comparisonData.employer_sponsorship[rec.pathway_name]}
                    </td>
                  ))}
                </tr>
              )}
              {comparisonData?.can_self_petition && (
                <tr>
                  <td className="py-4 px-4 font-medium">Can Self-Petition</td>
                  {selectedRecs.map((rec) => (
                    <td key={rec.pathway_id} className="py-4 px-4">
                      {comparisonData.can_self_petition[rec.pathway_name]}
                    </td>
                  ))}
                </tr>
              )}
              {comparisonData?.leads_to_green_card && (
                <tr>
                  <td className="py-4 px-4 font-medium">Leads to Green Card</td>
                  {selectedRecs.map((rec) => (
                    <td key={rec.pathway_id} className="py-4 px-4">
                      {comparisonData.leads_to_green_card[rec.pathway_name]}
                    </td>
                  ))}
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Detailed Cards */}
        <div className="mt-8 grid md:grid-cols-2 gap-6">
          {selectedRecs.map((rec) => (
            <div key={rec.pathway_id} className="card">
              <h3 className="text-xl font-bold mb-4">{rec.pathway_name}</h3>

              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">
                    Requirements Met
                  </h4>
                  <ul className="space-y-1">
                    {rec.requirements_met.map((req, idx) => (
                      <li key={idx} className="text-sm text-green-600 flex items-start">
                        <span className="mr-2">✓</span>
                        <span>{req}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {rec.requirements_missing.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">
                      Requirements Missing
                    </h4>
                    <ul className="space-y-1">
                      {rec.requirements_missing.map((req, idx) => (
                        <li key={idx} className="text-sm text-red-600 flex items-start">
                          <span className="mr-2">✗</span>
                          <span>{req}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <button
                  onClick={() => navigate(`/pathway/${rec.pathway_id}`)}
                  className="btn-secondary w-full mt-4"
                >
                  View Details & Next Steps
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 text-center">
          <button onClick={() => navigate('/results')} className="btn-secondary">
            Back to Results
          </button>
        </div>
      </div>
    </div>
  )
}
