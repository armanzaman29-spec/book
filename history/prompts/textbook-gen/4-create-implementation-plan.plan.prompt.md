---
id: 4
title: Create Implementation Plan
stage: plan
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: textbook-gen
branch: 1-textbook-gen
user: user
command: /sp.plan
labels: [planning, architecture, textbook, rag]
links:
  spec: specs/1-textbook-gen/spec.md
  plan: specs/1-textbook-gen/plan.md
  adr: null
  pr: null
files:
  - specs/1-textbook-gen/plan.md
  - specs/1-textbook-gen/research.md
  - specs/1-textbook-gen/data-model.md
  - specs/1-textbook-gen/quickstart.md
  - specs/1-textbook-gen/contracts/rag-api.yaml
  - specs/1-textbook-gen/contracts/content-api.yaml
tests:
  - none
---

## Prompt

```text
Create a complete execution plan for building an AI-native textbook with an embedded RAG chatbot, based on the existing /sp.specify.

CRITICAL CONSTRAINT:
- Use ONLY a native *Gemini API key*
- DO NOT use any OpenAI API, OpenAI-compatible, or external_client bridges
- All embeddings + generation must be done via *Google Gemini API*

OBJECTIVE
Plan the end-to-end implementation of:
1) A Docusaurus-based textbook created with Spec-Kit Plus + Claude Code and deployed to GitHub Pages
2) An integrated RAG chatbot using *Gemini API*, FastAPI, Neon Serverless Postgres, and Qdrant Cloud (free tier)
3) Selection-only answering mode where the bot can respond using ONLY the user-selected text

------------------------------------------------------------------

ARCHITECTURE SKETCH (text-based)

Authoring (Spec-Kit Plus + Claude Code)
→ Structured Markdown + front-matter
→ Docusaurus (Auto Sidebar)
→ GitHub Pages (static hosting)
→ Embedded Chat UI (custom React widget)

Chat UI (Frontend JS)
→ FastAPI Backend
   - /ingest
   - /embed     (Gemini embeddings)
   - /query     (Gemini generation)
   - /select-query (strict-selected-text mode)
→ Neon Postgres (metadata + provenance)
→ Qdrant Cloud (vector store, free tier)
→ Gemini API (embeddings + reasoning)

Selection Mode:
- User highlights text in Docusaurus
- Selected text OR (doc_id + offset) sent to /select-query
- Backend:
  - Does NOT perform vector search
  - Uses ONLY received text as context
  - Hard-locks prompt to selected content
- Answer + provenance returned

---------1.5-flash / gemini-1.5-pro
   - Tradeoff: speed vs reasoning depth

2. Chunking Strategy
   - Paragraph-based
   - Semantic-based
   - Tradeoff: recall vs accuracy

3. Selection-only Enforcement
   - Server only (not client)
   - Must block external context automatically
   - Tradeoff: UX friction vs accuracy

4. Backend Deployment
   - Render / Railway / Fly.io
   - Tradeoff: ease vs persistent uptime

5. Index Update Strategy
   - On every commit
   - Scheduled batch
   - Tradeoff: freshness vs cost

All choices logged in: DECISIONS.md

----------------------------------------------------------------------------------------------------------------

SECTION STRUCTURE (Docusaurus + Data Model)

Auto-sidebar generated from:

1. Introduction to Physical AI
2. Foundations of Robotics: Systems, Structure & Core Mechanisms
3. Human-Inspired Design Principles in Humanoid Robotics
4. Perception Systems in Humanoids
5. AI, Deep Learning & Control Systems
6. Humanoid Locomotion and Manipulation

Each chapter includes:
- chapter.md
- examples/
- assets/
- Front-matter fields:
  - chapter_id
  - section_id
  - learning_objectives
  - apa_references
  - chunking_strategy
  - embedding_ready: true/false

Each paragraph becomes:
- Embedding chunk → Qdrant
- Metadata → Neon:
  - doc_id
  - chapter_id
  - section_id
  - char_offset
  - length
  - source_url
  - text_hash

------------------------------------------------------------------

RESEARCH APPROACH (concurrent)

- Research WHILE writing each chapter
- For every chapter:
  1. Research & source
  2. Write using Claude Code
  3. Apply Spec-Kit Plus prom------------

TESTING STRATEGY (acceptance-focused)

UNIT TESTS:
- Markdown → chunk conversion
- Chunk → Gemini embedding → Qdrant insertion
- Metadata → Neon insert
- /select-query: ensure ONLY selected text used

INTEGRATION TESTS:
- Question → Vector search → Answer
- Selection-text → Answer (no retrieval used)

ACCEPTANCE TESTS:
- Docusaurus builds and deploys
- Sidebar auto-generates
- Chat UI loads in every chapter
- Selected-text answers contain only words from the selected region
- All answers return:
  - chapter_id
  - section_id
  - char_range

QUALITY BARS:
- ≥90% answer accuracy on content questions
- 0 hallucinations in selection-only mode
- Free-tier limits respected

------------------------------------------------------------------

PHASED EXECUTION PLAN

PHASE 1 — RESEARCH
- Define objectives per chapter
- Create APA reference base
- Write prompts for Claude Code + Spec-Kit Plus

PHASE 2 — FOUNDATION
- Install Docusaurus
- Setup auto sidebar
- Create FastAPI base
- Connect Gemini API
- Setup Neon + Qdrant
- Create /ingest & /embed

PHASE 3 — ANALYSIS
- Finalize 2 chapters
- Chunk + embed content
- Build Chat UI
- Implement /query & /select-query
- Run unit + integration testing

PHASE 4 — SYNTHESIS
- Complete all chapters
- Full ingestion
- Deploy site + backend
- Validate each acceptance criteria
- Lock system + spec

------------------------------------------------------------------

FINAL OUTPUT MUST INCLUDE

- Text-based architecture diagram
- Section-by-section execution plan
- Gemini integration steps
- Dataflow map (Docusaurus → Qdrant → Gemini → UI)
- Test matrix
- Phase breakdown:
  Research → Foundation → Analysis → Synthesis
```

## Response snapshot

Created comprehensive implementation plan for AI-native textbook with RAG chatbot. Generated plan.md with architecture overview, technical context, and project structure. Created research.md documenting key decisions (Gemini 1.5 Flash, semantic chunking, server-side selection enforcement). Created data-model.md with entity models for chapters, content chunks, queries, and sessions. Created quickstart.md with setup and deployment instructions. Created API contracts (rag-api.yaml and content-api.yaml) defining endpoints for ingestion, embedding, querying, and content management. All components designed to work with Gemini API exclusively and meet free-tier constraints.

## Outcome

- ✅ Impact: Complete implementation plan created with architecture, data models, API contracts, and deployment instructions
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and API contracts
- 🔁 Next prompts: Ready for task generation (/sp.tasks)
- 🧠 Reflection: Plan comprehensively addresses all requirements including Gemini API constraint, free-tier operation, and selection-only mode

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All plan components created successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks from plan using /sp.tasks