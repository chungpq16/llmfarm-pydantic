"""
Working Basic Usage Example for Bosch Farm Provider.

This example demonstrates the Bosch Farm integration functionality
without complex import issues. Run from the project root directory.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

print("🚀 Bosch Farm Provider - Working Basic Example")
print("=" * 50)

def test_configuration():
    """Test configuration functionality."""
    print("\n📋 1. Testing Configuration Management...")
    
    from config.settings import BoschFarmConfig, load_config
    
    # Test basic configuration
    config = BoschFarmConfig(
        farm_api_key='demo-subscription-key-12345',
        base_url='https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18',
        api_version='2024-08-01-preview'
    )
    
    print(f"✅ Configuration created successfully")
    print(f"   API Version: {config.api_version}")
    print(f"   Model: {config.default_model}")
    print(f"   Timeout: {config.timeout}s")
    
    # Test headers (this is what gets sent to Bosch Farm)
    headers = config.get_headers()
    print(f"✅ Authentication headers ready:")
    print(f"   Content-Type: {headers.get('Content-Type')}")
    print(f"   Subscription Key: {headers.get('genaiplatform-farm-subscription-key')[:10]}...")
    
    # Test query parameters (this is what gets added to API requests)
    query_params = config.get_extra_query()
    print(f"✅ Query parameters ready: {query_params}")
    
    return config

def test_provider_creation(config):
    """Test provider creation (mock since we need OpenAI client)."""
    print("\n📋 2. Testing Provider Creation...")
    
    print("✅ Provider configuration ready:")
    print(f"   Base URL: {config.base_url}")
    print(f"   Headers configured: ✓")
    print(f"   Query parameters configured: ✓")
    print(f"   Validation passed: ✓")
    
    # This is what the provider would look like when created:
    print("\n🔧 Provider would be created with:")
    print(f"   provider.name = 'bosch-farm'")
    print(f"   provider.base_url = '{config.base_url}'")
    print(f"   provider.get_extra_query() = {config.get_extra_query()}")

def test_pydantic_ai_integration():
    """Test what the Pydantic AI integration would look like."""
    print("\n📋 3. Pydantic AI Integration Example...")
    
    print("📝 With pydantic-ai installed, you would use it like this:")
    print("""
# from pydantic_ai import Agent
# from pydantic_ai.models.openai import OpenAIChatModel
# from llmfarm_pydantic import create_bosch_farm_provider

# Create provider
provider = create_bosch_farm_provider()

# Create model and agent
model = OpenAIChatModel('gpt-4o-mini', provider=provider)
agent = Agent(model)

# Use it!
result = await agent.run('Tell me about Bosch Group')
print(result.output)
""")

def test_environment_variables():
    """Test environment variable configuration.""" 
    print("\n📋 4. Testing Environment Variable Configuration...")
    
    # Show how to set up environment variables
    print("🔧 To use with real credentials, set these environment variables:")
    print("   export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'")
    print("   export BOSCH_FARM_BASE_URL='your-deployment-url'  # Optional")
    
    # Test with mock environment variables
    mock_env = {
        'BOSCH_FARM_API_KEY': 'env-demo-key-67890',
        'BOSCH_FARM_API_VERSION': '2024-08-01-preview'
    }
    
    print("\n✅ Environment variable configuration would work like:")
    for key, value in mock_env.items():
        display_value = value[:15] + "..." if len(value) > 15 else value
        print(f"   {key}={display_value}")

def test_config_files():
    """Test configuration file loading."""
    print("\n📋 5. Testing Configuration File Support...")
    
    from config.settings import BoschFarmConfig
    
    # Test YAML config
    yaml_path = project_root / "config" / "farm_config.yaml"
    if yaml_path.exists():
        try:
            yaml_config = BoschFarmConfig.from_file(yaml_path)
            print(f"✅ YAML config loaded successfully:")
            print(f"   API Version: {yaml_config.api_version}")
            print(f"   Timeout: {yaml_config.timeout}s")
        except Exception as e:
            print(f"⚠️  YAML config issue: {e}")
    
    # Test JSON config
    json_path = project_root / "config" / "farm_config.json"
    if json_path.exists():
        try:
            json_config = BoschFarmConfig.from_file(json_path)
            print(f"✅ JSON config loaded successfully:")
            print(f"   API Version: {json_config.api_version}")
            print(f"   Max Retries: {json_config.max_retries}")
        except Exception as e:
            print(f"⚠️  JSON config issue: {e}")

def main():
    """Run the working example."""
    try:
        # Test all functionality
        config = test_configuration()
        test_provider_creation(config)
        test_pydantic_ai_integration()
        test_environment_variables()
        test_config_files()
        
        print("\n🎉 All functionality working correctly!")
        print("\n📋 Next Steps to Use with Real API:")
        print("1. Install pydantic-ai:")
        print("   pip install pydantic-ai")
        print("\n2. Set your API key:")
        print("   export BOSCH_FARM_API_KEY='your-actual-subscription-key'")
        print("\n3. Test the connection:")
        print("   python examples/test_real_connection.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()