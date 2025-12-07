# Quickstart: AI-Native Textbook with RAG Chatbot

**Date**: 2025-12-07
**Feature**: 1-textbook-gen

## Prerequisites

### Development Environment
- Python 3.11+ with pip
- Node.js 18+ with npm
- Git
- Google Cloud account with Gemini API access
- Qdrant Cloud account (free tier)
- Neon Serverless Postgres account (free tier)

### Required API Keys and Credentials
- `GEMINI_API_KEY`: Google Gemini API key
- `QDRANT_API_KEY`: Qdrant Cloud API key
- `NEON_DATABASE_URL`: Neon Postgres connection string

## Setup Instructions

### 1. Clone and Initialize Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your-gemini-api-key"
export QDRANT_API_KEY="your-qdrant-api-key"
export QDRANT_HOST="your-qdrant-cluster-url"
export NEON_DATABASE_URL="your-neon-database-url"
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build the site
npm run build
```

### 4. Database Setup
```bash
# Run database migrations
cd backend
python -m src.scripts.setup_database
```

## Configuration

### Environment Variables
Create `.env` file in the backend directory:

```env
GEMINI_API_KEY=your-gemini-api-key
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_HOST=your-qdrant-cluster-url
NEON_DATABASE_URL=your-neon-database-url
QDRANT_COLLECTION_NAME=textbook_chunks
GEMINI_MODEL_NAME=gemini-1.5-flash
EMBEDDING_MODEL_NAME=embedding-001
```

### Docusaurus Configuration
The `docusaurus.config.js` file contains:
- Site metadata (title, description)
- Theme configuration
- Plugin settings for the chat widget
- Internationalization settings for Urdu support

## Running the Application

### Development Mode

#### Backend (FastAPI)
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

#### Frontend (Docusaurus)
```bash
cd frontend
npm start
```

### Production Mode

#### Backend Deployment
```bash
# Deploy to Railway (example)
cd backend
railway login
railway init
railway up
```

#### Frontend Deployment
```bash
# Build and deploy to GitHub Pages
cd frontend
npm run build
# Deployment to GitHub Pages via GitHub Actions
```

## API Endpoints

### Backend API (FastAPI)
- `POST /ingest` - Ingest textbook content for embedding
- `POST /embed` - Generate embeddings for content chunks
- `POST /query` - General RAG query against textbook content
- `POST /select-query` - Selection-only mode query using provided text only

### Request/Response Examples

#### Query Request
```json
{
  "question": "What are the key principles of humanoid locomotion?",
  "user_id": "optional-user-id"
}
```

#### Query Response
```json
{
  "answer": "The key principles of humanoid locomotion include...",
  "sources": [
    {
      "chapter_id": "ch6",
      "section_id": "6.2",
      "char_range": [100, 250]
    }
  ],
  "confidence": 0.95
}
```

#### Selection Query Request
```json
{
  "selected_text": "Humanoid locomotion requires precise balance control...",
  "question": "How does this relate to control systems?",
  "user_id": "optional-user-id"
}
```

## Content Management

### Adding New Chapters
1. Create a new directory in `frontend/docs/` with chapter content
2. Add the chapter to `sidebars.js` for auto-sidebar generation
3. Run the ingestion script to process the new content:

```bash
cd backend
python -m src.scripts.ingest-chapters
```

### Updating Content
1. Edit the relevant markdown files in `frontend/docs/`
2. Re-run the ingestion and embedding process:

```bash
cd backend
python -m src.scripts.update-embeddings
```

## Testing

### Unit Tests
```bash
cd backend
python -m pytest tests/unit/
```

### Integration Tests
```bash
cd backend
python -m pytest tests/integration/
```

### End-to-End Tests
```bash
cd frontend
npm run test:e2e
```

## Deployment

### GitHub Pages (Frontend)
1. Configure GitHub Actions workflow in `.github/workflows/deploy.yml`
2. Push changes to main branch to trigger deployment
3. Site will be available at `https://<username>.github.io/<repository>`

### Backend Hosting (Railway)
1. Connect Railway to your GitHub repository
2. Configure environment variables in Railway dashboard
3. Set up automatic deployments from main branch

## Troubleshooting

### Common Issues

#### API Rate Limits
- Check your Gemini API usage in Google Cloud Console
- Implement caching for frequent queries
- Consider upgrading to higher tier if needed

#### Vector Search Performance
- Verify Qdrant collection is properly indexed
- Check that embeddings were generated correctly
- Review chunking strategy for optimal results

#### Frontend-Backend Communication
- Ensure CORS is properly configured in FastAPI
- Verify backend URL is correctly set in frontend
- Check network connectivity between services

### Monitoring
- Check application logs in deployment platform
- Monitor response times and error rates
- Track API usage against free tier limits