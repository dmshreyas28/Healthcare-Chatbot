"""
LLM Service - Handles interaction with OpenAI, Anthropic, and Ollama APIs
"""
import re
from typing import List, Dict
from openai import OpenAI
from anthropic import Anthropic
import httpx
from config import settings
from prompts import get_system_prompt


class LLMService:
    """Service for interacting with Large Language Models"""

    _PROMPT_ECHO_MARKERS = [
        "you are a healthcare information assistant",
        "important guidelines:",
        "safety rules:",
        "follow these rules:",
        "context from trusted medical sources:",
        "user question:",
        "please answer based on the provided context",
    ]

    _META_RESPONSE_MARKERS = [
        "your answer is correct",
        "please continue providing accurate responses",
        "1. only use information from the provided context",
        "respond directly to the user question in plain language",
    ]

    _DIAGNOSIS_PHRASES = [
        "accurately diagnose",
        "for me to diagnose",
        "diagnose it",
        "i can diagnose",
    ]
    
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
        enhanced_message = self._build_user_message(user_message, use_rag, context)

        # Route to appropriate provider
        raw_response = ""
        if self.provider == "openai":
            raw_response = await self._get_openai_response(
                system_prompt, 
                enhanced_message, 
                conversation_history
            )
        elif self.provider == "anthropic":
            raw_response = await self._get_anthropic_response(
                system_prompt, 
                enhanced_message, 
                conversation_history
            )
        elif self.provider == "ollama":
            raw_response = await self._get_ollama_response(
                system_prompt, 
                enhanced_message, 
                conversation_history
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        return self._sanitize_response(raw_response)

    def _build_user_message(self, user_message: str, use_rag: bool, context: str = None) -> str:
        """Build a user message that minimizes prompt echo behavior."""
        if use_rag and context:
            return f"""Use only the retrieved medical context below.
Retrieved medical context:
{context}

User question:
{user_message}

Give a direct user-facing answer in plain language. Do not repeat instructions."""

        return user_message

    def _sanitize_response(self, response: str) -> str:
        """Normalize model output and guard against prompt echo / unsafe phrasing."""
        if not response:
            return (
                "I could not generate a reliable response right now. "
                "Please try rephrasing your question."
            )

        cleaned = response.strip().strip('"').strip()
        cleaned = self._strip_prompt_echo_lines(cleaned)

        lowered = cleaned.lower()
        if any(phrase in lowered for phrase in self._DIAGNOSIS_PHRASES):
            return (
                "I cannot diagnose conditions, but I can share general health information. "
                "Please consult a qualified healthcare professional for personal advice."
            )

        marker_hits = sum(1 for marker in self._PROMPT_ECHO_MARKERS if marker in lowered)
        if marker_hits >= 2:
            return (
                "I could not generate a clear answer from trusted context this time. "
                "Please rephrase your question, and consult a qualified healthcare professional "
                "for personal medical advice."
            )

        if self._looks_like_meta_response(cleaned):
            return (
                "I could not generate a user-facing answer this time. "
                "Please ask again in one sentence, and I will provide general health information."
            )

        return cleaned

    def _strip_prompt_echo_lines(self, text: str) -> str:
        """Remove common instruction/context headings that should not appear in final answers."""
        filtered_lines = []
        for line in text.splitlines():
            stripped = line.strip()
            lowered = stripped.lower()

            if not stripped:
                filtered_lines.append(line)
                continue

            if any(marker in lowered for marker in self._PROMPT_ECHO_MARKERS):
                continue

            # Drop line prefixes like "User Question: ..." that sometimes leak through.
            if re.match(r"^(user question|retrieved medical context)\s*:\s*", lowered):
                continue

            filtered_lines.append(line)

        cleaned = "\n".join(filtered_lines).strip()
        return cleaned if cleaned else text

    def _looks_like_meta_response(self, text: str) -> bool:
        """Detect rubric-style or evaluator-style output that is not a user answer."""
        lowered = text.strip().lower()
        if not lowered:
            return True

        return any(marker in lowered for marker in self._META_RESPONSE_MARKERS)

    def _compose_ollama_prompt(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
    ) -> str:
        """Flatten conversation history into a single prompt for Ollama generate API."""
        prompt = ""
        if conversation_history:
            history_lines = []
            for msg in conversation_history[-20:]:
                role = msg.get("role", "").strip().lower()
                content = msg.get("content", "").strip()
                if not content or role not in {"user", "assistant"}:
                    continue
                speaker = "User" if role == "user" else "Assistant"
                history_lines.append(f"{speaker}: {content}")
            if history_lines:
                prompt += "Previous conversation:\n" + "\n".join(history_lines) + "\n\n"
        
        prompt += f"### Instruction:\n{user_message}\n\n### Response:\n"
        return prompt
    
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
                temperature=0.2,
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
                temperature=0.2
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
        """Get response from Ollama API using generate endpoint for better template control."""
        try:
            prompt = self._compose_ollama_prompt(user_message, conversation_history)

            base_payload = {
                "model": self.model,
                "system": system_prompt,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "repeat_penalty": 1.15,
                    "num_predict": 600,
                    "num_ctx": 4096,
                    "stop": ["### Instruction:", "### Input:", "User:", "Assistant:"]
                },
            }

            # Call Ollama generate API
            async with httpx.AsyncClient(timeout=180.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json=base_payload,
                )
                response.raise_for_status()
                result = response.json()

                text = result.get("response", "").strip()
                if self._looks_like_meta_response(text):
                    retry_payload = {
                        **base_payload,
                        "system": (
                            "You are a healthcare information assistant. "
                            "Answer directly in plain language with educational information only. "
                            "No meta commentary."
                        ),
                        "prompt": (
                            "Answer the current user health question directly. "
                            "Do not evaluate previous answers. "
                            "Do not repeat instructions or context headers.\n\n"
                            f"Current user question:\n{user_message}"
                        ),
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                            "repeat_penalty": 1.15,
                            "num_predict": 500,
                            "stop": ["### Instruction:", "### Input:", "User:", "Assistant:"]
                        },
                    }
                    retry_response = await client.post(
                        f"{self.ollama_base_url}/api/generate",
                        json=retry_payload,
                    )
                    retry_response.raise_for_status()
                    retry_result = retry_response.json()
                    text = retry_result.get("response", text).strip()

                print(f"Ollama response: {text}")
                return text
        
        except Exception as e:
            print(f"Ollama error: {str(e)}")  # Debug logging
            return "The Ollama model failed to generate a response (this is often due to a CUDA or memory limit error). Please check your Ollama installation and ensure the model `meditron:7b` runs successfully on your hardware."


# Global LLM service instance
llm_service = LLMService()