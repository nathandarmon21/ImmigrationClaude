"""
Pydantic models for API requests and responses.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class UserProfile(BaseModel):
    """User's immigration profile information."""
    purpose: str
    current_status: Optional[str] = None
    education_level: Optional[str] = None
    field_of_expertise: Optional[str] = None
    achievements: List[str] = []
    years_experience: Optional[int] = None
    current_salary: Optional[int] = None
    has_job_offer: bool = False
    employer_will_sponsor: bool = False
    country_of_citizenship: Optional[str] = None
    currently_in_us: bool = False
    additional_info: Dict[str, Any] = {}


class AssessmentResponse(BaseModel):
    """User's response to an assessment question."""
    question_id: str
    answer: Any  # Can be string, list of strings, etc.


class PathwayRecommendation(BaseModel):
    """A recommended immigration pathway with scoring."""
    pathway_id: str
    pathway_name: str
    fit_score: float = Field(..., ge=0, le=100, description="0-100 score indicating fit")
    feasibility: str  # high, medium, low
    reasoning: str
    pros: List[str]
    cons: List[str]
    estimated_timeline: str
    estimated_cost: str
    next_steps: List[str]
    requirements_met: List[str]
    requirements_missing: List[str]


class PathwayComparison(BaseModel):
    """Detailed comparison between multiple pathways."""
    pathways: List[PathwayRecommendation]
    comparison_table: Dict[str, List[str]]
    recommendation_summary: str


class ConversationMessage(BaseModel):
    """A message in the conversation with Claude."""
    role: str  # user or assistant
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class AdvisoryRequest(BaseModel):
    """Request for immigration advice."""
    user_profile: UserProfile
    conversation_history: List[ConversationMessage] = []
    user_message: str


class AdvisoryResponse(BaseModel):
    """Response from immigration advisor."""
    response: str
    follow_up_questions: Optional[List[str]] = None
    recommended_pathways: Optional[List[str]] = None
    requires_more_info: bool = False


class WebAutomationRequest(BaseModel):
    """Request to automate web process."""
    pathway_id: str
    user_profile: UserProfile
    action: str  # e.g., "check_status", "start_application", "gather_forms"


class WebAutomationResponse(BaseModel):
    """Response from web automation."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    next_actions: Optional[List[str]] = None
    forms_needed: Optional[List[str]] = None
