import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useUserStore } from '../store/userStore'
import { immigrationApi } from '../services/api'
import { ArrowRight, ArrowLeft } from 'lucide-react'

export default function AssessmentPage() {
  const navigate = useNavigate()
  const { profile, updateProfile, setRecommendations, resetProfile } = useUserStore()
  const [currentStep, setCurrentStep] = useState(0)
  const [loading, setLoading] = useState(false)

  // Reset profile when component mounts to start fresh each time
  useEffect(() => {
    resetProfile()
  }, [])

  const questions = [
    {
      id: 'purpose',
      question: 'What is your primary purpose for coming to or staying in the United States?',
      type: 'radio',
      options: [
        { value: 'work', label: 'Work/Employment' },
        { value: 'permanent', label: 'Permanent residence (green card)' },
        { value: 'study', label: 'Education/Study' },
        { value: 'business', label: 'Start/run a business' },
        { value: 'family', label: 'Family reunification' },
      ],
    },
    {
      id: 'country_of_citizenship',
      question: 'What is your country of citizenship?',
      description: 'This is important because different countries have different visa eligibility, processing times, and potential backlogs.',
      type: 'text',
      placeholder: 'e.g., France, Brazil, India, etc.',
    },
    {
      id: 'education_level',
      question: 'What is your highest level of education?',
      type: 'radio',
      options: [
        { value: 'phd', label: 'PhD/Doctorate' },
        { value: 'masters', label: "Master's degree" },
        { value: 'bachelors', label: "Bachelor's degree" },
        { value: 'some_college', label: 'Some college' },
        { value: 'high_school', label: 'High school' },
      ],
    },
    {
      id: 'field_of_expertise',
      question: 'What is your field of work/expertise?',
      type: 'radio',
      options: [
        { value: 'technology', label: 'Technology/Software' },
        { value: 'engineering', label: 'Engineering' },
        { value: 'science', label: 'Sciences/Research' },
        { value: 'business', label: 'Business/Finance' },
        { value: 'healthcare', label: 'Healthcare/Medicine' },
        { value: 'arts', label: 'Arts/Entertainment' },
        { value: 'education', label: 'Education' },
        { value: 'other', label: 'Other' },
      ],
    },
    {
      id: 'achievements',
      question: 'Do you have any of the following achievements? (Select all that apply)',
      type: 'checkbox',
      options: [
        { value: 'awards', label: 'Major awards or prizes in your field' },
        { value: 'publications', label: 'Published research or articles' },
        { value: 'media', label: 'Media coverage about your work' },
        { value: 'high_salary', label: 'High salary (top 10% in field)' },
        { value: 'leadership', label: 'Leadership in distinguished organizations' },
        { value: 'none', label: 'None of the above' },
      ],
    },
    {
      id: 'employment',
      question: 'What is your employment situation?',
      type: 'select',
      subQuestions: [
        {
          id: 'has_job_offer',
          question: 'Do you have a job offer from a US employer?',
          type: 'radio',
          options: [
            { value: 'yes', label: 'Yes' },
            { value: 'no', label: 'No' },
          ],
        },
        {
          id: 'employer_will_sponsor',
          question: 'Is your employer willing to sponsor your visa?',
          type: 'radio',
          options: [
            { value: 'yes', label: 'Yes' },
            { value: 'no', label: 'No' },
            { value: 'unsure', label: 'Not sure' },
          ],
          showIf: (answers: any) => answers.has_job_offer === 'yes',
        },
      ],
    },
    {
      id: 'experience',
      question: 'How many years of professional experience do you have?',
      type: 'number',
    },
    {
      id: 'current_location',
      question: 'Where are you currently located?',
      type: 'radio',
      options: [
        { value: 'outside_us', label: 'Outside the United States' },
        { value: 'us_visitor', label: 'In the US (visitor/tourist)' },
        { value: 'us_student', label: 'In the US (F-1 student)' },
        { value: 'us_worker', label: 'In the US (work visa)' },
        { value: 'us_other', label: 'In the US (other status)' },
      ],
    },
    {
      id: 'immigration_story',
      question: 'Tell us about your immigration goals and situation',
      description: 'Please share any relevant details about your background, why you want to come to/stay in the US, any special circumstances, family ties, previous visa applications, timeline constraints, or anything else that would help us give you the best personalized advice.',
      type: 'textarea',
      placeholder: 'For example: I completed my Master\'s in Computer Science and have been working at a tech company for 3 years. My company is willing to sponsor me, but I\'m not sure whether to pursue H-1B or explore O-1 options since I have some publications...',
    },
  ]

  const handleAnswer = (questionId: string, value: any) => {
    if (questionId === 'achievements') {
      const currentAchievements = profile.achievements || []
      const updatedAchievements = currentAchievements.includes(value)
        ? currentAchievements.filter((a) => a !== value)
        : [...currentAchievements, value]
      updateProfile({ achievements: updatedAchievements })
    } else if (questionId === 'has_job_offer') {
      updateProfile({ has_job_offer: value === 'yes' })
    } else if (questionId === 'employer_will_sponsor') {
      updateProfile({ employer_will_sponsor: value === 'yes' })
    } else if (questionId === 'experience') {
      updateProfile({ years_experience: parseInt(value) || 0 })
    } else {
      updateProfile({ [questionId]: value })
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      console.log('Submitting profile:', profile)
      console.log('API Base URL:', import.meta.env.VITE_API_URL)
      const recommendations = await immigrationApi.analyzeProfile(profile as any)
      console.log('Recommendations received:', recommendations)
      setRecommendations(recommendations)
      navigate('/results')
    } catch (error: any) {
      console.error('Failed to analyze profile:', error)
      console.error('Error response:', error.response?.data)
      console.error('Error status:', error.response?.status)
      const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
      alert(`Failed to analyze your profile: ${errorMessage}\n\nCheck browser console for details.`)
    } finally {
      setLoading(false)
    }
  }

  const currentQuestion = questions[currentStep]
  const isLastStep = currentStep === questions.length - 1

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-3xl">
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-3xl font-bold text-gray-900">Immigration Assessment</h1>
            <span className="text-sm text-gray-500">
              Step {currentStep + 1} of {questions.length}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-6">{currentQuestion.question}</h2>

          {currentQuestion.type === 'radio' && (
            <div className="space-y-3">
              {currentQuestion.options?.map((option) => (
                <label
                  key={option.value}
                  className="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-primary-300 transition-colors"
                >
                  <input
                    type="radio"
                    name={currentQuestion.id}
                    value={option.value}
                    checked={(profile as any)[currentQuestion.id] === option.value}
                    onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
                    className="mr-3 w-5 h-5 text-primary-600"
                  />
                  <span className="text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.type === 'checkbox' && (
            <div className="space-y-3">
              {currentQuestion.options?.map((option) => (
                <label
                  key={option.value}
                  className="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-primary-300 transition-colors"
                >
                  <input
                    type="checkbox"
                    value={option.value}
                    checked={profile.achievements?.includes(option.value)}
                    onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
                    className="mr-3 w-5 h-5 text-primary-600 rounded"
                  />
                  <span className="text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.type === 'number' && (
            <input
              type="number"
              value={(profile as any).years_experience || ''}
              onChange={(e) => handleAnswer('experience', e.target.value)}
              className="input-field"
              placeholder="Enter number of years"
            />
          )}

          {currentQuestion.type === 'text' && (
            <div>
              {currentQuestion.description && (
                <p className="text-gray-600 mb-4 text-sm">{currentQuestion.description}</p>
              )}
              <input
                type="text"
                value={(profile as any)[currentQuestion.id] || ''}
                onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
                className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-primary-300 focus:outline-none"
                placeholder={currentQuestion.placeholder}
              />
            </div>
          )}

          {currentQuestion.type === 'select' && (
            <div className="space-y-6">
              {currentQuestion.subQuestions?.map((subQ) => {
                if (subQ.showIf && !subQ.showIf(profile)) return null

                return (
                  <div key={subQ.id}>
                    <h3 className="font-medium mb-3">{subQ.question}</h3>
                    <div className="space-y-2">
                      {subQ.options?.map((option) => (
                        <label
                          key={option.value}
                          className="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:border-primary-300"
                        >
                          <input
                            type="radio"
                            name={subQ.id}
                            value={option.value}
                            onChange={(e) => handleAnswer(subQ.id, e.target.value)}
                            className="mr-3 text-primary-600"
                          />
                          <span>{option.label}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          )}

          {currentQuestion.type === 'textarea' && (
            <div>
              {currentQuestion.description && (
                <p className="text-gray-600 mb-4 text-sm">{currentQuestion.description}</p>
              )}
              <textarea
                value={(profile as any)[currentQuestion.id] || ''}
                onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
                className="w-full min-h-[200px] p-4 border-2 border-gray-200 rounded-lg focus:border-primary-300 focus:outline-none resize-y"
                placeholder={currentQuestion.placeholder}
                rows={8}
              />
              <p className="text-sm text-gray-500 mt-2">
                {((profile as any)[currentQuestion.id] || '').length} characters
              </p>
            </div>
          )}

          <div className="flex justify-between mt-8">
            <button
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
              className="btn-secondary inline-flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft size={18} />
              <span>Previous</span>
            </button>

            {!isLastStep ? (
              <button
                onClick={() => setCurrentStep(currentStep + 1)}
                className="btn-primary inline-flex items-center space-x-2"
              >
                <span>Next</span>
                <ArrowRight size={18} />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="btn-primary inline-flex items-center space-x-2"
              >
                <span>{loading ? 'Analyzing...' : 'Get Recommendations'}</span>
                <ArrowRight size={18} />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
