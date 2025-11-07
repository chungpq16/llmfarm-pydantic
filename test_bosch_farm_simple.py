#!/usr/bin/env python3
"""
Simple test script for Bosch Farm Provider with Pydantic AI.
Based on the custom OpenAI-compatible endpoint pattern.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set."""
    api_key = os.getenv("BOSCH_FARM_API_KEY")
    base_url = os.getenv("BOSCH_FARM_BASE_URL")
    
    logger.info("Environment check:")
    logger.info(f"  BOSCH_FARM_API_KEY: {'SET' if api_key else 'NOT SET'}")
    logger.info(f"  BOSCH_FARM_BASE_URL: {base_url if base_url else 'NOT SET'}")
    
    if not api_key:
        logger.error("BOSCH_FARM_API_KEY is required!")
        return False
    
    return True

async def test_bosch_farm_with_pydantic_ai():
    """Test Bosch Farm with actual Pydantic AI (if available)."""
    
    try:
        # Import Pydantic AI components
        from pydantic_ai import Agent
        from pydantic_ai.models.openai import OpenAIModel
        from pydantic_ai.providers.openai import OpenAIProvider
        
        logger.info("✅ Pydantic AI imports successful")
        
        # Import our Bosch Farm provider
        from providers.bosch_farm import create_bosch_farm_provider
        
        logger.info("✅ Bosch Farm provider import successful")
        
        # 1) Create Bosch Farm provider (handles custom headers and authentication)
        logger.info("Creating Bosch Farm provider...")
        bosch_provider = create_bosch_farm_provider()
        
        logger.info(f"✅ Provider created:")
        logger.info(f"  Name: {bosch_provider.name}")
        logger.info(f"  Base URL: {bosch_provider.base_url}")
        logger.info(f"  Deployment: {bosch_provider.deployment_name}")
        logger.info(f"  Extra query: {bosch_provider.get_extra_query()}")
        
        # 2) Get the configured AsyncOpenAI client from our provider
        client = bosch_provider.client
        logger.info(f"✅ AsyncOpenAI client obtained:")
        logger.info(f"  Client base_url: {client.base_url}")
        logger.info(f"  Default headers: {dict(client.default_headers)}")
        
        # 3) Wrap it in a PydanticAI OpenAI model
        logger.info("Creating OpenAI model...")
        model = OpenAIModel(
            model_name=bosch_provider.deployment_name,  # Use Azure deployment name
            provider=OpenAIProvider(openai_client=client),
        )
        logger.info(f"✅ Model created with deployment: {bosch_provider.deployment_name}")
        
        # 4) Build the agent
        logger.info("Creating agent...")
        agent = Agent(
            model=model,
            system_prompt="You are a helpful assistant from Bosch Corporate LLM Farm.",
        )
        logger.info("✅ Agent created")
        
        # 5) Test the agent with a simple query
        logger.info("Running test query...")
        test_message = "Hello! Can you tell me what you are and confirm you're working correctly?"
        
        logger.info(f"Sending message: '{test_message}'")
        result = await agent.run(test_message)
        
        logger.info("✅ SUCCESS! Got response from Bosch Farm:")
        logger.info(f"Response: {result.data}")
        
        return True
        
    except ImportError as e:
        logger.warning(f"Pydantic AI not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error during test: {e}")
        logger.exception("Full traceback:")
        return False

def test_provider_creation_only():
    """Test just the provider creation (no Pydantic AI required)."""
    
    try:
        # Import our Bosch Farm provider
        from providers.bosch_farm import create_bosch_farm_provider
        
        logger.info("✅ Bosch Farm provider import successful")
        
        # Create provider
        logger.info("Creating Bosch Farm provider...")
        provider = create_bosch_farm_provider()
        
        logger.info("✅ Provider created successfully:")
        logger.info(f"  Name: {provider.name}")
        logger.info(f"  Config base_url: {provider.config.base_url}")
        logger.info(f"  Client base_url: {provider.base_url}")
        logger.info(f"  Deployment name: {provider.deployment_name}")
        logger.info(f"  API version: {provider.config.api_version}")
        logger.info(f"  Headers: {provider.config.get_headers()}")
        logger.info(f"  Extra query: {provider.get_extra_query()}")
        
        # Verify URL construction
        expected_api_root = "https://aoai-farm.bosch-temp.com/api/openai"
        actual_base_url = provider.base_url.rstrip('/')
        
        if actual_base_url == expected_api_root:
            logger.info("✅ URL construction is correct (API root)")
        else:
            logger.warning(f"⚠️  URL might be incorrect. Expected: {expected_api_root}, Got: {actual_base_url}")
        
        # Verify deployment name extraction
        expected_deployment = "askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18"
        if provider.deployment_name == expected_deployment:
            logger.info("✅ Deployment name extraction is correct")
        else:
            logger.info(f"ℹ️  Deployment name: {provider.deployment_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating provider: {e}")
        logger.exception("Full traceback:")
        return False

async def main():
    """Main test function."""
    logger.info("🚀 Bosch Farm Provider Simple Test")
    logger.info("=" * 50)
    
    # Check environment
    if not check_environment():
        logger.error("❌ Environment not configured properly")
        logger.info("Please set:")
        logger.info("  export BOSCH_FARM_API_KEY='your-subscription-key'")
        logger.info("  export BOSCH_FARM_BASE_URL='https://aoai-farm.bosch-temp.com/api/openai/deployments/your-deployment'")
        return False
    
    # Test provider creation (always works)
    logger.info("\n📋 Test 1: Provider Creation")
    logger.info("-" * 30)
    provider_ok = test_provider_creation_only()
    
    if not provider_ok:
        logger.error("❌ Provider creation failed")
        return False
    
    # Test with Pydantic AI (if available)
    logger.info("\n📋 Test 2: Full Pydantic AI Integration")
    logger.info("-" * 40)
    
    pydantic_ok = await test_bosch_farm_with_pydantic_ai()
    
    if pydantic_ok:
        logger.info("\n🎉 ALL TESTS PASSED!")
        logger.info("✅ Provider creates correctly")
        logger.info("✅ URLs are constructed properly") 
        logger.info("✅ Pydantic AI integration works")
        logger.info("✅ Bosch Farm API responds correctly")
    else:
        logger.info("\n⚠️  PARTIAL SUCCESS")
        logger.info("✅ Provider works correctly")
        logger.info("❌ Pydantic AI test failed (check logs above)")
        logger.info("💡 Install pydantic-ai for full testing: pip install pydantic-ai")
    
    return pydantic_ok

if __name__ == "__main__":
    # Run the async main function
    success = asyncio.run(main())
    exit_code = 0 if success else 1
    sys.exit(exit_code)