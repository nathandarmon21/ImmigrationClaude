# Immigration Advisory System

An intelligent US immigration advisory interface powered by Claude AI that provides personalized immigration pathway recommendations and guidance.

## Features

- **Interactive Assessment**: Dynamic questionnaire that adapts to user's situation
- **Comprehensive Knowledge Base**: Up-to-date information on all major US immigration pathways
- **Intelligent Advisory**: Powered by Claude AI for personalized, attorney-level guidance
- **Pathway Comparison**: Compare multiple immigration options with feasibility analysis
- **Real-time Data**: Integrated with USCIS and State Department for current processing times and requirements
- **Agentic Automation**: Web automation to help start application processes

## Immigration Pathways Covered

- **Work Visas**: H-1B, L-1, O-1, E-2, TN
- **Green Cards**: EB-1, EB-2, EB-3, Family-based
- **Study**: F-1, Optional Practical Training (OPT)
- **Other**: B-1/B-2, K-1, Asylum, Naturalization

## Architecture

```
├── backend/                 # FastAPI backend server
│   ├── api/                # API endpoints
│   ├── core/               # Core business logic
│   ├── models/             # Data models
│   ├── services/           # External service integrations
│   └── knowledge/          # Immigration knowledge base
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API clients
│   │   └── types/         # TypeScript types
└── docs/                  # Documentation
```

## Quick Start

### 1. Prerequisites
- Python 3.11+
- Node.js 18+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### 2. Clone and Setup

```bash
git clone <repository-url>
cd ImmigrationClaude
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Setup environment
cp .env.example .env
# Edit .env and add your Anthropic API key:
# ANTHROPIC_API_KEY=your_api_key_here

# Run backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 4. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Optional: Configure API URL
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 5. Using Startup Scripts

For convenience, use the provided scripts:

```bash
# Make executable (first time only)
chmod +x backend/run.sh frontend/run.sh

# Terminal 1 - Run backend
cd backend && ./run.sh

# Terminal 2 - Run frontend
cd frontend && ./run.sh
```

## Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[User Guide](docs/USER_GUIDE.md)** - How to use the system
- **[API Documentation](docs/API.md)** - Complete API reference

## Usage

1. **Start Assessment**: Answer questions about your situation
2. **Review Options**: See personalized immigration pathway recommendations
3. **Compare Pathways**: Detailed comparison with pros/cons, timeline, costs
4. **Get Guidance**: Step-by-step instructions for your chosen path
5. **Start Process**: Use automated assistance to begin applications

## Legal Disclaimer

This tool provides informational guidance only and does not constitute legal advice. For specific legal matters, consult with a licensed immigration attorney.

## License

MIT License
