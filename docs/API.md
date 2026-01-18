# Immigration Advisory API Documentation

Base URL: `http://localhost:8000` (development)

## Table of Contents

1. [Health & Info](#health--info)
2. [Pathways](#pathways)
3. [Assessment](#assessment)
4. [Analysis](#analysis)
5. [Advisory](#advisory)
6. [Data](#data)
7. [Automation](#automation)

## Health & Info

### GET /
Health check endpoint

**Response:**
```json
{
  "message": "Immigration Advisory API",
  "version": "1.0.0",
  "status": "running"
}
```

### GET /health
Health status

**Response:**
```json
{
  "status": "healthy"
}
```

## Pathways

### GET /pathways
Get all available immigration pathways

**Response:**
```json
{
  "pathways": [
    {
      "id": "h1b",
      "name": "H-1B Specialty Occupation Visa",
      "category": "work",
      "short_description": "Temporary work visa for specialty occupations..."
    }
  ]
}
```

### GET /pathways/{pathway_id}
Get detailed information about a specific pathway

**Parameters:**
- `pathway_id` (path) - Pathway identifier (e.g., "h1b", "o1", "eb1a")

**Response:**
```json
{
  "pathway": {
    "id": "h1b",
    "name": "H-1B Specialty Occupation Visa",
    "category": "work",
    "detailed_description": "...",
    "requirements": [...],
    "advantages": [...],
    "disadvantages": [...],
    "typical_timeline": "6-8 months",
    "cost_range": "$5,000-$10,000",
    "success_factors": [...],
    "common_denials": [...],
    "next_steps": [...],
    "official_links": [...]
  }
}
```

## Assessment

### GET /assessment/questions
Get assessment questionnaire

**Response:**
```json
{
  "questions": [
    {
      "id": "purpose",
      "question": "What is your primary purpose...",
      "type": "single_choice",
      "options": [...]
    }
  ]
}
```

## Analysis

### POST /analyze
Analyze user profile and recommend immigration pathways

**Request Body:**
```json
{
  "profile": {
    "purpose": "work",
    "education_level": "masters",
    "field_of_expertise": "technology",
    "achievements": ["publications", "awards"],
    "years_experience": 5,
    "has_job_offer": true,
    "employer_will_sponsor": true,
    "currently_in_us": false
  }
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "pathway_id": "h1b",
      "pathway_name": "H-1B Specialty Occupation Visa",
      "fit_score": 85.0,
      "feasibility": "high",
      "reasoning": "Aligns with work visa purpose; Advanced degree matches...",
      "pros": [...],
      "cons": [...],
      "estimated_timeline": "6-8 months",
      "estimated_cost": "$5,000-$10,000",
      "next_steps": [...],
      "requirements_met": ["Job Offer", "Bachelor's Degree"],
      "requirements_missing": []
    }
  ],
  "total_pathways": 3
}
```

### POST /compare
Compare multiple immigration pathways

**Request Body:**
```json
{
  "pathway_ids": ["h1b", "o1", "eb2_niw"],
  "profile": { ... }
}
```

**Response:**
```json
{
  "comparison_data": {
    "timeline": {
      "H-1B": "6-8 months",
      "O-1": "2-3 months"
    },
    "cost": { ... },
    "employer_sponsorship": { ... },
    "can_self_petition": { ... }
  },
  "narrative": "AI-generated detailed comparison...",
  "pathways_compared": ["h1b", "o1", "eb2_niw"]
}
```

## Advisory

### POST /advice
Get intelligent immigration advice from Claude AI

**Request Body:**
```json
{
  "user_profile": { ... },
  "user_message": "What is the difference between H-1B and O-1?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous question...",
      "timestamp": "2025-01-18T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Previous response...",
      "timestamp": "2025-01-18T12:00:05Z"
    }
  ]
}
```

**Response:**
```json
{
  "response": "The H-1B and O-1 are both work visas but differ significantly...",
  "requires_more_info": false
}
```

### POST /next-steps
Get detailed next steps for a specific immigration pathway

**Request Body:**
```json
{
  "pathway_id": "h1b",
  "profile": { ... }
}
```

**Response:**
```json
{
  "pathway_id": "h1b",
  "next_steps": "Detailed action plan with specific steps..."
}
```

## Data

### GET /data/processing-times/{form_type}
Get current USCIS processing times

**Parameters:**
- `form_type` (path) - Form type (e.g., "I-129", "I-140", "I-485")
- `service_center` (query, optional) - Specific service center

**Response:**
```json
{
  "form_type": "I-129",
  "service_center": "All Centers",
  "last_updated": "2025-01-18T12:00:00Z",
  "estimated_range": "Data fetched from USCIS",
  "source_url": "https://egov.uscis.gov/processing-times/"
}
```

### GET /data/visa-bulletin
Get current State Department Visa Bulletin

**Response:**
```json
{
  "month": "January 2025",
  "last_updated": "2025-01-18T12:00:00Z",
  "employment_based": {
    "EB-1": "Current for most countries",
    "EB-2": "Check bulletin for current priority dates"
  },
  "source_url": "https://travel.state.gov/..."
}
```

### GET /data/h1b-stats
Get H-1B lottery statistics and cap information

**Response:**
```json
{
  "fiscal_year": 2025,
  "regular_cap": 65000,
  "masters_cap": 20000,
  "total_cap": 85000,
  "registration_period": "Typically March",
  "estimated_selection_rate": "~21%"
}
```

### GET /data/filing-fees
Get current USCIS filing fees

**Response:**
```json
{
  "fees": {
    "I-129 (H-1B, L-1, O-1)": "$460",
    "I-140 (Employment Green Card)": "$700",
    "Premium Processing": "$2,500"
  },
  "source_url": "https://www.uscis.gov/forms/filing-fees"
}
```

## Automation

### GET /automation/forms/{pathway_id}
Get required forms for a pathway

**Parameters:**
- `pathway_id` (path) - Pathway identifier

**Response:**
```json
{
  "pathway_id": "h1b",
  "forms": [
    {
      "form": "I-129",
      "name": "Petition for Nonimmigrant Worker",
      "url": "https://www.uscis.gov/i-129"
    }
  ]
}
```

### POST /automation/document-checklist
Get personalized document checklist

**Request Body:**
```json
{
  "pathway_id": "h1b",
  "profile": { ... }
}
```

**Response:**
```json
{
  "pathway_id": "h1b",
  "documents_required": [
    "Valid passport",
    "Educational credentials",
    "Job offer letter"
  ],
  "next_steps": [...],
  "important_notes": [...]
}
```

### GET /automation/find-attorney
Get information about finding immigration attorneys

**Parameters:**
- `location` (query) - City/state for attorney search
- `specialty` (query, optional) - Type of immigration case (default: "immigration")

**Response:**
```json
{
  "location": "San Francisco",
  "specialty": "immigration",
  "resources": [
    {
      "name": "American Immigration Lawyers Association (AILA)",
      "url": "https://www.ailalawyer.com"
    }
  ],
  "tips": [...]
}
```

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Successful request
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

## Rate Limiting

Currently no rate limiting in development. Production deployment should implement rate limiting.

## Authentication

Currently no authentication required. Production deployment should implement API key or OAuth.

## Interactive Documentation

FastAPI provides interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Examples

### Complete User Flow

1. **Get pathways:**
```bash
curl http://localhost:8000/pathways
```

2. **Analyze profile:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "purpose": "work",
      "education_level": "masters",
      "field_of_expertise": "technology",
      "achievements": ["publications"],
      "has_job_offer": true,
      "employer_will_sponsor": true
    }
  }'
```

3. **Get advice:**
```bash
curl -X POST http://localhost:8000/advice \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": { ... },
    "user_message": "Should I apply for H-1B or O-1?",
    "conversation_history": []
  }'
```

## Support

For API issues or questions:
- Check interactive docs at `/docs`
- Review this documentation
- Open an issue on GitHub
