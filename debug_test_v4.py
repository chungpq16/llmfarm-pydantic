import logging
import asyncio
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable OpenAI and httpx debug logging
logging.getLogger("openai").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)

class LLMFarmPydantic:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.logger = logging.getLogger(__name__)
        
        # Log the configuration
        self.logger.info(f"Initializing LLM Farm with model: {model}")
        
        # SOLUTION: Include the FULL URL with /chat/completions AND api-version
        # This bypasses the OpenAI client's URL construction completely
        base_url = "https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18/chat/completions?api-version=2024-08-01-preview"
        
        self.logger.info(f"Base URL: {base_url}")
        
        # Create AsyncOpenAI client with the complete URL
        try:
            client = AsyncOpenAI(
                api_key="secrets",  # Replace with your actual API key
                base_url=base_url,
                default_headers={
                    "genaiplatform-farm-subscription-key": "my-farm-key",  # Replace with your actual key
                    "Content-Type": "application/json"
                }
            )
            self.logger.info("AsyncOpenAI client created successfully")
        except Exception as e:
            self.logger.error(f"Failed to create AsyncOpenAI client: {e}")
            raise
        
        # Create provider with the custom client
        try:
            provider = OpenAIProvider(openai_client=client)
            self.logger.info("OpenAIProvider created successfully")
            self.logger.info(f"Provider base URL: {provider.base_url}")
        except Exception as e:
            self.logger.error(f"Failed to create OpenAIProvider: {e}")
            raise
        
        # Create the model
        try:
            self.model_instance = OpenAIChatModel(self.model, provider=provider)
            self.logger.info(f"OpenAIChatModel created with model name: {self.model}")
        except Exception as e:
            self.logger.error(f"Failed to create OpenAIChatModel: {e}")
            raise
        
        # Create the agent
        try:
            self.agent = Agent(self.model_instance)
            self.logger.info("Agent created successfully")
        except Exception as e:
            self.logger.error(f"Failed to create Agent: {e}")
            raise
    
    def completion(self, usertext, sysprompt="You are a helpful assistant"):
        """
        Generate completion using PydanticAI Agent
        """
        self.logger.info(f"Starting completion - User text: {usertext[:100]}...")
        self.logger.info(f"System prompt: {sysprompt}")
        
        try:
            # Use system prompt if provided
            if sysprompt != "You are a helpful assistant":
                # Create agent with custom system prompt
                agent_with_prompt = Agent(
                    self.model_instance, 
                    system_prompt=sysprompt
                )
                self.logger.info("Created agent with custom system prompt")
                result = agent_with_prompt.run_sync(usertext)
            else:
                self.logger.info("Using default agent")
                result = self.agent.run_sync(usertext)
            
            self.logger.info("Completion successful")
            self.logger.debug(f"Result: {result.output}")
            return result.output
            
        except Exception as e:
            self.logger.error(f"Completion failed: {e}")
            self.logger.error(f"Exception type: {type(e)}")
            
            # Log additional debug info for HTTP errors
            if hasattr(e, 'status_code'):
                self.logger.error(f"HTTP Status Code: {e.status_code}")
            if hasattr(e, 'body'):
                self.logger.error(f"Response Body: {e.body}")
            if hasattr(e, 'model_name'):
                self.logger.error(f"Model Name: {e.model_name}")
                
            raise

if __name__ == "__main__":
    print("=== LLM Farm PydanticAI Debug Test (Full URL Version) ===")
    print("IMPORTANT: Replace 'my-farm-key' and 'secrets' with actual values!")
    
    try:
        # Create instance
        print("Creating LLM Farm instance...")
        llm_farm = LLMFarmPydantic()
        print("LLM Farm instance created successfully")
        
        # Test completion
        prompt = "test"  # Using same simple prompt as in curl command
        print(f"\nTesting completion with prompt: {prompt}")
        response = llm_farm.completion(prompt, "You are a helpful assistant")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print(f"Error type: {type(e)}")
        
        # Print detailed error info
        if hasattr(e, 'status_code'):
            print(f"HTTP Status Code: {e.status_code}")
        if hasattr(e, 'body'):
            print(f"Response Body: {e.body}")
        if hasattr(e, 'model_name'):
            print(f"Model Name: {e.model_name}")
            
        print("\n=== DEBUGGING HINTS ===")
        print("1. Make sure to replace 'my-farm-key' with your actual subscription key")
        print("2. Make sure to replace 'secrets' with your actual API key/token")
        print("3. Verify your farm URL is correct")
        print("4. Check if you need to be on VPN to access the farm")