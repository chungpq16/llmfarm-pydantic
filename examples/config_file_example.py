"""
Configuration file usage example for Bosch Farm Provider.

This example demonstrates how to use YAML and JSON configuration files
to manage Bosch Farm settings instead of environment variables.
"""

import asyncio
from pathlib import Path
import sys

# Add the src directory to the Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    PYDANTIC_AI_AVAILABLE = True
except ImportError:
    PYDANTIC_AI_AVAILABLE = False
    print("Warning: pydantic-ai not installed. This example shows the code structure.")

from llmfarm_pydantic import BoschFarmProvider, BoschFarmConfig


def create_sample_config_files():
    """Create sample configuration files for demonstration."""
    
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(exist_ok=True)
    
    # YAML configuration
    yaml_config = """
# Bosch Farm Configuration
bosch_farm:
  # API settings  
  api_version: "2024-08-01-preview"
  default_model: "gpt-4o-mini"
  
  # HTTP settings
  timeout: 30
  max_retries: 3
  
  # Note: farm_api_key and base_url should be set via environment variables
  # for security reasons, but can be included here for development
  
  # farm_api_key: "your-key-here"  # Better to use BOSCH_FARM_API_KEY env var
  # base_url: "https://aoai-farm.bosch-temp.com/api/openai/deployments/..."
"""
    
    yaml_path = config_dir / "farm_config.yaml"
    yaml_path.write_text(yaml_config)
    print(f"📄 Created sample YAML config: {yaml_path}")
    
    # JSON configuration
    json_config = """{
  "bosch_farm": {
    "api_version": "2024-08-01-preview", 
    "default_model": "gpt-4o-mini",
    "timeout": 30,
    "max_retries": 3
  }
}"""
    
    json_path = config_dir / "farm_config.json"
    json_path.write_text(json_config)
    print(f"📄 Created sample JSON config: {json_path}")
    
    return yaml_path, json_path


async def config_file_example():
    """Example using configuration file."""
    
    yaml_path, json_path = create_sample_config_files()
    
    try:
        # Load configuration from YAML file
        print("\n📋 Loading configuration from YAML file...")
        config = BoschFarmConfig.from_file(yaml_path)
        print(f"✅ Loaded config: api_version={config.api_version}, model={config.default_model}")
        
        # Create provider with config file
        provider = BoschFarmProvider(config_path=yaml_path)
        print(f"✅ Created provider from YAML config: {provider}")
        
        # Try JSON configuration
        print("\n📋 Loading configuration from JSON file...")
        json_config = BoschFarmConfig.from_file(json_path)
        print(f"✅ Loaded JSON config: timeout={json_config.timeout}, retries={json_config.max_retries}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        if "farm_api_key" in str(e):
            print("💡 Set BOSCH_FARM_API_KEY environment variable to test with actual API")


async def mixed_config_example():
    """Example using both config file and environment variables."""
    
    yaml_path, _ = create_sample_config_files()
    
    try:
        # This loads from both file and environment variables
        # Environment variables take precedence
        print("\n📋 Using mixed configuration (file + environment)...")
        config = BoschFarmConfig.from_mixed(yaml_path)
        
        print(f"✅ Mixed config loaded:")
        print(f"   API Version: {config.api_version}")
        print(f"   Timeout: {config.timeout}")
        print(f"   Max Retries: {config.max_retries}")
        print(f"   Has API Key: {'Yes' if config.farm_api_key else 'No (set BOSCH_FARM_API_KEY)'}")
        
        if config.farm_api_key:
            # Create provider with mixed configuration
            provider = BoschFarmProvider(config_path=yaml_path)
            print(f"✅ Provider created with mixed config")
            
            if PYDANTIC_AI_AVAILABLE:
                model = OpenAIChatModel('gpt-4o-mini', provider=provider)
                agent = Agent(model)
                
                print("🤖 Testing with simple prompt...")
                result = await agent.run("Hello, can you confirm you're working?")
                print(f"📝 Response: {result.output}")
        else:
            print("💡 Set BOSCH_FARM_API_KEY to test actual API calls")
            
    except Exception as e:
        print(f"❌ Mixed configuration error: {e}")


def demonstrate_config_validation():
    """Demonstrate configuration validation features."""
    
    print("\n📋 Demonstrating configuration validation...")
    
    try:
        # This should fail validation (no API key)
        config = BoschFarmConfig()
        config.validate()
    except ValueError as e:
        print(f"✅ Validation correctly caught missing API key: {e}")
    
    try:
        # This should pass validation
        config = BoschFarmConfig(
            farm_api_key="test-key",
            base_url="https://test.example.com"
        )
        config.validate()
        print(f"✅ Valid configuration passed validation")
        
        # Show headers
        headers = config.get_headers()
        print(f"   Headers: {headers}")
        
        # Show query params
        query_params = config.get_extra_query()
        print(f"   Query params: {query_params}")
        
    except ValueError as e:
        print(f"❌ Unexpected validation error: {e}")


def main():
    """Main function to run configuration examples."""
    print("📁 Bosch Farm Provider - Configuration File Example")
    print("=" * 55)
    
    # Run configuration examples
    print("📋 Creating and loading configuration files...")
    asyncio.run(config_file_example())
    
    print("\n📋 Testing mixed configuration approach...")
    asyncio.run(mixed_config_example())
    
    print("\n📋 Demonstrating configuration validation...")
    demonstrate_config_validation()
    
    print("\n✅ Configuration examples completed!")
    print("\n💡 Tips:")
    print("   - Store sensitive data (API keys) in environment variables")
    print("   - Use config files for non-sensitive settings")
    print("   - Environment variables override config file values")


if __name__ == "__main__":
    main()