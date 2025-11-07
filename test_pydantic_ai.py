"""
Test script ONLY for PydanticAI completion method - NO FALLBACKS!
Attempts to fix the URL issue by using the complete URL with api-version
"""
import logging
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class PydanticAIOnlyClient:
    """
    Client that ONLY uses PydanticAI - attempts to fix URL issue
    """
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        logger.info(f"Creating PydanticAI-only client with model: {model}")
        
        # Try different URL configurations to fix the API version issue
        self._try_different_configurations()
    
    def _try_different_configurations(self):
        """Try different URL configurations to make PydanticAI work"""
        
        # Configuration 1: Include api-version in base URL
        print("\n🔧 Trying Configuration 1: api-version in base URL")
        try:
            base_url_with_version = "https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18?api-version=2024-08-01-preview"
            
            client1 = AsyncOpenAI(
                api_key="secrets",
                base_url=base_url_with_version,
                default_headers={"genaiplatform-farm-subscription-key": "my-farm-key"}
            )
            
            provider1 = OpenAIProvider(openai_client=client1)
            model1 = OpenAIChatModel(self.model, provider=provider1)
            self.agent1 = Agent(model1)
            
            print("✅ Configuration 1 created successfully")
            self.config1_ready = True
        except Exception as e:
            print(f"❌ Configuration 1 failed: {e}")
            self.config1_ready = False
        
        # Configuration 2: Use full chat/completions URL with api-version
        print("\n� Trying Configuration 2: Full URL with /chat/completions and api-version")
        try:
            full_url = "https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18/chat/completions?api-version=2024-08-01-preview"
            
            client2 = AsyncOpenAI(
                api_key="secrets",
                base_url=full_url,
                default_headers={"genaiplatform-farm-subscription-key": "my-farm-key"}
            )
            
            provider2 = OpenAIProvider(openai_client=client2)
            model2 = OpenAIChatModel(self.model, provider=provider2)
            self.agent2 = Agent(model2)
            
            print("✅ Configuration 2 created successfully")
            self.config2_ready = True
        except Exception as e:
            print(f"❌ Configuration 2 failed: {e}")
            self.config2_ready = False
    
    def test_pydantic_ai_only(self):
        """Test PydanticAI ONLY - no fallbacks!"""
        print("\n" + "="*50)
        print("🎯 TESTING PYDANTIC AI ONLY - NO FALLBACKS!")
        print("="*50)
        
        prompt = "Hello, how are you?"
        
        if self.config1_ready:
            print(f"\n🔄 Testing Configuration 1 with prompt: '{prompt}'")
            try:
                result1 = self.agent1.run_sync(prompt)
                print(f"✅ Configuration 1 SUCCESS: {result1.output}")
                return  # Success! No need to try other configs
            except Exception as e:
                print(f"❌ Configuration 1 failed: {e}")
                print(f"Error type: {type(e).__name__}")
        
        if self.config2_ready:
            print(f"\n🔄 Testing Configuration 2 with prompt: '{prompt}'")
            try:
                result2 = self.agent2.run_sync(prompt)
                print(f"✅ Configuration 2 SUCCESS: {result2.output}")
                return  # Success!
            except Exception as e:
                print(f"❌ Configuration 2 failed: {e}")
                print(f"Error type: {type(e).__name__}")
        
        print("\n💥 ALL PYDANTIC AI CONFIGURATIONS FAILED!")
        print("The URL/api-version issue prevents PydanticAI from working with Bosch Farm")

def test_pydantic_ai_completion():
    """Test ONLY PydanticAI completion - NO OTHER METHODS!"""
    print("=== PYDANTIC AI ONLY TEST ===")
    print("IMPORTANT: Replace 'my-farm-key' and 'secrets' with actual values!")
    print("This test will NOT use direct API calls - PydanticAI only!")
    
    try:
        client = PydanticAIOnlyClient()
        client.test_pydantic_ai_only()
        
    except Exception as e:
        print(f"❌ Failed to create PydanticAI client: {e}")
        print(f"Error type: {type(e).__name__}")
        
        print("\n=== ROOT CAUSE ANALYSIS ===")
        print("PydanticAI doesn't support extra_query parameters")
        print("The Bosch Farm requires ?api-version=2024-08-01-preview")
        print("This is why direct OpenAI calls work but PydanticAI fails")

if __name__ == "__main__":
    test_pydantic_ai_completion()