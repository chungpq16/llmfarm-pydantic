import asyncio
import logging
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMFarmAgent:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize LLM Farm Agent with Pydantic AI"""
        logger.info(f"Initializing LLM Farm Agent with model: {model}")
        
        # Configure AsyncOpenAI client for LLM Farm
        # Note: base_url should NOT include deployment path - OpenAI SDK will append /chat/completions
        self.client = AsyncOpenAI(
            base_url="https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18",
            api_key="dummy",  # LLM Farm doesn't use standard API key
            default_headers={
                "genaiplatform-farm-subscription-key": api_key
            },
            default_query={"api-version": "2024-08-01-preview"}
        )
        logger.info(f"AsyncOpenAI client configured with base_url: {self.client.base_url}")
        
        # Wrap in PydanticAI OpenAI model
        # Use empty model_name since it's already in the base_url
        self.model = OpenAIModel(
            model_name="",  # Empty because deployment is in base_url
            provider=OpenAIProvider(openai_client=self.client),
        )
        logger.info("OpenAIModel provider created")
        
        # Create agent
        self.agent = Agent(
            model=self.model,
            system_prompt="You are a helpful assistant.",
        )
        logger.info("Pydantic AI Agent initialized successfully")
    
    async def run(self, prompt: str) -> str:
        """Run the agent with a prompt"""
        logger.info(f"Running agent with prompt: {prompt[:50]}...")
        try:
            result = await self.agent.run(prompt)
            logger.info("Agent execution completed successfully")
            logger.debug(f"Result type: {type(result)}")
            return result.data
        except Exception as e:
            logger.error(f"Error during agent execution: {str(e)}", exc_info=True)
            raise
    
    def run_sync(self, prompt: str) -> str:
        """Synchronous wrapper for run"""
        logger.info(f"Running agent synchronously with prompt: {prompt[:50]}...")
        return asyncio.run(self.run(prompt))


async def main():
    """Example usage"""
    # Replace with your actual API key
    API_KEY = "your-farm-key-here"
    
    logger.info("=== Starting LLM Farm Pydantic AI Demo ===")
    
    # Initialize agent
    agent = LLMFarmAgent(api_key=API_KEY)
    
    # Test prompts
    prompts = [
        "Tell me about Bosch group",
        "What are the main products of Bosch?",
        "Tell me a short joke"
    ]
    
    for prompt in prompts:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing prompt: {prompt}")
        logger.info(f"{'='*60}")
        try:
            result = await agent.run(prompt)
            print(f"\nPrompt: {prompt}")
            print(f"Response: {result}\n")
        except Exception as e:
            logger.error(f"Failed to process prompt: {e}")


if __name__ == "__main__":
    asyncio.run(main())
