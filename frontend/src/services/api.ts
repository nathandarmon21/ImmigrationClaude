import axios from 'axios'
import type { UserProfile, PathwayRecommendation, ConversationMessage, PathwayInfo } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const immigrationApi = {
  // Get all pathways
  getPathways: async (): Promise<PathwayInfo[]> => {
    const response = await api.get('/pathways')
    return response.data.pathways
  },

  // Get pathway details
  getPathwayDetails: async (pathwayId: string): Promise<PathwayInfo> => {
    const response = await api.get(`/pathways/${pathwayId}`)
    return response.data.pathway
  },

  // Analyze profile and get recommendations
  analyzeProfile: async (profile: UserProfile): Promise<PathwayRecommendation[]> => {
    const response = await api.post('/analyze', { profile })
    return response.data.recommendations
  },

  // Compare pathways
  comparePathways: async (pathwayIds: string[], profile: UserProfile) => {
    const response = await api.post('/compare', { pathway_ids: pathwayIds, profile })
    return response.data
  },

  // Get advice from Claude
  getAdvice: async (
    userProfile: UserProfile,
    userMessage: string,
    conversationHistory: ConversationMessage[] = []
  ) => {
    const response = await api.post('/advice', {
      user_profile: userProfile,
      user_message: userMessage,
      conversation_history: conversationHistory,
    })
    return response.data
  },

  // Get next steps for a pathway
  getNextSteps: async (pathwayId: string, profile: UserProfile) => {
    const response = await api.post('/next-steps', {
      pathway_id: pathwayId,
      profile,
    })
    return response.data.next_steps
  },

  // Get processing times
  getProcessingTimes: async (formType: string, serviceCenter?: string) => {
    const response = await api.get(`/data/processing-times/${formType}`, {
      params: { service_center: serviceCenter },
    })
    return response.data
  },

  // Get visa bulletin
  getVisaBulletin: async () => {
    const response = await api.get('/data/visa-bulletin')
    return response.data
  },

  // Get H-1B stats
  getH1BStats: async () => {
    const response = await api.get('/data/h1b-stats')
    return response.data
  },

  // Get filing fees
  getFilingFees: async () => {
    const response = await api.get('/data/filing-fees')
    return response.data
  },

  // Get required forms
  getRequiredForms: async (pathwayId: string) => {
    const response = await api.get(`/automation/forms/${pathwayId}`)
    return response.data
  },

  // Get document checklist
  getDocumentChecklist: async (pathwayId: string, profile: UserProfile) => {
    const response = await api.post('/automation/document-checklist', {
      pathway_id: pathwayId,
      profile,
    })
    return response.data
  },

  // Find attorney
  findAttorney: async (location: string, specialty: string = 'immigration') => {
    const response = await api.get('/automation/find-attorney', {
      params: { location, specialty },
    })
    return response.data
  },
}

export default api
