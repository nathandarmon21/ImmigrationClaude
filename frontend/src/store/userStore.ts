import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { UserProfile, PathwayRecommendation, ConversationMessage } from '../types'

interface UserStore {
  profile: Partial<UserProfile>
  recommendations: PathwayRecommendation[]
  conversationHistory: ConversationMessage[]
  selectedPathways: string[]

  updateProfile: (updates: Partial<UserProfile>) => void
  setRecommendations: (recommendations: PathwayRecommendation[]) => void
  addMessage: (message: ConversationMessage) => void
  clearConversation: () => void
  togglePathwaySelection: (pathwayId: string) => void
  clearSelectedPathways: () => void
  resetProfile: () => void
}

const defaultProfile: Partial<UserProfile> = {
  purpose: '',
  achievements: [],
  has_job_offer: false,
  employer_will_sponsor: false,
  currently_in_us: false,
  additional_info: {},
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      profile: defaultProfile,
      recommendations: [],
      conversationHistory: [],
      selectedPathways: [],

      updateProfile: (updates) =>
        set((state) => ({
          profile: { ...state.profile, ...updates },
        })),

      setRecommendations: (recommendations) =>
        set({ recommendations }),

      addMessage: (message) =>
        set((state) => ({
          conversationHistory: [...state.conversationHistory, message],
        })),

      clearConversation: () =>
        set({ conversationHistory: [] }),

      togglePathwaySelection: (pathwayId) =>
        set((state) => ({
          selectedPathways: state.selectedPathways.includes(pathwayId)
            ? state.selectedPathways.filter((id) => id !== pathwayId)
            : [...state.selectedPathways, pathwayId],
        })),

      clearSelectedPathways: () =>
        set({ selectedPathways: [] }),

      resetProfile: () =>
        set({
          profile: defaultProfile,
          recommendations: [],
          conversationHistory: [],
          selectedPathways: [],
        }),
    }),
    {
      name: 'immigration-user-store',
    }
  )
)
