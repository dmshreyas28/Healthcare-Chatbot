"""
LLM Service - Handles interaction with OpenAI, Anthropic, and Ollama APIs
"""
from typing import List, Dict
from openai import OpenAI
from anthropic import Anthropic
import httpx
from config import settings
from prompts import get_system_prompt


class LLMService:
    """Service for interacting with Large Language Models"""
    
    def __init__(self):
        self.provider = settings.llm_provider
        
        # Initialize clients based on provider
        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not found in environment variables")
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
        
        elif self.provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not found in environment variables")
            self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
            self.model = settings.anthropic_model
        
        elif self.provider == "ollama":
            self.ollama_base_url = settings.ollama_base_url
            self.model = settings.ollama_model
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def get_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, str]] = None,
        use_rag: bool = False,
        context: str = None
    ) -> str:
        """
        Get a response from the LLM
        
        Args:
            user_message: The user's input message
            conversation_history: Previous messages in the conversation
            use_rag: Whether to use RAG context
            context: RAG context to include in the prompt
        
        Returns:
            The LLM's response as a string
        """
        if conversation_history is None:
            conversation_history = []
        
        # Get system prompt
        system_prompt = get_system_prompt(use_rag=use_rag)
        
        # Add RAG context if provided
        if use_rag and context:
            enhanced_message = f"""Context from trusted medical sources:
{context}

User Question: {user_message}

Please answer based on the provided context."""
        else:
            enhanced_message = user_message
        
        # Route to appropriate provider
        if self.provider == "openai":
            return await self._get_openai_response(
                system_prompt, 
                enhanced_message, 
                conversation_history
            )
        elif self.provider == "anthropic":
            return await self._get_anthropic_response(
                system_prompt, 
                enhanced_message, 
                conversation_history
            )
        elif self.provider == "ollama":
            return await self._get_ollama_response(
                system_prompt, 
                enhanced_message, 
                conversation_history
            )
    
    async def _get_openai_response(
        self, 
        system_prompt: str, 
        user_message: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Get response from OpenAI API"""
        try:
            # Build messages array
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history
            messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _get_anthropic_response(
        self, 
        system_prompt: str, 
        user_message: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Get response from Anthropic API"""
        try:
            # Build messages array (Anthropic format)
            messages = []
            
            # Add conversation history
            messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call Anthropic API
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_prompt,
                messages=messages,
                temperature=0.7
            )
            
            return response.content[0].text
        
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def _get_ollama_response(
        self, 
        system_prompt: str, 
        user_message: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Get response from Ollama API"""
        try:
            # Build messages array
            messages = []
            
            # Add system message
            messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history
            messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call Ollama API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 1000
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                print(f"Ollama response: {result}")  # Debug logging
                return result["message"]["content"]
        
        except Exception as e:
            print(f"Ollama error: {str(e)}")  # Debug logging
            raise Exception(f"Ollama API error: {str(e)}")


# Global LLM service instance
llm_service = LLMService()