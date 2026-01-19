export interface UserProfile {
  purpose: string
  current_status?: string
  education_level?: string
  field_of_expertise?: string
  achievements: string[]
  years_experience?: number
  current_salary?: number
  has_job_offer: boolean
  employer_will_sponsor: boolean
  country_of_citizenship?: string
  currently_in_us: boolean
  current_location?: string
  immigration_story?: string
  additional_info: Record<string, any>
}

export interface PathwayRecommendation {
  pathway_id: string
  pathway_name: string
  fit_score: number
  feasibility: 'high' | 'medium' | 'low'
  reasoning: string
  pros: string[]
  cons: string[]
  estimated_timeline: string
  estimated_cost: string
  next_steps: string[]
  requirements_met: string[]
  requirements_missing: string[]
}

export interface ConversationMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface PathwayInfo {
  id: string
  name: string
  category: string
  short_description: string
  detailed_description: string
  requirements: Requirement[]
  advantages: string[]
  disadvantages: string[]
  typical_timeline: string
  cost_range: string
  success_factors: string[]
  common_denials: string[]
  next_steps: string[]
  official_links: Array<{ title: string; url: string }>
}

export interface Requirement {
  name: string
  description: string
  is_mandatory: boolean
  alternatives?: string[]
}
