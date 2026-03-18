# Project Context: Healthcare Assistant Chatbot

## Project Overview
This project is a web-based Healthcare Assistant Chatbot built as part of an academic project for an "Emerging Tools and Technologies" subject.

The system provides **health-related information and guidance only**.  
It does **NOT diagnose diseases, prescribe medication, or replace professional medical advice**.

The chatbot uses:
- A Large Language Model (LLM) for natural language understanding and response generation
- Optional Retrieval-Augmented Generation (RAG) to ground responses in trusted medical sources
- DevOps practices for automated build and deployment

---

## Core Objectives
- Build a user-facing **website** with a chat interface
- Use an **LLM** to answer health-related questions safely
- Ensure **accuracy and reliability** using RAG (if applicable)
- Deploy the backend using **Docker**
- Implement a basic **CI/CD pipeline** using GitHub Actions

---

## Functional Scope (IMPORTANT)
The chatbot is allowed to:
- Explain symptoms in simple, non-diagnostic language
- Provide general health and wellness information
- Explain medical terms and reports
- Suggest when a user should consult a doctor
- Provide preventive healthcare tips

The chatbot must NOT:
- Diagnose diseases
- Prescribe medications
- Provide dosage instructions
- Handle emergencies as a medical authority

Always include safety disclaimers when appropriate.

---

## System Architecture
- Frontend: Web-based chat interface
- Backend: Python API server
- LLM Service: External API-based LLM
- RAG Module (optional):
  - Chunk trusted healthcare documents
  - Generate embeddings
  - Store and retrieve from a vector database
- DevOps:
  - Docker for containerization
  - GitHub Actions for CI/CD

---

## Technology Stack
### Frontend
- HTML, CSS, JavaScript (simple implementation)
- OR React (optional)

### Backend
- Python
- FastAPI (preferred) or Flask

### AI & RAG
- LLM API (no model training or fine-tuning)
- Embeddings for semantic search
- Vector database (FAISS or ChromaDB)

### DevOps
- Docker
- GitHub Actions
- (Optional) Kubernetes

---

## Backend Design Guidelines
- Use clean modular structure
- Separate concerns:
  - API routes
  - LLM interaction
  - RAG logic
  - Configuration
- Use environment variables for secrets
- Do NOT hardcode API keys

---

## Prompting Rules for LLM
When generating responses:
- Use only retrieved context (if RAG is enabled)
- Avoid making medical diagnoses
- Use clear, empathetic, and simple language
- Encourage professional medical consultation when symptoms are serious

---

## Ethical & Safety Constraints
- Add disclaimers stating this is not medical advice
- Avoid authoritative medical language
- Handle sensitive topics carefully
- Encourage emergency services when required

---

## DevOps Expectations
- Application must run via Docker
- CI pipeline should:
  - Install dependencies
  - Run basic checks
  - Build Docker image
- Focus on reliability and reproducibility

---

## Coding Style Preferences
- Clear, readable code
- Meaningful function and variable names
- Pythonic conventions
- Minimal but sufficient comments

---

## What GitHub Copilot Should Assume
- This is an academic project
- Safety and correctness are higher priority than feature richness
- The chatbot is informational, not diagnostic
- The system will be demonstrated live

---

## Project Progress (Updated: February 11, 2026)

### ✅ COMPLETED

