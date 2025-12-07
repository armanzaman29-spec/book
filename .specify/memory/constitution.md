<!-- Sync Impact Report:
Version change: N/A → 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections
Removed sections: N/A
Templates requiring updates: N/A
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics - Essentials Constitution

## Core Principles

### I. Simplicity and Minimalism
All features and implementations must follow the principle of simplicity and minimalism. Solutions should be as simple as possible while maintaining functionality. Complexity must be justified with clear benefits and trade-offs.

### II. Accuracy and Quality
All content and technical implementations must maintain high accuracy and quality standards. Information presented in the textbook must be factually correct and up-to-date with current research and industry practices in physical AI and humanoid robotics.

### III. Free-Tier Architecture
All technical implementations must be designed to operate within free-tier constraints. This includes minimal resource usage, lightweight embeddings, and cost-effective deployment strategies that don't require heavy GPU usage.

### IV. RAG-Only Knowledge Base
The AI chatbot must answer questions exclusively from the book's text content. External knowledge sources are prohibited to ensure accuracy and maintain the integrity of the educational material.

### V. Fast Builds and Performance
All components must prioritize fast build times and responsive performance. This includes quick Docusaurus builds, fast embedding generation, and responsive RAG query times for the chatbot.

### VI. Clean UI/UX Design
The user interface must maintain clean, professional design principles that enhance learning experience. Navigation should be intuitive and the design should support both desktop and mobile learning.

## Technical Constraints

- No heavy GPU usage in production deployment
- Minimal embeddings to stay within free-tier limits
- GitHub Pages deployment for hosting
- Docusaurus-based documentation framework
- Qdrant vector database for RAG implementation
- Neon PostgreSQL for metadata storage
- FastAPI backend for RAG services
- Support for optional Urdu language features

## Development Workflow

- Content must be well-structured and organized by chapters
- Each chapter should have clear learning objectives
- Code examples must be tested and verified
- All features must be documented
- Regular testing of RAG accuracy required
- Performance monitoring for response times
- Deployment must be automated via GitHub Actions

## Governance

This constitution governs all development decisions for the Physical AI & Humanoid Robotics textbook project. All features, implementations, and architectural decisions must align with these principles. Any deviations require explicit justification and approval. All pull requests must verify compliance with these principles before merging.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07