# Immigration Advisory System - Setup Guide

This guide will help you get the Immigration Advisory System running on your local machine.

## Prerequisites

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Anthropic API Key** - [Get one here](https://console.anthropic.com/)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ImmigrationClaude
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create .env file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create environment file (optional)
echo "VITE_API_URL=http://localhost:8000" > .env.local
```

### 4. Running the Application

You need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Using Startup Scripts

For convenience, you can use the provided startup scripts:

### macOS/Linux:

```bash
# Make scripts executable
chmod +x backend/run.sh frontend/run.sh

# Run backend
cd backend && ./run.sh

# In another terminal, run frontend
cd frontend && ./run.sh
```

### Windows:

Create batch files or use the manual commands above.

## Configuration

### Backend Configuration (.env)

```env
ANTHROPIC_API_KEY=your_api_key_here
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite+aiosqlite:///./immigration_advisory.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Configuration (.env.local)

```env
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
# or change the port in uvicorn command
python -m uvicorn main:app --reload --port 8001
```

**Module import errors:**
```bash
# Make sure you're in the backend directory and venv is activated
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Anthropic API errors:**
- Verify your API key is correct in `.env`
- Check your API key has sufficient credits
- Ensure no extra spaces or quotes around the key

### Frontend Issues

**Port 5173 already in use:**
The Vite dev server will automatically try the next available port.

**API connection errors:**
- Verify backend is running on port 8000
- Check `VITE_API_URL` in `.env.local`
- Clear browser cache and reload

**Node modules errors:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Development Tips

### Backend Development

- API documentation is auto-generated at http://localhost:8000/docs
- Use `--reload` flag for auto-restart on code changes
- Check logs in terminal for debugging

### Frontend Development

- Vite provides hot module replacement
- Check browser console for errors
- Use React DevTools for component debugging

## Next Steps

1. Complete the assessment at http://localhost:5173/assessment
2. Review your personalized recommendations
3. Compare different pathways
4. Ask questions to the AI advisor

## Production Deployment

For production deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## Getting Help

- Check the [FAQ](./FAQ.md)
- Review API documentation at http://localhost:8000/docs
- Open an issue on GitHub

## License

MIT License - see LICENSE file for details
