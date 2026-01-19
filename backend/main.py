"""
Main FastAPI application for Immigration Advisory System.
"""

print("=" * 60)
print("STARTING IMMIGRATION ADVISORY API")
print("=" * 60)

import sys
import os
import traceback

print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

print("✓ FastAPI core imports successful")

from dotenv import load_dotenv
load_dotenv()
print("✓ Environment variables loaded")

# Import with error handling
IMMIGRATION_PATHWAYS = {}
ASSESSMENT_QUESTIONS = []
pathway_analyzer = None
claude_advisor = None
data_fetcher = None
web_automation = None
immigration_updates = None

try:
    print("Importing schemas...")
    from models.schemas import (
        UserProfile,
        PathwayRecommendation,
        AdvisoryRequest,
        AdvisoryResponse,
        ConversationMessage,
    )
    print("✓ Schemas imported")
except Exception as e:
    print(f"✗ Schemas import failed: {e}")
    traceback.print_exc()

try:
    print("Importing knowledge base...")
    from knowledge.pathways import IMMIGRATION_PATHWAYS, ASSESSMENT_QUESTIONS
    print(f"✓ Knowledge base imported ({len(IMMIGRATION_PATHWAYS)} pathways)")
except Exception as e:
    print(f"✗ Knowledge base import failed: {e}")
    traceback.print_exc()

try:
    print("Importing PathwayAnalyzer...")
    from core.analyzer import PathwayAnalyzer
    print("✓ PathwayAnalyzer imported")
except Exception as e:
    print(f"✗ PathwayAnalyzer import failed: {e}")
    traceback.print_exc()
    PathwayAnalyzer = None

try:
    print("Importing services...")
    from services.claude_advisor import ClaudeAdvisor
    print("✓ ClaudeAdvisor imported")
except Exception as e:
    print(f"✗ ClaudeAdvisor import failed: {e}")
    traceback.print_exc()
    ClaudeAdvisor = None

try:
    from services.data_fetcher import ImmigrationDataFetcher
    print("✓ ImmigrationDataFetcher imported")
except Exception as e:
    print(f"✗ ImmigrationDataFetcher import failed: {e}")
    traceback.print_exc()
    ImmigrationDataFetcher = None

try:
    from services.web_automation import ImmigrationWebAutomation
    print("✓ ImmigrationWebAutomation imported")
except Exception as e:
    print(f"✗ ImmigrationWebAutomation import failed: {e}")
    traceback.print_exc()
    ImmigrationWebAutomation = None

try:
    from services.immigration_updates import ImmigrationUpdatesService
    print("✓ ImmigrationUpdatesService imported")
except Exception as e:
    print(f"✗ ImmigrationUpdatesService import failed: {e}")
    traceback.print_exc()
    ImmigrationUpdatesService = None

# Initialize FastAPI app
print("Initializing FastAPI app...")
app = FastAPI(
    title="Immigration Advisory API",
    description="Intelligent US immigration advisory system powered by Claude AI",
    version="1.0.0",
)
print("✓ FastAPI app created")

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✓ CORS middleware configured")

# Initialize services with error handling
if PathwayAnalyzer:
    try:
        pathway_analyzer = PathwayAnalyzer()
        print("✓ PathwayAnalyzer initialized")
    except Exception as e:
        print(f"✗ PathwayAnalyzer initialization failed: {e}")
        traceback.print_exc()
        pathway_analyzer = None

if ClaudeAdvisor:
    try:
        claude_advisor = ClaudeAdvisor()
        print("✓ ClaudeAdvisor initialized")
    except Exception as e:
        print(f"✗ ClaudeAdvisor initialization failed: {e}")
        traceback.print_exc()
        claude_advisor = None

if ImmigrationDataFetcher:
    try:
        data_fetcher = ImmigrationDataFetcher()
        print("✓ ImmigrationDataFetcher initialized")
    except Exception as e:
        print(f"✗ ImmigrationDataFetcher initialization failed: {e}")
        traceback.print_exc()
        data_fetcher = None

if ImmigrationWebAutomation:
    try:
        web_automation = ImmigrationWebAutomation()
        print("✓ ImmigrationWebAutomation initialized")
    except Exception as e:
        print(f"✗ ImmigrationWebAutomation initialization failed: {e}")
        traceback.print_exc()
        web_automation = None

