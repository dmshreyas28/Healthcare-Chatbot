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
