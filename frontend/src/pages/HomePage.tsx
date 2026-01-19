import { useNavigate } from 'react-router-dom'
import { ArrowRight, Heart, Compass, BookOpen } from 'lucide-react'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="bg-gradient-to-b from-primary-50 to-white min-h-screen">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-6xl font-display font-bold text-gray-900 mb-6 text-center">
            Camille Goes To America!
          </h1>
          <p className="text-xl text-gray-700 mb-8 leading-relaxed text-center">
            Let's figure out your path to the United States together. Answer a few questions about your background, and I'll help you understand which visa options make sense for your situation.
          </p>
          <div className="text-center">
            <button
              onClick={() => navigate('/assessment')}
              className="btn-primary inline-flex items-center space-x-2 text-lg px-8 py-4 shadow-lg hover:shadow-xl transition-shadow"
            >
              <span>Start Here</span>
              <ArrowRight size={20} />
            </button>
          </div>
        </div>
      </section>

      {/* Simple How It Works */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpen className="text-primary-600" size={28} />
              </div>
              <h3 className="text-lg font-semibold mb-2">Share Your Story</h3>
              <p className="text-gray-600">
                Tell me about your background, education, and goals
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Compass className="text-primary-600" size={28} />
              </div>
              <h3 className="text-lg font-semibold mb-2">Explore Your Options</h3>
              <p className="text-gray-600">
                See which visa pathways fit your situation best
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="text-primary-600" size={28} />
              </div>
              <h3 className="text-lg font-semibold mb-2">Get Personalized Advice</h3>
              <p className="text-gray-600">
                Ask any questions and get answers tailored to you
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Simple Note */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center">
          <p className="text-gray-600 leading-relaxed">
            US immigration can be overwhelming - there are dozens of visa types, each with their own requirements, timelines, and costs. This tool is here to help you make sense of it all and find the path that works for you.
          </p>
          <p className="text-sm text-gray-500 mt-6">
            Note: This provides informational guidance based on current immigration law. For legal advice specific to your case, consult with a licensed immigration attorney.
          </p>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-display font-bold mb-4">Ready to get started?</h2>
          <p className="text-lg text-primary-100 mb-8">
            It takes about 5 minutes
          </p>
          <button
            onClick={() => navigate('/assessment')}
            className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors inline-flex items-center space-x-2 shadow-lg"
          >
            <span>Begin</span>
            <ArrowRight size={20} />
          </button>
        </div>
      </section>
    </div>
  )
}
