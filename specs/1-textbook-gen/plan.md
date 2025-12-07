# Implementation Plan: AI-Native Textbook with RAG Chatbot

**Branch**: `1-textbook-gen` | **Date**: 2025-12-07 | **Spec**: [specs/1-textbook-gen/spec.md](../1-textbook-gen/spec.md)

**Input**: Feature specification from `/specs/1-textbook-gen/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Docusaurus-based AI-native textbook with integrated RAG chatbot using Google Gemini API, FastAPI backend, Neon Serverless Postgres, and Qdrant Cloud. The system will include selection-only answering mode where the bot responds using only user-selected text, deployed to GitHub Pages with free-tier architecture constraints.

## Technical Context

**Language/Version**: Python 3.11 (for FastAPI backend), JavaScript/TypeScript (for frontend Docusaurus)
**Primary Dependencies**: FastAPI, Docusaurus, Google Generative AI SDK, Qdrant, Neon Postgres
**Storage**: Qdrant Cloud (vector store), Neon Serverless Postgres (metadata), GitHub Pages (static content)
**Testing**: pytest (backend), Jest/Cypress (frontend)
**Target Platform**: Web-based (GitHub Pages hosting)
**Project Type**: Web application
**Performance Goals**: <3 second page load times, <2 second AI response times, 98% accuracy for textbook content questions
**Constraints**: Free-tier usage limits, no heavy GPU usage, minimal resource consumption, 98% accuracy requirement
**Scale/Scope**: 6 textbook chapters, multiple users, concurrent AI requests within free-tier limits

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Simplicity and Minimalism**: Architecture uses minimal components (Docusaurus, FastAPI, Qdrant, Neon) with clear separation of concerns
- **Accuracy and Quality**: RAG system ensures answers only from textbook content with 98% accuracy requirement
- **Free-Tier Architecture**: All components selected for free-tier operation (Qdrant Cloud free tier, Neon Serverless, GitHub Pages)
- **RAG-Only Knowledge Base**: System designed to use exclusively textbook content with selection-only mode
- **Fast Builds and Performance**: Optimized for quick Docusaurus builds and responsive AI responses
- **Clean UI/UX Design**: Custom React widget for chat interface designed for learning experience

## Project Structure

### Documentation (this feature)

```text
specs/1-textbook-gen/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── rag_service.py
│   │   └── selection_service.py
│   ├── api/
│   │   ├── ingest.py
│   │   ├── embed.py
│   │   ├── query.py
│   │   └── select_query.py
│   └── config/
│       └── settings.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── docs/
│   ├── 01-introduction-to-physical-ai/
│   ├── 02-foundations-of-robotics/
│   ├── 03-human-inspired-design/
│   ├── 04-perception-systems/
│   ├── 05-ai-deep-learning/
│   └── 06-humanoid-locomotion/
├── src/
│   ├── components/
│   │   └── ChatWidget/
│   │       ├── ChatWidget.jsx
│   │       ├── ChatInterface.jsx
│   │       └── SelectionHandler.js
│   └── pages/
├── static/
├── docusaurus.config.js
├── sidebars.js
└── package.json

scripts/
├── ingest-chapters.py
└── update-embeddings.py
```

**Structure Decision**: Web application with separate backend and frontend components. Backend handles AI processing and data management using FastAPI, while frontend provides the textbook interface using Docusaurus with custom React chat widget. This separation allows for independent scaling and maintenance while meeting all constitutional requirements.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple services | Required for proper separation of concerns between static content (Docusaurus) and dynamic AI processing (FastAPI) | Single service would violate free-tier constraints and performance requirements |
| External vector store | Qdrant provides necessary performance and scaling for RAG implementation | In-memory storage would not handle the volume of textbook content effectively |