if ImmigrationUpdatesService:
    try:
        immigration_updates = ImmigrationUpdatesService()
        print("✓ ImmigrationUpdatesService initialized")
    except Exception as e:
        print(f"✗ ImmigrationUpdatesService initialization failed: {e}")
        traceback.print_exc()
        immigration_updates = None

print("=" * 60)
print("STARTUP COMPLETE - API READY")
print("=" * 60)


# Request/Response models
class AnalyzeRequest(BaseModel):
    profile: Dict[str, Any]


class CompareRequest(BaseModel):
    pathway_ids: List[str]
    profile: Dict[str, Any]


class NextStepsRequest(BaseModel):
    pathway_id: str
    profile: Dict[str, Any]


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Immigration Advisory API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/health",
            "/pathways",
            "/analyze",
            "/updates/latest",
            "/advice",
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "pathway_analyzer": pathway_analyzer is not None,
            "claude_advisor": claude_advisor is not None,
            "data_fetcher": data_fetcher is not None,
            "web_automation": web_automation is not None,
            "immigration_updates": immigration_updates is not None,
        },
        "pathways_loaded": len(IMMIGRATION_PATHWAYS) if IMMIGRATION_PATHWAYS else 0
    }


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
    if pathway_analyzer is None:
        raise HTTPException(status_code=503, detail="Pathway analyzer service is not available")

    try:
        from models.schemas import UserProfile
        profile = UserProfile(**request.profile)
        recommendations = pathway_analyzer.analyze_profile(profile)

        return {
            "recommendations": [rec.dict() for rec in recommendations],
            "total_pathways": len(recommendations),
        }
    except Exception as e:
        print(f"Error in analyze_profile: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/compare")
