# Quick Start Guide

## Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- OpenAI API key

## Setup Steps

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo OPENAI_API_KEY=your_key_here > .env
# Or manually create .env and add: OPENAI_API_KEY=your_key_here

# Run the server
uvicorn main:app --reload --port 8000
```

Backend will be available at http://localhost:8000

### 2. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

Frontend will be available at http://localhost:3000

## Usage

1. **Add Content**: 
   - Go to "Add Content" tab
   - Enter text note OR paste a URL
   - Click "Add Content"

2. **View Items**: 
   - Go to "Saved Items" tab
   - See all your saved content

3. **Ask Questions**: 
   - Go to "Ask Question" tab
   - Enter your question
   - Get AI-powered answer with source citations

## Testing the API

You can test the API directly:

```bash
# Ingest text
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"content": "FastAPI is a modern web framework for building APIs with Python."}'

# Ingest URL
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"url": "https://fastapi.tiangolo.com"}'

# List items
curl http://localhost:8000/api/items

# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'
```

## Troubleshooting

- **Import errors**: Make sure virtual environment is activated
- **OpenAI errors**: Check your API key in `.env` file
- **Port conflicts**: Change ports in `main.py` (backend) or `vite.config.js` (frontend)
- **CORS errors**: Ensure backend is running on port 8000

