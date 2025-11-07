import logging
import asyncio
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,  # Changed to INFO to reduce noise, change to DEBUG if needed
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class LLMFarmPydanticAI:
    """
    PydanticAI wrapper for Bosch LLM Farm that mimics your original working approach
    """
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        logger.info(f"Initializing LLM Farm with model: {model}")
        
        # Use the EXACT same configuration as your original working code
        client = AsyncOpenAI(
            api_key="secrets",  # Replace with your actual API key
            base_url="https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18",
            default_headers={"genaiplatform-farm-subscription-key": "my-farm-key"}  # Replace with your key
        )
        
        # Store client for direct API calls when needed
        self._client = client
        
        # Create PydanticAI provider and model
        provider = OpenAIProvider(openai_client=client)
        self.model_instance = OpenAIChatModel(self.model, provider=provider)
        self.agent = Agent(self.model_instance)
        
        logger.info("LLM Farm PydanticAI instance created successfully")
    
    async def _direct_completion(self, usertext, sysprompt):
        """
        Direct API call using the same approach as your original code
        This bypasses PydanticAI for the actual API call but keeps the interface
        """
        messages = [
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": usertext}
        ]
        
        logger.info(f"Making direct API call with messages: {len(messages)} messages")
        
        try:
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                extra_query={"api-version": "2024-08-01-preview"}  # This is the key!
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Direct API call failed: {e}")
            raise
    
    def completion(self, usertext, sysprompt="You are a helpful assistant"):
        """
        Synchronous completion - uses direct API call for reliability
        """
        logger.info(f"Starting completion - User text: {usertext[:100]}...")
        
        try:
            # Use direct async call in sync context
            result = asyncio.run(self._direct_completion(usertext, sysprompt))
            logger.info("Completion successful")
            return result
        except Exception as e:
            logger.error(f"Completion failed: {e}")
            raise
    
    async def completion_async(self, usertext, sysprompt="You are a helpful assistant"):
        """
        Asynchronous completion - uses direct API call for reliability
        """
        logger.info(f"Starting async completion - User text: {usertext[:100]}...")
        
        try:
            result = await self._direct_completion(usertext, sysprompt)
            logger.info("Async completion successful")
            return result
        except Exception as e:
            logger.error(f"Async completion failed: {e}")
            raise
    
    def completion_with_pydantic_ai(self, usertext, sysprompt="You are a helpful assistant"):
        """
        Alternative method using full PydanticAI (may not work due to URL issues)
        """
        logger.info(f"Starting PydanticAI completion - User text: {usertext[:100]}...")
        
        try:
            if sysprompt != "You are a helpful assistant":
                agent_with_prompt = Agent(self.model_instance, system_prompt=sysprompt)
                result = agent_with_prompt.run_sync(usertext)
            else:
                result = self.agent.run_sync(usertext)
            
            logger.info("PydanticAI completion successful")
            return result.output
        except Exception as e:
            logger.error(f"PydanticAI completion failed: {e}")
            logger.warning("Try using the direct completion() method instead")
            raise

if __name__ == "__main__":
    print("=== LLM Farm PydanticAI Hybrid Solution ===")
    print("This version uses direct API calls with extra_query (like your original code)")
    print("but wraps it in a PydanticAI-compatible interface")
    print("IMPORTANT: Replace 'my-farm-key' and 'secrets' with actual values!")
    print()
    
    try:
        # Create instance
        print("Creating LLM Farm instance...")
        llm_farm = LLMFarmPydanticAI()
        print("LLM Farm instance created successfully")
        
        # Test direct completion (recommended)
        prompt = "test"
        print(f"\nTesting direct completion with prompt: {prompt}")
        response = llm_farm.completion(prompt, "You are a helpful assistant")
        print(f"Response: {response}")
        
        # Test async completion
        print(f"\nTesting async completion...")
        async def test_async():
            response = await llm_farm.completion_async(prompt, "You are a helpful assistant")
            print(f"Async Response: {response}")
        
        asyncio.run(test_async())
        
        # Optionally test PydanticAI method (may fail due to URL issues)
        print(f"\nOptionally testing PydanticAI method (may fail)...")
        try:
            response_pydantic = llm_farm.completion_with_pydantic_ai(prompt, "You are a helpful assistant")
            print(f"PydanticAI Response: {response_pydantic}")
        except Exception as e:
            print(f"PydanticAI method failed as expected: {e}")
            print("Use the direct completion() method instead")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print(f"Error type: {type(e)}")
        
        print("\n=== DEBUGGING HINTS ===")
        print("1. Make sure to replace 'my-farm-key' with your actual subscription key")
        print("2. Make sure to replace 'secrets' with your actual API key/token")
        print("3. Verify your farm URL is correct")
        print("4. Check if you need to be on VPN to access the farm")