#### Phase 1: Project Setup & Infrastructure
- [x] Created project structure (backend/, frontend/, docs/, .github/workflows/)
- [x] Set up `.gitignore` for Python/Node/Docker projects
- [x] Created Python virtual environment on E: drive
- [x] Installed all backend dependencies (FastAPI, Uvicorn, ChromaDB, Sentence Transformers)
- [x] Set up Git repository and pushed to GitHub (https://github.com/dmshreyas28/Healthcare-Chatbot)

#### Phase 2: Backend Development
- [x] **config.py** - Environment configuration with support for OpenAI, Anthropic, and Ollama
- [x] **prompts.py** - India-specific system prompts with safety guidelines and emergency detection
- [x] **llm_service.py** - LLM service supporting multiple providers (OpenAI, Anthropic, Ollama)
- [x] **rag_service.py** - RAG implementation with ChromaDB and sentence-transformers
- [x] **main.py** - FastAPI application with /chat, /health, and /disclaimer endpoints
- [x] **load_rag_data.py** - Script to load healthcare documents into vector database
- [x] **healthcare_data/indian_health_info.txt** - Knowledge base with Indian healthcare context

#### Phase 2.1: LLM Model Setup
- [x] Downloaded **Meditron-7B-Chat** (4.1GB) - Medical domain-specific model
- [x] Imported Meditron model into Ollama
- [x] Configured backend to use Ollama with meditron:7b
- [x] Successfully tested model responses

#### Phase 2.2: RAG System Implementation
- [x] Enabled RAG in configuration (ENABLE_RAG=true)
- [x] Downloaded embedding model (all-MiniLM-L6-v2)
- [x] Loaded **16 document chunks** of Indian healthcare information including:
  - Common Indian medications (Dolo 650, Crocin, Combiflam, Disprin, Zincovit)
  - Indian healthcare system (AIIMS, PHC, CHC, Ayushman Bharat, CGHS, ESI)
  - Common health issues in India (dengue, malaria, typhoid, diabetes, hypertension, TB)
  - Traditional medicine (Ayurveda, AYUSH)
  - Drug regulations (CDSCO, Schedule H/X)
  - Emergency services (108, 102)

#### Phase 2.3: Testing & Validation
- [x] Backend server running successfully on http://localhost:8000
- [x] Tested chat endpoint with Indian healthcare queries
- [x] Verified RAG retrieval (bot correctly references Indian medications)
- [x] Confirmed emergency detection works
- [x] Validated medical disclaimers appear in responses
- [x] API documentation accessible at /docs

#### Indian Healthcare Context Integration
- [x] System prompts customized for Indian users
- [x] Knowledge base includes Indian medication brands
- [x] References to Indian healthcare schemes and facilities
- [x] Emergency numbers updated to Indian standards (108 for ambulance)
- [x] Awareness of prevalent health issues in India

### ⏳ IN PROGRESS / PENDING

#### Phase 3: Frontend Development (NOT STARTED)
- [ ] Create `frontend/index.html` - Main chat interface
- [ ] Create `frontend/styles.css` - Healthcare-themed styling
- [ ] Create `frontend/script.js` - Chat functionality and API integration
- [ ] Add medical disclaimer banner
- [ ] Implement message history display
- [ ] Add loading indicators
- [ ] Make responsive design (mobile-friendly)
- [ ] Test cross-browser compatibility

#### Phase 4: Docker Containerization (NOT STARTED)
- [ ] Create `Dockerfile` for backend
- [ ] Create `docker-compose.yml` for full stack
- [ ] Configure multi-stage builds
- [ ] Set up health checks
- [ ] Test Docker deployment locally
- [ ] Document Docker run instructions

#### Phase 5: CI/CD Pipeline (NOT STARTED)
- [ ] Create `.github/workflows/ci.yml`
- [ ] Add dependency installation step
- [ ] Add code linting (flake8/pylint)
- [ ] Add Docker image build step
- [ ] Optional: Add automated testing
- [ ] Optional: Add deployment workflow

#### Phase 6: Documentation (PARTIALLY COMPLETE)
- [x] Project context documented (this file)
- [ ] Create comprehensive `README.md` with:
  - Setup instructions
  - Environment variables guide
  - How to run locally
  - Docker deployment steps
  - Safety disclaimers
- [ ] Create `ARCHITECTURE.md` with system design diagrams
- [ ] Document API endpoints
- [ ] Add inline code comments where needed

#### Phase 7: Enhancements (OPTIONAL)
- [ ] Add conversation memory across sessions
- [ ] Implement user feedback mechanism
- [ ] Add more Indian healthcare documents to RAG
- [ ] Support for multiple languages (Hindi, Tamil, etc.)
- [ ] Voice input/output capabilities
- [ ] Integration with health tracking apps

---

## Current System Status

### Working Components
✅ **Backend API** - Fully functional on http://localhost:8000  
✅ **LLM Integration** - Meditron-7B medical model via Ollama  
✅ **RAG System** - ChromaDB with 16 Indian healthcare documents  
✅ **Safety Features** - Emergency detection, disclaimers, India-aware prompts  
✅ **API Endpoints** - /chat, /health, /disclaimer all working  

### Technology Choices Made
- **LLM Provider**: Ollama (local, free, privacy-friendly)
- **LLM Model**: Meditron-7B-Chat (medical domain-specific)
- **Backend Framework**: FastAPI
- **Vector Database**: ChromaDB
- **Embedding Model**: all-MiniLM-L6-v2
- **Geographic Focus**: India (medications, healthcare system, emergency services)

### Next Immediate Steps
1. Build frontend chat interface (Phase 3)
2. Create Docker containers (Phase 4)
3. Set up CI/CD pipeline (Phase 5)
4. Complete documentation (Phase 6)

---

## Testing Evidence
- Successfully answered: "I have runny nose, no pain and fever. What do i do?"
- Bot correctly referenced Dolo 650 and Combiflam (proving RAG works)
- Medical disclaimers properly displayed
- Emergency detection not triggered (correct for non-emergency query)
- Response time: ~10-13 seconds (acceptable for academic demo)
