import { useNavigate } from 'react-router-dom'
import { ArrowRight, CheckCircle, Users, Clock, DollarSign } from 'lucide-react'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="bg-gradient-to-b from-primary-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Camille Goes To America!
            <span className="block text-primary-600 mt-2">Your Personalized Immigration Guide</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 leading-relaxed">
            Get personalized immigration guidance powered by AI. Understand your options,
            compare pathways, and take the next step with confidence.
          </p>
          <button
            onClick={() => navigate('/assessment')}
            className="btn-primary inline-flex items-center space-x-2 text-lg px-8 py-4"
          >
            <span>Start Your Assessment</span>
            <ArrowRight size={20} />
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="text-primary-600" size={28} />
              </div>
              <h3 className="text-xl font-semibold mb-3">1. Take Assessment</h3>
              <p className="text-gray-600">
                Answer questions about your situation, qualifications, and goals
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <GitCompare className="text-primary-600" size={28} />
              </div>
              <h3 className="text-xl font-semibold mb-3">2. Compare Options</h3>
              <p className="text-gray-600">
                Review personalized pathway recommendations with detailed comparisons
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageSquare className="text-primary-600" size={28} />
              </div>
              <h3 className="text-xl font-semibold mb-3">3. Get Guidance</h3>
              <p className="text-gray-600">
                Ask questions and receive expert-level advice from AI
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Why Use Our Platform</h2>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <div className="card flex items-start space-x-4">
              <CheckCircle className="text-green-500 flex-shrink-0" size={24} />
              <div>
                <h3 className="font-semibold text-lg mb-2">Comprehensive Knowledge</h3>
                <p className="text-gray-600">
                  Up-to-date information on all major US immigration pathways
                </p>
              </div>
            </div>

            <div className="card flex items-start space-x-4">
              <Users className="text-blue-500 flex-shrink-0" size={24} />
              <div>
                <h3 className="font-semibold text-lg mb-2">Personalized Recommendations</h3>
                <p className="text-gray-600">
                  Tailored advice based on your unique situation and qualifications
                </p>
              </div>
            </div>

            <div className="card flex items-start space-x-4">
              <Clock className="text-purple-500 flex-shrink-0" size={24} />
              <div>
                <h3 className="font-semibold text-lg mb-2">Save Time</h3>
                <p className="text-gray-600">
                  Get clear answers instantly instead of spending hours researching
                </p>
              </div>
            </div>

            <div className="card flex items-start space-x-4">
              <DollarSign className="text-green-500 flex-shrink-0" size={24} />
              <div>
                <h3 className="font-semibold text-lg mb-2">Make Informed Decisions</h3>
                <p className="text-gray-600">
                  Understand costs, timelines, and success factors before proceeding
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Your Journey?</h2>
          <p className="text-xl text-primary-100 mb-8">
            Take the first step towards understanding your immigration options
          </p>
          <button
            onClick={() => navigate('/assessment')}
            className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors inline-flex items-center space-x-2"
          >
            <span>Begin Assessment</span>
            <ArrowRight size={20} />
          </button>
        </div>
      </section>
    </div>
  )
}

function FileText(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" x2="8" y1="13" y2="13" />
      <line x1="16" x2="8" y1="17" y2="17" />
      <line x1="10" x2="8" y1="9" y2="9" />
    </svg>
  )
}

function GitCompare(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="18" cy="18" r="3" />
      <circle cx="6" cy="6" r="3" />
      <path d="M13 6h3a2 2 0 0 1 2 2v7" />
      <path d="M11 18H8a2 2 0 0 1-2-2V9" />
    </svg>
  )
}

function MessageSquare(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  )
}