async def compare_pathways(request: CompareRequest) -> Dict[str, Any]:
    """
    Compare multiple immigration pathways.

    Returns detailed comparison and recommendation.
    """
    if pathway_analyzer is None:
        raise HTTPException(status_code=503, detail="Pathway analyzer not available")

    if claude_advisor is None:
        raise HTTPException(status_code=503, detail="Claude advisor not available")

    try:
        from models.schemas import UserProfile
        profile = UserProfile(**request.profile)

        # Get comparison data from analyzer
        comparison_data = pathway_analyzer.compare_pathways(
            request.pathway_ids,
            profile
        )

        # Get AI-generated comparison narrative
        comparison_narrative = claude_advisor.generate_comparison(
            request.pathway_ids,
            profile
        )

        return {
            "comparison_data": comparison_data,
            "narrative": comparison_narrative,
            "pathways_compared": request.pathway_ids,
        }
    except Exception as e:
        print(f"Error in compare_pathways: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@app.post("/advice")
async def get_advice(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get intelligent immigration advice from Claude AI.

    Provides conversational guidance based on user profile and question.
    """
    if claude_advisor is None:
        raise HTTPException(status_code=503, detail="Claude advisor not available")

    if pathway_analyzer is None:
        raise HTTPException(status_code=503, detail="Pathway analyzer not available")

    try:
        from models.schemas import UserProfile
        profile = UserProfile(**request.get("user_profile", {}))

        # Get pathway recommendations for context
        recommendations = pathway_analyzer.analyze_profile(profile)

        # Get advice from Claude
        response_text = claude_advisor.get_advice(
            user_profile=profile,
            user_message=request.get("user_message", ""),
            conversation_history=request.get("conversation_history", []),
            recommended_pathways=recommendations[:3],  # Top 3
        )

        return {
            "response": response_text,
            "requires_more_info": False,
        }
    except Exception as e:
        print(f"Error in get_advice: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Advisory failed: {str(e)}")


@app.post("/next-steps")
async def get_next_steps(request: NextStepsRequest) -> Dict[str, str]:
    """
    Get detailed next steps for a specific immigration pathway.

    Returns actionable step-by-step guidance.
    """
    if claude_advisor is None:
        raise HTTPException(status_code=503, detail="Claude advisor not available")

    try:
        from models.schemas import UserProfile
        profile = UserProfile(**request.profile)

        steps = claude_advisor.get_next_steps(
            pathway_id=request.pathway_id,
            user_profile=profile
        )

        return {
            "pathway_id": request.pathway_id,
            "next_steps": steps,
        }
    except Exception as e:
        print(f"Error in get_next_steps: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get next steps: {str(e)}")


@app.get("/data/processing-times/{form_type}")
async def get_processing_times(form_type: str, service_center: Optional[str] = None):
    """Get current USCIS processing times."""
    if data_fetcher is None:
        raise HTTPException(status_code=503, detail="Data fetcher not available")

    data = await data_fetcher.get_processing_times(form_type, service_center)
    return data


@app.get("/data/visa-bulletin")
async def get_visa_bulletin():
    """Get current State Department Visa Bulletin."""
    if data_fetcher is None:
        raise HTTPException(status_code=503, detail="Data fetcher not available")

    data = await data_fetcher.get_visa_bulletin()
    return data


@app.get("/data/h1b-stats")
async def get_h1b_stats():
    """Get H-1B lottery statistics."""
    if data_fetcher is None:
        raise HTTPException(status_code=503, detail="Data fetcher not available")

    data = await data_fetcher.get_h1b_stats()
    return data


@app.get("/data/filing-fees")
async def get_filing_fees():
    """Get current USCIS filing fees."""
    if data_fetcher is None:
        raise HTTPException(status_code=503, detail="Data fetcher not available")

    data = await data_fetcher.get_filing_fees()
    return data


@app.get("/automation/forms/{pathway_id}")
async def get_required_forms(pathway_id: str):
    """Get required forms for a pathway."""
    if web_automation is None:
        raise HTTPException(status_code=503, detail="Web automation not available")

    forms = await web_automation.find_immigration_forms(pathway_id)
    return forms


@app.post("/automation/document-checklist")
async def get_document_checklist(request: NextStepsRequest):
    """Get personalized document checklist."""
    if web_automation is None:
        raise HTTPException(status_code=503, detail="Web automation not available")

    checklist = await web_automation.prepare_document_checklist(
        request.pathway_id,
        request.profile
    )
    return checklist


@app.get("/automation/find-attorney")
async def find_attorney(location: str, specialty: str = "immigration"):
    """Get information about finding immigration attorneys."""
    if web_automation is None:
        raise HTTPException(status_code=503, detail="Web automation not available")

    results = await web_automation.get_attorney_search_results(location, specialty)
    return results


@app.get("/updates/latest")
async def get_latest_updates(limit: int = 10, pathways: Optional[str] = None):
    """
    Get latest immigration law updates and policy changes.

    Args:
        limit: Maximum number of updates to return (default 10)
        pathways: Optional comma-separated list of pathway IDs to prioritize (e.g., "h1b,o1,eb2_niw")

    Returns recent updates from USCIS, State Department, and Federal Register.
    """
    if immigration_updates is None:
        raise HTTPException(status_code=503, detail="Immigration updates service is not available")

    try:
        # Parse pathway filter if provided
        pathway_filter = None
        if pathways:
            pathway_filter = [p.strip() for p in pathways.split(',')]

        updates = await immigration_updates.get_latest_updates(limit=limit, pathway_filter=pathway_filter)

        # Convert datetime objects to ISO strings for JSON serialization
        serialized_updates = []
        for update in updates:
            serialized_update = update.copy()
            if 'date' in serialized_update and hasattr(serialized_update['date'], 'isoformat'):
                serialized_update['date'] = serialized_update['date'].isoformat()
            serialized_updates.append(serialized_update)

        return {
            "updates": serialized_updates,
            "total": len(serialized_updates),
            "last_updated": serialized_updates[0]['date'] if serialized_updates else None,
            "filtered_by_pathways": pathway_filter
        }
    except Exception as e:
        print(f"Error in get_latest_updates: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch updates: {str(e)}")


@app.get("/updates/details")
async def get_update_details(source_url: str):
    """
    Get full legal text and details for a specific update.

    Args:
        source_url: URL of the update
    """
    if immigration_updates is None:
        raise HTTPException(status_code=503, detail="Immigration updates service not available")

    try:
        details = await immigration_updates.get_update_details(source_url)
        if not details:
            raise HTTPException(status_code=404, detail="Update details not found")
        return details
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_update_details: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch update details: {str(e)}")


@app.get("/updates/search")
async def search_updates(query: str, category: Optional[str] = None):
    """
    Search for immigration updates by keyword.

    Args:
        query: Search query (e.g., "H-1B", "green card")
        category: Optional category filter (policy_update, visa_bulletin, executive_order)
    """
    if immigration_updates is None:
        raise HTTPException(status_code=503, detail="Immigration updates service not available")

    try:
        results = await immigration_updates.search_updates(query, category)
        return {
            "results": results,
            "total": len(results),
            "query": query
        }
    except Exception as e:
        print(f"Error in search_updates: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
