"""
Basic usage example for Bosch Farm Provider with Pydantic AI.

This example demonstrates the simplest way to use the Bosch Farm integration
using environment variables for configuration.
"""

import os
import asyncio
from pathlib import Path
import sys

# Add the src directory to the Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import Pydantic AI components
try:
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    PYDANTIC_AI_AVAILABLE = True
except ImportError:
    PYDANTIC_AI_AVAILABLE = False
    print("Warning: pydantic-ai not installed. This example shows the code structure but won't run.")

# Import our Bosch Farm provider
from llmfarm_pydantic import BoschFarmProvider, create_bosch_farm_provider


def setup_environment_variables():
    """
    Set up environment variables for demo purposes.
    In production, these should be set in your environment.
    """
    # Required: Your Bosch Farm subscription key
    if not os.getenv("BOSCH_FARM_API_KEY"):
        print("⚠️  Please set BOSCH_FARM_API_KEY environment variable")
        print("   export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'")
        return False
    
    # Optional: Custom base URL (uses default if not set)
    if not os.getenv("BOSCH_FARM_BASE_URL"):
        print("ℹ️  Using default Bosch Farm base URL")
    
    return True


async def basic_chat_example():
    """Example of basic chat functionality with Bosch Farm."""
    
    if not PYDANTIC_AI_AVAILABLE:
        print("📝 Example code (requires pydantic-ai installation):")
        print("""
# Create the provider using environment variables
provider = create_bosch_farm_provider()

# Create a chat model with the provider
model = OpenAIChatModel('gpt-4o-mini', provider=provider)

# Create an agent
agent = Agent(model)

# Run a simple conversation
result = await agent.run('Tell me about Bosch Group')
print(result.output)
""")
        return
    
    try:
        # Create the provider using environment variables
        provider = create_bosch_farm_provider()
        print(f"✅ Created provider: {provider}")
        
        # Create a chat model with the provider
        model = OpenAIChatModel('gpt-4o-mini', provider=provider)
        print(f"✅ Created model with base URL: {provider.base_url}")
        
        # Create an agent
        agent = Agent(model)
        print("✅ Created agent")
        
        # Run a simple conversation
        print("\n🤖 Running conversation...")
        result = await agent.run('Tell me a short fact about Bosch Group')
        print(f"\n📝 Response: {result.output}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your BOSCH_FARM_API_KEY is set correctly")


async def advanced_provider_example():
    """Example of advanced provider configuration."""
    
    try:
        # Create provider with explicit parameters
        provider = BoschFarmProvider(
            farm_api_key=os.getenv("BOSCH_FARM_API_KEY"),
            api_version="2024-08-01-preview"
        )
        
        print(f"✅ Advanced provider created: {provider}")
        print(f"   Extra query params: {provider.get_extra_query()}")
        
        if PYDANTIC_AI_AVAILABLE:
            model = OpenAIChatModel('gpt-4o-mini', provider=provider)
            agent = Agent(model)
            
            result = await agent.run('What is artificial intelligence?')
            print(f"📝 AI Response: {result.output}")
        
    except Exception as e:
        print(f"❌ Error in advanced example: {e}")


def main():
    """Main function to run the examples."""
    print("🚀 Bosch Farm Provider - Basic Usage Example")
    print("=" * 50)
    
    # Check environment setup
    if not setup_environment_variables():
        return
    
    # Run the examples
    print("\n📋 Running basic chat example...")
    asyncio.run(basic_chat_example())
    
    print("\n📋 Running advanced provider example...")
    asyncio.run(advanced_provider_example())
    
    print("\n✅ Examples completed!")


if __name__ == "__main__":
    main()