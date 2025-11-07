import asyncio
import logging
from typing import Optional
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LLMFarmAgent:
    """Pydantic AI Agent wrapper for LLM Farm"""
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "gpt-4o-mini",
        system_prompt: str = "You are a helpful assistant.",
        base_url: str = "https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18/"
    ):
        """
        Initialize LLM Farm Agent with Pydantic AI
        
        Args:
            api_key: LLM Farm subscription key
            model: Model name (not added to URL, just for reference)
            system_prompt: Default system prompt for the agent
            base_url: LLM Farm endpoint URL (must end with /)
        """
        logger.info(f"Initializing LLM Farm Agent with model: {model}")
        
        # Configure AsyncOpenAI client for LLM Farm
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key="dummy",  # LLM Farm doesn't use standard API key
            default_headers={"genaiplatform-farm-subscription-key": api_key},
            default_query={"api-version": "2024-08-01-preview"}
        )
        
        # Create Pydantic AI model and agent
        model_instance = OpenAIChatModel(
            model_name=model,
            provider=OpenAIProvider(openai_client=self.client)
        )
        
        self.agent = Agent(model=model_instance, system_prompt=system_prompt)
        logger.info("✓ LLM Farm Agent initialized successfully")
    
    async def run(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Run the agent with a prompt
        
        Args:
            prompt: User prompt/query
            system_prompt: Override system prompt for this specific request
            
        Returns:
            Agent response as string
        """
        logger.info(f"Running agent: {prompt[:60]}...")
        
        try:
            # Update system prompt if provided
            if system_prompt:
                self.agent._system_prompt = system_prompt
            
            result = await self.agent.run(prompt)
            output = str(result.output)
            logger.info(f"✓ Completed ({len(output)} chars)")
            return output
            
        except Exception as e:
            logger.error(f"✗ Error: {type(e).__name__}: {str(e)}")
            raise
    
    async def run_stream(self, prompt: str, system_prompt: Optional[str] = None):
        """
        Run the agent with streaming response
        
        Args:
            prompt: User prompt/query
            system_prompt: Override system prompt for this specific request
            
        Yields:
            Response chunks as they arrive
        """
        logger.info(f"Running agent (streaming): {prompt[:60]}...")
        
        try:
            if system_prompt:
                self.agent._system_prompt = system_prompt
            
            async for chunk in self.agent.run_stream(prompt):
                yield chunk
                
        except Exception as e:
            logger.error(f"✗ Stream error: {type(e).__name__}: {str(e)}")
            raise
    
    def run_sync(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Synchronous wrapper for run"""
        return asyncio.run(self.run(prompt, system_prompt))


async def main():
    """Example usage"""
    # Replace with your actual API key
    API_KEY = "your-farm-key-here"
    
    logger.info("=== LLM Farm Pydantic AI Demo ===\n")
    
    # Initialize agent
    agent = LLMFarmAgent(api_key=API_KEY)
    
    # Test prompts
    prompts = [
        "Tell me about Bosch group in 2 sentences",
        "What are the main products of Bosch?",
        "Tell me a short joke"
    ]
    
    # Example 1: Regular run
    print("\n--- Regular Responses ---")
    for prompt in prompts:
        try:
            result = await agent.run(prompt)
            print(f"\nQ: {prompt}")
            print(f"A: {result}")
        except Exception as e:
            logger.error(f"Failed: {e}")
    
    # Example 2: Streaming response
    print("\n\n--- Streaming Response ---")
    print("Q: Tell me a fun fact about AI")
    print("A: ", end="", flush=True)
    try:
        async for chunk in agent.run_stream("Tell me a fun fact about AI"):
            if isinstance(chunk, str):
                print(chunk, end="", flush=True)
        print("\n")
    except Exception as e:
        logger.error(f"Failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
