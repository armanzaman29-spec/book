---
id: 1
title: Create Project Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, setup, project]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
project Name: Physical AI & Humanoid Robotics - Essentials

purpose:
create a short, clean, professional AI-Native textbook based on the physical AI & Humanoid Robotics course.
The book must server as a fast, simple, high-quality learning resource built with a modern Docusaurus UI  and a fully integrated free-tier RAG Chabot.

Scope:
-6 Short Chapters:
1. Introduction to Physical AI
2. Foundations of Robotics: Systems, Structure & Core Mechanisms
3. Human-Inspired Design Principles in Humanoid Robotics
4. Perception Systems in Humanoids
5. AI, Deep Learning & Control Systems
6. Humanoid Locomotion and Manipulation
-Clean UI
-Free-tier friendly
-Lightweight embeddings

Core Principles:
-Simplicity
-Accuracy
-Minimalism
-Fast builds
-Free-tier architecture
-RAG answer ONLY from book text

Key Features:
-Docusaurus textbook
-RAG chatbot (Qdrant + Neon + FastAPI)
-Select-text -> Ask AI
-Optional urdu / personalize features

Constraints:
-No heavy GPU usage
-Minimal embeddings

Success Criteria:
-Build success
-Accurate chatbot
-Clean UI
-Smooth Github pages deployment

Generate full constitution.
```

## Response snapshot

Created a comprehensive constitution for the Physical AI & Humanoid Robotics textbook project with six core principles: Simplicity and Minimalism, Accuracy and Quality, Free-Tier Architecture, RAG-Only Knowledge Base, Fast Builds and Performance, and Clean UI/UX Design. The constitution also includes technical constraints, development workflow guidelines, and governance rules aligned with the project requirements.

## Outcome

- ✅ Impact: Created foundational project constitution document that establishes guiding principles for the Physical AI & Humanoid Robotics textbook development
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific constitution
- 🔁 Next prompts: Proceed with project setup and feature specification based on established constitution
- 🧠 Reflection: Constitution successfully captures the essential principles of simplicity, accuracy, free-tier architecture, and RAG-only knowledge base as specified in requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution aligns with specified project requirements
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on established constitution