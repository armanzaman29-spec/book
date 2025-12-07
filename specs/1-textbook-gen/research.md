# Research: AI-Native Textbook with RAG Chatbot

**Date**: 2025-12-07
**Feature**: 1-textbook-gen

## Decision Log

### 1. AI Model Selection: Gemini 1.5 Flash vs Gemini 1.5 Pro

**Decision**: Gemini 1.5 Flash
**Rationale**: For textbook Q&A, speed and cost efficiency are prioritized over maximum reasoning depth. Flash provides faster response times and lower costs while still offering excellent performance for content-based questions.
**Alternatives considered**:
- Gemini 1.5 Pro: Better reasoning depth but slower and more expensive
- Other models: Would violate the constraint of using only Gemini API

### 2. Chunking Strategy: Semantic vs Paragraph-based

**Decision**: Semantic chunking with paragraph boundaries
**Rationale**: Semantic chunking provides better context preservation for AI understanding while maintaining readability. Keeping paragraph boundaries ensures coherent content segments.
**Alternatives considered**:
- Paragraph-only: Might break up related concepts
- Pure semantic: Might create chunks that are hard to trace back to source

### 3. Selection-only Enforcement: Client vs Server

**Decision**: Server-side enforcement only
**Rationale**: Server-side enforcement provides security and prevents bypassing the selection-only constraint. Client-side could be circumvented by users.
**Alternatives considered**:
- Client-side: Faster but insecure
- Hybrid approach: More complex without added benefit

### 4. Backend Deployment: Render vs Railway vs Fly.io

**Decision**: Railway (for initial deployment)
**Rationale**: Railway offers generous free tier, easy deployment, and good integration with Python/FastAPI applications. Good for initial development and testing.
**Alternatives considered**:
- Render: Good free tier but slightly less generous
- Fly.io: More complex but better for scaling

### 5. Index Update Strategy: On-demand vs Scheduled vs Commit-triggered

**Decision**: Commit-triggered updates via GitHub Actions
**Rationale**: Ensures content freshness automatically when textbook is updated, while maintaining free-tier cost efficiency.
**Alternatives considered**:
- Scheduled: Might update unnecessarily and consume resources
- On-demand: Could lead to stale content if forgotten

## Technical Research Findings

### Gemini API Integration

- **Embedding model**: `embedding-001` (Google's text-embedding model)
- **Generation model**: `gemini-1.5-flash` (for balance of speed and quality)
- **Rate limits**: Free tier allows 60 requests per minute for Gemini models
- **Token limits**: 1M tokens per day for free tier
- **Pricing**: Free tier sufficient for development and low-traffic deployment

### Qdrant Cloud Free Tier

- **Storage**: 1GB vector storage
- **Vectors**: Up to 1M vectors
- **Queries**: Unlimited queries
- **Collections**: Up to 5 collections
- **Sufficient for**: A textbook with 6 chapters and reasonable chunking

### Neon Serverless Postgres

- **Storage**: 1GB storage in free tier
- **Connections**: Up to 20 concurrent connections
- **Compute**: 1 CPU, 1GB RAM
- **Sufficient for**: Metadata storage for textbook content and user sessions

### Docusaurus Integration

- **Auto-sidebar**: Built-in feature using `sidebars.js`
- **Custom components**: React components can be embedded using MDX
- **Static export**: Compatible with GitHub Pages deployment
- **Internationalization**: Built-in i18n support for Urdu translation

### Selection-only Mode Implementation

- **Approach**: When text is selected, frontend sends the exact text content to backend endpoint
- **Server validation**: Backend uses only the provided text as context, ignoring vector search
- **Security**: Prevents client-side bypass by ensuring context is locked server-side
- **Provenance**: Response includes original text reference for transparency

## Architecture Considerations

### Performance Optimization

- **Caching**: Implement Redis caching for frequent queries (if needed beyond free tier)
- **Compression**: Compress embeddings where possible to reduce storage
- **Batch processing**: Batch embedding operations to reduce API calls
- **Frontend optimization**: Lazy-load chat widget to improve initial page load

### Error Handling

- **API failures**: Graceful degradation when Gemini API is unavailable
- **Rate limiting**: Implement retry logic with exponential backoff
- **Content freshness**: Handle scenarios where embeddings are outdated
- **Fallback responses**: Provide helpful messages when AI cannot generate response

### Security

- **API key management**: Secure storage of Gemini API key in environment variables
- **Input validation**: Validate and sanitize all user inputs
- **Rate limiting**: Implement rate limiting to prevent abuse
- **Content filtering**: Ensure responses align with educational content only