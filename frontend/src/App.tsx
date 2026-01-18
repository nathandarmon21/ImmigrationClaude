import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import HomePage from './pages/HomePage'
import AssessmentPage from './pages/AssessmentPage'
import ResultsPage from './pages/ResultsPage'
import ComparePage from './pages/ComparePage'
import ChatPage from './pages/ChatPage'
import PathwayDetailPage from './pages/PathwayDetailPage'
import Navigation from './components/Navigation'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen flex flex-col">
          <Navigation />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/assessment" element={<AssessmentPage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/compare" element={<ComparePage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/pathway/:pathwayId" element={<PathwayDetailPage />} />
            </Routes>
          </main>
          <footer className="bg-gray-800 text-white py-8 mt-12">
            <div className="container mx-auto px-4 text-center">
              <p className="text-sm text-gray-400">
                This tool provides informational guidance only and does not constitute legal advice.
                For specific legal matters, consult with a licensed immigration attorney.
              </p>
              <p className="mt-4 text-xs text-gray-500">
                © 2025 Immigration Advisory System. Powered by Claude AI.
              </p>
            </div>
          </footer>
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
