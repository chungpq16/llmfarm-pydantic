"""
Production-ready Bosch LLM Farm client.
Clean, reliable interface that works with Bosch's API requirements.
"""
import asyncio
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from openai import AsyncOpenAI


@dataclass
class LLMConfig:
    """Configuration for the LLM Farm client"""
    model: str = "gpt-4o-mini"
    api_key: str = "secrets"  # Replace with actual API key
    subscription_key: str = "my-farm-key"  # Replace with actual subscription key
    base_url: str = "https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18"
    api_version: str = "2024-08-01-preview"
    timeout: float = 30.0
    log_level: str = "INFO"


@dataclass
class CompletionResponse:
    """Response from completion"""
    content: str
    model_used: str
    usage: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


class BoschLLMFarm:
    """
    Clean, production-ready client for Bosch LLM Farm.
    
    This client uses direct OpenAI API calls with the required extra_query parameter
    that Bosch Farm needs. It provides a clean, PydanticAI-style interface while
    ensuring reliable communication with the farm.
    """
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize the Bosch LLM Farm client.
        
        Args:
            config: LLM configuration. If None, uses default config.
        """
        self.config = config or LLMConfig()
        self._setup_logging()
        self._client = self._create_client()
        
        self.logger.info(f"Bosch LLM Farm client initialized - Model: {self.config.model}")
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _create_client(self) -> AsyncOpenAI:
        """Create and configure the OpenAI client"""
        return AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            default_headers={
                "genaiplatform-farm-subscription-key": self.config.subscription_key
            },
            timeout=self.config.timeout
        )
    
    def _build_messages(self, user_text: str, system_prompt: str) -> list:
        """Build the message list for the API call"""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    
    def _extract_usage(self, response) -> Optional[Dict[str, Any]]:
        """Extract usage information from response"""
        if hasattr(response, 'usage') and response.usage:
            return {
                "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0),
                "completion_tokens": getattr(response.usage, 'completion_tokens', 0),
                "total_tokens": getattr(response.usage, 'total_tokens', 0)
            }
        return None
    
    async def _complete_async(self, user_text: str, system_prompt: str = "You are a helpful assistant") -> CompletionResponse:
        """
        Internal async completion method.
        
        Args:
            user_text: The user's input text
            system_prompt: System prompt to guide the AI
            
        Returns:
            CompletionResponse with the generated content
            
        Raises:
            Exception: If the API call fails
        """
        if not user_text or not user_text.strip():
            raise ValueError("User text cannot be empty")
        
        messages = self._build_messages(user_text, system_prompt)
        
        self.logger.info(f"Making API call - User text: {user_text[:100]}...")
        self.logger.debug(f"Messages: {len(messages)} messages")
        
        try:
            response = await self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                extra_query={"api-version": self.config.api_version}  # Required by Bosch Farm!
            )
            
            content = response.choices[0].message.content
            usage = self._extract_usage(response)
            
            self.logger.info("Completion successful")
            self.logger.debug(f"Response length: {len(content)} characters")
            
            return CompletionResponse(
                content=content,
                model_used=self.config.model,
                usage=usage,
                request_id=getattr(response, 'id', None)
            )
            
        except Exception as e:
            self.logger.error(f"API call failed: {e}")
            raise
    
    def complete(self, user_text: str, system_prompt: str = "You are a helpful assistant") -> str:
        """
        Generate text completion (synchronous).
        
        Args:
            user_text: The user's input text
            system_prompt: System prompt to guide the AI (optional)
            
        Returns:
            Generated text response
            
        Example:
            >>> client = BoschLLMFarm()
            >>> response = client.complete("Hello, how are you?")
            >>> print(response)
            Hello! I'm just a computer program...
        """
        response = asyncio.run(self._complete_async(user_text, system_prompt))
        return response.content
    
    async def complete_async(self, user_text: str, system_prompt: str = "You are a helpful assistant") -> str:
        """
        Generate text completion (asynchronous).
        
        Args:
            user_text: The user's input text
            system_prompt: System prompt to guide the AI (optional)
            
        Returns:
            Generated text response
            
        Example:
            >>> client = BoschLLMFarm()
            >>> response = await client.complete_async("Hello, how are you?")
            >>> print(response)
            Hello! I'm just a computer program...
        """
        response = await self._complete_async(user_text, system_prompt)
        return response.content
    
    def complete_with_details(self, user_text: str, system_prompt: str = "You are a helpful assistant") -> CompletionResponse:
        """
        Generate text completion with detailed response info (synchronous).
        
        Args:
            user_text: The user's input text
            system_prompt: System prompt to guide the AI (optional)
            
        Returns:
            CompletionResponse with content, usage info, etc.
            
        Example:
            >>> client = BoschLLMFarm()
            >>> response = client.complete_with_details("Hello!")
            >>> print(f"Content: {response.content}")
            >>> print(f"Tokens used: {response.usage}")
        """
        return asyncio.run(self._complete_async(user_text, system_prompt))
    
    async def complete_with_details_async(self, user_text: str, system_prompt: str = "You are a helpful assistant") -> CompletionResponse:
        """
        Generate text completion with detailed response info (asynchronous).
        
        Args:
            user_text: The user's input text
            system_prompt: System prompt to guide the AI (optional)
            
        Returns:
            CompletionResponse with content, usage info, etc.
        """
        return await self._complete_async(user_text, system_prompt)
    
    def chat(self, message: str) -> str:
        """
        Simple chat interface with default helpful assistant prompt.
        
        Args:
            message: User message
            
        Returns:
            AI response
        """
        return self.complete(message, "You are a helpful assistant.")
    
    def code_assistant(self, code_question: str) -> str:
        """
        Code assistant interface with coding-specific prompt.
        
        Args:
            code_question: Programming question or code to analyze
            
        Returns:
            AI response focused on coding help
        """
        return self.complete(
            code_question, 
            "You are an expert software developer and coding assistant. Provide clear, concise, and accurate programming advice."
        )


# Backward compatibility alias
LLMFarmPydanticAI = BoschLLMFarm


def create_client(api_key: str, subscription_key: str, **kwargs) -> BoschLLMFarm:
    """
    Convenience function to create a client with custom credentials.
    
    Args:
        api_key: Your Bosch Farm API key
        subscription_key: Your Bosch Farm subscription key
        **kwargs: Additional configuration options
        
    Returns:
        Configured BoschLLMFarm client
    """
    config = LLMConfig(
        api_key=api_key,
        subscription_key=subscription_key,
        **kwargs
    )
    return BoschLLMFarm(config)


if __name__ == "__main__":
    print("=== Bosch LLM Farm Client - Production Version ===")
    print("🚀 Clean, reliable interface that actually works!")
    print("IMPORTANT: Replace placeholder credentials with actual values!")
    print()
    
    try:
        # Create client with default config (update the credentials!)
        client = BoschLLMFarm()
        
        # Test basic completion
        print("🔄 Testing basic completion...")
        response = client.complete("Hello, how are you?")
        print(f"✅ Response: {response}")
        
        # Test with custom prompt
        print("\n🔄 Testing with custom system prompt...")
        response = client.complete(
            "What is Python?",
            "You are a technical expert who explains things simply."
        )
        print(f"✅ Custom prompt response: {response}")
        
        # Test detailed response
        print("\n🔄 Testing detailed response...")
        detailed = client.complete_with_details("Tell me a joke")
        print(f"✅ Content: {detailed.content}")
        print(f"📊 Usage: {detailed.usage}")
        
        # Test convenience methods
        print("\n🔄 Testing convenience methods...")
        chat_response = client.chat("What's the weather like?")
        print(f"💬 Chat: {chat_response}")
        
        code_response = client.code_assistant("How do I reverse a string in Python?")
        print(f"💻 Code help: {code_response}")
        
        # Test async
        print("\n🔄 Testing async...")
        async def test_async():
            response = await client.complete_async("What is AI?")
            print(f"⚡ Async response: {response}")
        
        asyncio.run(test_async())
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        if "secrets" in str(e) or "my-farm-key" in str(e):
            print("\n💡 Tip: You need to replace the placeholder credentials!")
            print("   config = LLMConfig(api_key='your-real-key', subscription_key='your-real-sub-key')")
        
        print("\n=== SETUP INSTRUCTIONS ===")
        print("1. Replace 'secrets' with your actual API key")
        print("2. Replace 'my-farm-key' with your actual subscription key")
        print("3. Ensure you're on the correct network/VPN")
        print("4. Verify the farm URL is accessible")