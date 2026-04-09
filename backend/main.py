"""
Healthcare Assistant Chatbot - FastAPI Backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

from config import settings
from llm_service import llm_service
from rag_service import rag_service
from prompts import check_for_emergency, EMERGENCY_RESPONSE, DISCLAIMER_MESSAGE


# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Assistant API",
    description="Backend API for Healthcare Information Chatbot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ChatMessage(BaseModel):
    """Single chat message"""
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    """Chat request from frontend"""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """Chat response to frontend"""
    response: str
    is_emergency: bool = False
    disclaimer: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    llm_provider: str
    rag_enabled: bool
    rag_documents_count: int = 0


# API Endpoints
@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Healthcare Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    rag_count = 0
    if settings.enable_rag:
        try:
            rag_count = rag_service.get_collection_count()
        except:
            pass
    
    return HealthCheckResponse(
        status="healthy",
        llm_provider=settings.llm_provider,
        rag_enabled=settings.enable_rag,
        rag_documents_count=rag_count
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    
    Handles user messages and returns AI responses with safety checks
    """
    try:
        user_message = request.message.strip()
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Check for emergency keywords
        is_emergency = check_for_emergency(user_message)
        if is_emergency:
            return ChatResponse(
                response=EMERGENCY_RESPONSE,
                is_emergency=True
            )
        
        # Convert conversation history to dict format
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]
        
        # Retrieve RAG context if enabled
        context = None
        use_rag = False
        if settings.enable_rag:
            try:
                use_rag = rag_service.should_use_rag(user_message)
                if use_rag:
                    context = rag_service.retrieve_context(user_message)
            except Exception as e:
                print(f"RAG retrieval error: {e}")
                # Continue without RAG if it fails
                use_rag = False
                context = None
        
        # Get LLM response
        response = await llm_service.get_response(
            user_message=user_message,
            conversation_history=conversation_history,
            use_rag=use_rag and context is not None,
            context=context
        )
        
        return ChatResponse(
            response=response,
            is_emergency=False,
            disclaimer=DISCLAIMER_MESSAGE
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/disclaimer", response_model=dict)
async def get_disclaimer():
    """Get the medical disclaimer"""
    return {"disclaimer": DISCLAIMER_MESSAGE}


# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )