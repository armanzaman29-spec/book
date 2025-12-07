---
description: "Task list for AI-Native Textbook with RAG Chatbot implementation"
---

# Tasks: AI-Native Textbook with RAG Chatbot

**Input**: Design documents from `/specs/1-textbook-gen/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Scripts**: `scripts/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure with Python 3.11 and FastAPI
- [X] T002 Create frontend project structure with Docusaurus
- [X] T003 [P] Initialize backend requirements.txt with FastAPI, google-generativeai, qdrant-client, psycopg2
- [X] T004 [P] Initialize frontend package.json with Docusaurus dependencies
- [X] T005 [P] Configure project gitignore for both backend and frontend
- [X] T006 Setup development environment documentation in docs/development.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Setup database schema and migrations framework for Neon Postgres
- [X] T008 [P] Implement Gemini API integration service in backend/src/services/gemini_service.py
- [X] T009 [P] Setup Qdrant vector store integration in backend/src/services/vector_service.py
- [X] T010 Create base models for Chapter, ContentChunk, UserQuery, and UserSession in backend/src/models/
- [X] T011 Configure error handling and logging infrastructure in backend/src/utils/
- [X] T012 Setup environment configuration management in backend/src/config/settings.py
- [X] T013 [P] Create API routing structure in backend/src/api/
- [X] T014 Setup frontend Docusaurus configuration with auto sidebar in docusaurus.config.js
- [X] T015 Create base frontend components structure in frontend/src/components/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Interactive Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Implement the core functionality to access textbook content with RAG chatbot integration

**Independent Test**: Can be fully tested by accessing textbook chapters and using the RAG chatbot to ask questions about the content, delivering immediate educational value.

### Implementation for User Story 1

- [X] T016 [P] [US1] Create Chapter model in backend/src/models/chapter.py
- [X] T017 [P] [US1] Create ContentChunk model in backend/src/models/content_chunk.py
- [X] T018 [US1] Implement ChapterService in backend/src/services/chapter_service.py
- [X] T019 [US1] Implement ContentChunkService in backend/src/services/content_chunk_service.py
- [X] T020 [US1] Create /ingest endpoint in backend/src/api/ingest.py
- [X] T021 [US1] Create /embed endpoint in backend/src/api/embed.py
- [X] T022 [US1] Create /query endpoint in backend/src/api/query.py
- [X] T023 [US1] Implement RAG service in backend/src/services/rag_service.py
- [X] T024 [US1] Create initial textbook content for Chapter 1 in frontend/docs/01-introduction-to-physical-ai/
- [X] T025 [US1] Add ChatWidget React component in frontend/src/components/ChatWidget/ChatWidget.jsx
- [X] T026 [US1] Integrate ChatWidget with Docusaurus pages
- [X] T027 [US1] Implement basic chat UI with message display and input
- [X] T028 [US1] Connect frontend to backend API endpoints
- [X] T029 [US1] Add validation and error handling for API calls
- [X] T030 [US1] Test end-to-end functionality with Chapter 1 content

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Navigate Organized Content (Priority: P1)

**Goal**: Implement auto-generated navigation sidebar to easily navigate between the 6 structured chapters

**Independent Test**: Can be fully tested by navigating between all 6 chapters using the auto-generated sidebar, delivering structured learning value.

### Implementation for User Story 2

- [ ] T031 [P] [US2] Create sidebar configuration for all 6 chapters in frontend/sidebars.js
- [ ] T032 [US2] Implement remaining 5 textbook chapters in frontend/docs/
- [ ] T033 [US2] Add navigation components in frontend/src/components/Navigation/
- [ ] T034 [US2] Implement auto-sidebar generation based on folder structure
- [ ] T035 [US2] Create chapter metadata with learning objectives in frontmatter
- [ ] T036 [US2] Add breadcrumbs navigation to each chapter page
- [ ] T037 [US2] Implement table of contents for each chapter
- [ ] T038 [US2] Add search functionality to find content across chapters
- [ ] T039 [US2] Test navigation between all 6 chapters independently

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Experience Responsive Design (Priority: P2)

**Goal**: Ensure the textbook is accessible and functional on different devices (desktop, tablet, mobile)

**Independent Test**: Can be fully tested by accessing the textbook on different screen sizes, delivering consistent user experience.

### Implementation for User Story 3

