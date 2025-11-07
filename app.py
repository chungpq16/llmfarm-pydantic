import asyncio
import logging
import httpx
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for troubleshooting
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enable httpx debug logging only when needed
# logging.getLogger("httpx").setLevel(logging.DEBUG)


async def log_request(request: httpx.Request):
    """Log HTTP request details"""
    logger.debug("=" * 80)
    logger.debug("HTTP REQUEST:")
    logger.debug(f"Method: {request.method}")
    logger.debug(f"URL: {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    if request.content:
        logger.debug(f"Body: {request.content.decode('utf-8', errors='ignore')[:1000]}")
    logger.debug("=" * 80)


async def log_response(response: httpx.Response):
    """Log HTTP response details"""
    logger.debug("=" * 80)
    logger.debug("HTTP RESPONSE:")
    logger.debug(f"Status: {response.status_code} {response.reason_phrase}")
    logger.debug(f"Headers: {dict(response.headers)}")
    # Note: Can't access response.text here as it's streaming
    # The body will be consumed by the OpenAI client
    logger.debug("=" * 80)


class LLMFarmAgent:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize LLM Farm Agent with Pydantic AI"""
        logger.info(f"Initializing LLM Farm Agent with model: {model}")
        
        # Configure AsyncOpenAI client for LLM Farm
        # IMPORTANT: base_url must end with / - OpenAI SDK will append chat/completions
        # Working URL pattern: base_url + "chat/completions" + "?api-version=..."
        http_client = httpx.AsyncClient(
            event_hooks={
                'request': [log_request],
                'response': [log_response]
            }
        )
        
        self.client = AsyncOpenAI(
            base_url="https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18/",
            api_key="dummy",  # LLM Farm doesn't use standard API key
            default_headers={
                "genaiplatform-farm-subscription-key": api_key
            },
            default_query={"api-version": "2024-08-01-preview"},
            http_client=http_client
        )
        logger.info(f"AsyncOpenAI client configured with base_url: {self.client.base_url}")
        
        # Wrap in PydanticAI OpenAI model
        # Use the model name - it won't be added to URL since deployment is already in base_url
        self.model = OpenAIChatModel(
            model_name=model,
            provider=OpenAIProvider(openai_client=self.client),
        )
        logger.info("OpenAIChatModel provider created")
        
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
            logger.info(f"✓ Agent completed successfully, response length: {len(result.data) if result.data else 0}")
            return result.data
        except Exception as e:
            logger.error("=" * 80)
            logger.error("ERROR DETAILS:")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            logger.error("=" * 80)
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
