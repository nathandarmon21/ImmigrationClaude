"""
Main FastAPI application for Immigration Advisory System.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

from models.schemas import (
    UserProfile,
    PathwayRecommendation,
    AdvisoryRequest,
    AdvisoryResponse,
    ConversationMessage,
)
from core.analyzer import PathwayAnalyzer
from services.claude_advisor import ClaudeAdvisor
from services.data_fetcher import ImmigrationDataFetcher
from services.web_automation import ImmigrationWebAutomation
from knowledge.pathways import IMMIGRATION_PATHWAYS, ASSESSMENT_QUESTIONS

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Immigration Advisory API",
    description="Intelligent US immigration advisory system powered by Claude AI",
    version="1.0.0",
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pathway_analyzer = PathwayAnalyzer()
claude_advisor = ClaudeAdvisor()
data_fetcher = ImmigrationDataFetcher()
web_automation = ImmigrationWebAutomation()


# Request/Response models
class AnalyzeRequest(BaseModel):
    profile: UserProfile


class CompareRequest(BaseModel):
    pathway_ids: List[str]
    profile: UserProfile


class NextStepsRequest(BaseModel):
    pathway_id: str
    profile: UserProfile


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Immigration Advisory API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/pathways")
async def get_pathways():
    """Get all available immigration pathways."""
    return {
        "pathways": [
            {
                "id": pathway.id,
                "name": pathway.name,
                "category": pathway.category,
                "short_description": pathway.short_description,
            }
            for pathway in IMMIGRATION_PATHWAYS.values()
        ]
    }


@app.get("/pathways/{pathway_id}")
async def get_pathway_details(pathway_id: str):
    """Get detailed information about a specific pathway."""
    if pathway_id not in IMMIGRATION_PATHWAYS:
        raise HTTPException(status_code=404, detail="Pathway not found")

    pathway = IMMIGRATION_PATHWAYS[pathway_id]
    return {
        "pathway": pathway.dict()
    }


@app.get("/assessment/questions")
async def get_assessment_questions():
    """Get assessment questionnaire."""
    return {
        "questions": ASSESSMENT_QUESTIONS
    }


@app.post("/analyze")
async def analyze_profile(request: AnalyzeRequest) -> Dict[str, Any]:
    """
    Analyze user profile and recommend immigration pathways.

    Returns ranked list of pathway recommendations.
    """
    try:
        recommendations = pathway_analyzer.analyze_profile(request.profile)

        return {
            "recommendations": [rec.dict() for rec in recommendations],
            "total_pathways": len(recommendations),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/compare")
async def compare_pathways(request: CompareRequest) -> Dict[str, Any]:
    """
    Compare multiple immigration pathways.

    Returns detailed comparison and recommendation.
    """
    try:
        # Get comparison data from analyzer
        comparison_data = pathway_analyzer.compare_pathways(
            request.pathway_ids,
            request.profile
        )

        # Get AI-generated comparison narrative
        comparison_narrative = claude_advisor.generate_comparison(
            request.pathway_ids,
            request.profile
        )

        return {
            "comparison_data": comparison_data,
            "narrative": comparison_narrative,
            "pathways_compared": request.pathway_ids,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@app.post("/advice")
async def get_advice(request: AdvisoryRequest) -> AdvisoryResponse:
    """
    Get intelligent immigration advice from Claude AI.

    Provides conversational guidance based on user profile and question.
    """
    try:
        # Get pathway recommendations for context
        recommendations = pathway_analyzer.analyze_profile(request.user_profile)

        # Get advice from Claude
        response_text = claude_advisor.get_advice(
            user_profile=request.user_profile,
            user_message=request.user_message,
            conversation_history=request.conversation_history,
            recommended_pathways=recommendations[:3],  # Top 3
        )

        return AdvisoryResponse(
            response=response_text,
            requires_more_info=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advisory failed: {str(e)}")


@app.post("/next-steps")
async def get_next_steps(request: NextStepsRequest) -> Dict[str, str]:
    """
    Get detailed next steps for a specific immigration pathway.

    Returns actionable step-by-step guidance.
    """
    try:
        steps = claude_advisor.get_next_steps(
            pathway_id=request.pathway_id,
            user_profile=request.profile
        )

        return {
            "pathway_id": request.pathway_id,
            "next_steps": steps,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get next steps: {str(e)}")


@app.get("/data/processing-times/{form_type}")
async def get_processing_times(form_type: str, service_center: Optional[str] = None):
    """Get current USCIS processing times."""
    data = await data_fetcher.get_processing_times(form_type, service_center)
    return data


@app.get("/data/visa-bulletin")
async def get_visa_bulletin():
    """Get current State Department Visa Bulletin."""
    data = await data_fetcher.get_visa_bulletin()
    return data


@app.get("/data/h1b-stats")
async def get_h1b_stats():
    """Get H-1B lottery statistics."""
    data = await data_fetcher.get_h1b_stats()
    return data


@app.get("/data/filing-fees")
async def get_filing_fees():
    """Get current USCIS filing fees."""
    data = await data_fetcher.get_filing_fees()
    return data


@app.get("/automation/forms/{pathway_id}")
async def get_required_forms(pathway_id: str):
    """Get required forms for a pathway."""
    forms = await web_automation.find_immigration_forms(pathway_id)
    return forms


@app.post("/automation/document-checklist")
async def get_document_checklist(request: NextStepsRequest):
    """Get personalized document checklist."""
    checklist = await web_automation.prepare_document_checklist(
        request.pathway_id,
        request.profile.dict()
    )
    return checklist


@app.get("/automation/find-attorney")
async def find_attorney(location: str, specialty: str = "immigration"):
    """Get information about finding immigration attorneys."""
    results = await web_automation.get_attorney_search_results(location, specialty)
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