- [ ] T040 [P] [US3] Create responsive design components in frontend/src/components/Responsive/
- [ ] T041 [US3] Implement mobile-friendly navigation menu
- [ ] T042 [US3] Make ChatWidget responsive for mobile screens
- [ ] T043 [US3] Optimize text readability for different screen sizes
- [ ] T044 [US3] Create media queries for responsive layouts
- [ ] T045 [US3] Test and adjust typography for mobile devices
- [ ] T046 [US3] Optimize image loading for different screen sizes
- [ ] T047 [US3] Implement touch-friendly controls for mobile
- [ ] T048 [US3] Test responsive design across different devices and screen sizes

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Access Multilingual Content (Priority: P3)

**Goal**: Enable access to textbook content in Urdu language for users who speak Urdu

**Independent Test**: Can be fully tested by switching language settings and viewing content in Urdu, delivering inclusive learning experience.

### Implementation for User Story 4

- [ ] T049 [P] [US4] Update UserSession model to include language preference in backend/src/models/user_session.py
- [ ] T050 [US4] Create Urdu translations for Chapter 1 content
- [ ] T051 [US4] Implement i18n configuration in Docusaurus for Urdu support
- [ ] T052 [US4] Create language switcher component in frontend/src/components/LanguageSwitcher/
- [ ] T053 [US4] Update API to support multilingual content queries
- [ ] T054 [US4] Add Urdu language detection and routing
- [ ] T055 [US4] Translate UI elements to Urdu
- [ ] T056 [US4] Test multilingual functionality with Urdu content
- [ ] T057 [US4] Ensure proper text direction and formatting for Urdu

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Personalize Learning Experience (Priority: P3)

**Goal**: Allow users to customize their learning experience by bookmarking chapters or getting personalized reading paths

**Independent Test**: Can be fully tested by using personalization options, delivering tailored learning experience.

### Implementation for User Story 5

- [ ] T058 [P] [US5] Update UserSession model with bookmarks and personalized path in backend/src/models/user_session.py
- [ ] T059 [US5] Create UserSessionService in backend/src/services/user_session_service.py
- [ ] T060 [US5] Create /user-session endpoints in backend/src/api/user_session.py
- [ ] T061 [US5] Implement bookmarking functionality in frontend/src/components/Bookmark/
- [ ] T062 [US5] Create personalized reading path algorithm in backend/src/services/personalization_service.py
- [ ] T063 [US5] Add bookmark UI controls to each chapter
- [ ] T064 [US5] Implement personalized recommendation display
- [ ] T065 [US5] Create user preference settings UI
- [ ] T066 [US5] Test personalization features independently

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Selection-Only Mode Implementation

**Goal**: Implement the selection-only answering mode where the bot responds using only user-selected text

**Independent Test**: Can be fully tested by selecting text in textbook chapters and asking questions about only the selected text, ensuring answers contain only words from the selected region.

### Implementation for Selection-Only Mode

- [ ] T067 [P] [SEL] Update UserQuery model to include selected_text in backend/src/models/user_query.py
- [ ] T068 [SEL] Create /select-query endpoint in backend/src/api/select_query.py
- [ ] T069 [SEL] Implement SelectionService in backend/src/services/selection_service.py
- [ ] T070 [SEL] Add text selection handler to ChatWidget in frontend/src/components/ChatWidget/SelectionHandler.js
- [ ] T071 [SEL] Implement server-side enforcement to use only selected text as context
- [ ] T072 [SEL] Add provenance tracking to responses with source information
- [ ] T073 [SEL] Test selection-only mode to ensure no external context is used
- [ ] T074 [SEL] Add visual feedback for selected text in the UI

**Checkpoint**: Selection-only mode should work independently and in conjunction with other features

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T075 [P] Documentation updates in docs/
- [ ] T076 Code cleanup and refactoring across all components
- [ ] T077 Performance optimization across all services
- [ ] T078 [P] Additional unit tests in backend/tests/ and frontend/tests/
- [ ] T079 Security hardening for API endpoints
- [ ] T080 Run quickstart.md validation
- [ ] T081 Optimize vector storage and retrieval performance
- [ ] T082 Add comprehensive error handling and user feedback
- [ ] T083 Implement caching for frequently accessed content
- [ ] T084 Add analytics and usage tracking
- [ ] T085 Final testing across all user stories
- [ ] T086 Prepare deployment configuration for GitHub Pages and backend hosting

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Selection-Only Mode (Phase 8)**: Depends on foundational and User Story 1 completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable
- **Selection-Only Mode**: Depends on User Story 1 completion

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Chapter model in backend/src/models/chapter.py"
Task: "Create ContentChunk model in backend/src/models/content_chunk.py"

# Launch backend services for User Story 1 together:
Task: "Implement ChapterService in backend/src/services/chapter_service.py"
Task: "Implement ContentChunkService in backend/src/services/content_chunk_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add Selection-Only Mode → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence