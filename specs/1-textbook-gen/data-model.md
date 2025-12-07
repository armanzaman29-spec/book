# Data Model: AI-Native Textbook with RAG Chatbot

**Date**: 2025-12-07
**Feature**: 1-textbook-gen

## Entity Models

### Textbook Content
- **Entity**: `Chapter`
- **Fields**:
  - `chapter_id` (string): Unique identifier for the chapter
  - `title` (string): Chapter title
  - `content` (text): Full chapter content
  - `learning_objectives` (json): List of learning objectives
  - `apa_references` (json): List of APA-formatted references
  - `chunking_strategy` (string): Strategy used for chunking
  - `embedding_ready` (boolean): Whether content is ready for embedding
  - `created_at` (datetime): Creation timestamp
  - `updated_at` (datetime): Last update timestamp

### Content Chunks
- **Entity**: `ContentChunk`
- **Fields**:
  - `chunk_id` (string): Unique identifier for the chunk
  - `chapter_id` (string): Reference to parent chapter
  - `content` (text): Chunk text content
  - `char_offset` (integer): Character offset in original document
  - `length` (integer): Length of the chunk in characters
  - `source_url` (string): URL to the original content location
  - `text_hash` (string): Hash of the text content for integrity
  - `embedding_vector_id` (string): Reference to vector in Qdrant
  - `created_at` (datetime): Creation timestamp

### User Queries
- **Entity**: `UserQuery`
- **Fields**:
  - `query_id` (string): Unique identifier for the query
  - `user_id` (string): User identifier (optional for anonymous)
  - `question` (text): Original question from user
  - `answer` (text): Generated answer from AI
  - `source_chunks` (json): List of chunk IDs used to generate answer
  - `query_type` (string): "general" or "selection" for selection-only mode
  - `selected_text` (text): Text selected by user (for selection mode)
  - `response_time_ms` (integer): Time taken to generate response
  - `created_at` (datetime): Creation timestamp

### User Sessions
- **Entity**: `UserSession`
- **Fields**:
  - `session_id` (string): Unique session identifier
  - `user_id` (string): User identifier
  - `preferences` (json): User preferences (language, etc.)
  - `bookmarks` (json): List of bookmarked content sections
  - `personalized_path` (json): Suggested learning path for user
  - `last_accessed` (datetime): Last access timestamp
  - `created_at` (datetime): Creation timestamp

### Vector Metadata (Neon DB)
- **Entity**: `VectorMetadata`
- **Fields**:
  - `vector_id` (string): ID in Qdrant vector store
  - `doc_id` (string): Document identifier
  - `chapter_id` (string): Chapter identifier
  - `section_id` (string): Section identifier
  - `char_offset` (integer): Character offset in source
  - `length` (integer): Length of the chunk
  - `source_url` (string): URL to source location
  - `text_hash` (string): Hash of original text
  - `created_at` (datetime): Creation timestamp

## Relationships

### Chapter → ContentChunk
- One-to-Many: A chapter can have multiple content chunks
- Foreign Key: `ContentChunk.chapter_id` → `Chapter.chapter_id`
- Constraint: All chunks must belong to an existing chapter

### UserSession → UserQuery
- One-to-Many: A user session can have multiple queries
- Foreign Key: `UserQuery.user_id` → `UserSession.user_id`
- Constraint: Queries must belong to an existing session (or be anonymous)

## Validation Rules

### Chapter Validation
- `title` must be 1-200 characters
- `content` must be present and non-empty
- `chapter_id` must be unique
- `embedding_ready` must be boolean

### ContentChunk Validation
- `content` must be 50-2000 characters (for optimal Gemini processing)
- `char_offset` must be non-negative
- `length` must be positive and match actual content length
- `text_hash` must match the content hash

### UserQuery Validation
- `question` must be 1-1000 characters
- `query_type` must be either "general" or "selection"
- If `query_type` is "selection", `selected_text` must be present
- `response_time_ms` must be positive

### UserSession Validation
- `session_id` must be unique
- `preferences` must be valid JSON
- `bookmarks` must be valid JSON array of bookmark objects

## State Transitions

### Chapter States
- `draft` → `review` → `published` → `archived`
- Only `published` chapters are included in embedding process
- `archived` chapters remain accessible but not updated

### ContentChunk States
- `created` → `embedded` → `indexed` → `active`
- Only `active` chunks are used for RAG queries
- State progression requires successful processing at each step

## Indexing Strategy

### Database Indexes
- `Chapter.chapter_id` (unique)
- `ContentChunk.chapter_id` (foreign key)
- `ContentChunk.text_hash` (for deduplication)
- `UserQuery.created_at` (for time-based queries)
- `VectorMetadata.doc_id` (for document-based queries)

### Qdrant Vector Indexes
- Vectors indexed by `vector_id`
- Payload includes all metadata fields for filtering
- Similarity search using cosine distance