# Development Environment Setup

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Google Cloud account with Gemini API access
- Qdrant Cloud account (free tier)
- Neon Serverless Postgres account (free tier)

## Project Structure

```
project-root/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   ├── api/            # API endpoints
│   │   ├── utils/          # Utility functions
│   │   └── config/         # Configuration
│   └── requirements.txt    # Python dependencies
├── frontend/               # Docusaurus frontend
│   ├── docs/              # Textbook content
│   ├── src/               # Custom components
│   ├── static/            # Static assets
│   └── package.json       # Node.js dependencies
├── scripts/                # Utility scripts
├── specs/                  # Feature specifications
└── docs/                   # Documentation
```

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. Run the backend:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
GEMINI_API_KEY=your-gemini-api-key
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_HOST=your-qdrant-cluster-url
NEON_DATABASE_URL=your-neon-database-url
QDRANT_COLLECTION_NAME=textbook_chunks
GEMINI_MODEL_NAME=gemini-1.5-flash
EMBEDDING_MODEL_NAME=embedding-001
```

## Running Tests

Backend tests:
```bash
cd backend
python -m pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

## Building for Production

Backend:
```bash
# No specific build step needed for FastAPI
```

Frontend:
```bash
cd frontend
npm run build
```

## Deployment

### Frontend
The frontend is designed to be deployed to GitHub Pages:
1. Run `npm run build`
2. The output is in the `build/` directory
3. Configure GitHub Pages to serve from the `build/` directory

### Backend
The backend can be deployed to various platforms like Railway, Render, or Fly.io:
1. Ensure all environment variables are configured in the deployment platform
2. The backend exposes a standard FastAPI application on port 8000
3. Make sure to configure CORS appropriately for your frontend domain