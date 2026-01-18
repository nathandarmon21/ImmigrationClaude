import { useState, useRef, useEffect } from 'react'
import { useUserStore } from '../store/userStore'
import { immigrationApi } from '../services/api'
import { Send, Loader } from 'lucide-react'

export default function ChatPage() {
  const { profile, conversationHistory, addMessage } = useUserStore()
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [conversationHistory])

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      role: 'user' as const,
      content: inputMessage,
      timestamp: new Date().toISOString(),
    }

    addMessage(userMessage)
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await immigrationApi.getAdvice(
        profile as any,
        inputMessage,
        conversationHistory
      )

      const assistantMessage = {
        role: 'assistant' as const,
        content: response.response,
        timestamp: new Date().toISOString(),
      }

      addMessage(assistantMessage)
    } catch (error) {
      console.error('Failed to get advice:', error)
      const errorMessage = {
        role: 'assistant' as const,
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      }
      addMessage(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const suggestedQuestions = [
    'What is the difference between H-1B and O-1 visas?',
    'How long does the green card process take?',
    'Can I change employers while on H-1B?',
    'What documents do I need for EB-2 NIW?',
    'How much does the immigration process cost?',
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-5xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Ask Immigration Questions
          </h1>
          <p className="text-gray-600">
            Get expert-level advice from our AI immigration advisor
          </p>
        </div>

        <div className="card h-[600px] flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {conversationHistory.length === 0 ? (
              <div className="text-center py-12">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Start a conversation
                </h3>
                <p className="text-gray-600 mb-6">
                  Ask me anything about US immigration pathways, requirements, or processes.
                </p>
                <div className="space-y-2">
                  <p className="text-sm font-semibold text-gray-700">
                    Try asking:
                  </p>
                  {suggestedQuestions.map((question, idx) => (
                    <button
                      key={idx}
                      onClick={() => setInputMessage(question)}
                      className="block w-full text-left px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <>
                {conversationHistory.map((message, idx) => (
                  <div
                    key={idx}
                    className={`flex ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-3xl px-4 py-3 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 px-4 py-3 rounded-lg">
                      <Loader className="animate-spin text-primary-600" size={20} />
                    </div>
                  </div>
                )}
              </>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex items-end space-x-2">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your question here..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                rows={3}
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send size={20} />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              This AI advisor provides informational guidance only, not legal advice.
              Consult with a licensed immigration attorney for specific legal matters.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
