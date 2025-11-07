"""
Advanced usage example for Bosch Farm Provider with Pydantic AI.

This example demonstrates advanced features including:
- Custom HTTP clients
- Error handling
- Custom model settings  
- Integration with Pydantic models for structured output
"""

import asyncio
import httpx
from pathlib import Path
import sys
from typing import Optional
from pydantic import BaseModel

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


# Example Pydantic models for structured output
class CompanyInfo(BaseModel):
    """Model for company information."""
    name: str
    founded_year: int
    headquarters: str
    industry: str
    brief_description: str


class TechnicalSolution(BaseModel):
    """Model for technical solutions."""
    problem: str
    solution: str
    technologies: list[str]
    complexity_level: str  # "low", "medium", "high"


async def custom_http_client_example():
    """Example using custom HTTP client configuration."""
    
    print("\n📋 Custom HTTP Client Example")
    print("-" * 40)
    
    try:
        # Create custom HTTP client with specific settings
        custom_client = httpx.AsyncClient(
            timeout=60.0,  # Longer timeout
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10
            ),
            follow_redirects=True,
            verify=True  # SSL verification
        )
        
        # Create provider with custom client
        provider = BoschFarmProvider(
            http_client=custom_client,
            farm_api_key=None  # Will use environment variable
        )
        
        print(f"✅ Created provider with custom HTTP client: {provider}")
        
        if PYDANTIC_AI_AVAILABLE:
            model = OpenAIChatModel('gpt-4o-mini', provider=provider)
            agent = Agent(model)
            
            result = await agent.run("Explain HTTP clients in simple terms")
            print(f"📝 Response: {result.output[:200]}...")
        
        # Don't forget to close the client
        await custom_client.aclose()
        print("✅ Custom HTTP client closed")
        
    except Exception as e:
        print(f"❌ Custom client error: {e}")


async def structured_output_example():
    """Example using Pydantic models for structured output."""
    
    print("\n📋 Structured Output Example") 
    print("-" * 35)
    
    if not PYDANTIC_AI_AVAILABLE:
        print("📝 Example code (requires pydantic-ai):")
        print("""
# Create agent with structured output
agent = Agent(model, output_type=CompanyInfo)

# Get structured response
result = await agent.run(
    "Tell me about Bosch company including founded year, headquarters, industry and brief description"
)

print(f"Company: {result.output.name}")
print(f"Founded: {result.output.founded_year}")
print(f"HQ: {result.output.headquarters}")
""")
        return
    
    try:
        provider = BoschFarmProvider()
        model = OpenAIChatModel('gpt-4o-mini', provider=provider)
        
        # Create agent with structured output
        agent = Agent(model, output_type=CompanyInfo)
        
        print("🤖 Requesting structured company information...")
        result = await agent.run(
            "Tell me about Bosch company including founded year, headquarters, industry and brief description"
        )
        
        company = result.output
        print(f"✅ Structured response received:")
        print(f"   Company: {company.name}")
        print(f"   Founded: {company.founded_year}")
        print(f"   Headquarters: {company.headquarters}")
        print(f"   Industry: {company.industry}")
        print(f"   Description: {company.brief_description}")
        
    except Exception as e:
        print(f"❌ Structured output error: {e}")


async def error_handling_example():
    """Example demonstrating proper error handling."""
    
    print("\n📋 Error Handling Example")
    print("-" * 30)
    
    try:
        # Try to create provider with invalid configuration
        print("🧪 Testing invalid configuration...")
        
        try:
            provider = BoschFarmProvider(farm_api_key="")  # Empty key
            print("❌ Should have failed with empty API key")
        except ValueError as e:
            print(f"✅ Correctly caught empty API key error: {e}")
        
        # Try to create provider without any credentials
        print("\n🧪 Testing missing credentials...")
        try:
            # Temporarily clear environment variable for test
            import os
            original_key = os.environ.get('BOSCH_FARM_API_KEY')
            if 'BOSCH_FARM_API_KEY' in os.environ:
                del os.environ['BOSCH_FARM_API_KEY']
            
            provider = BoschFarmProvider()
            print("❌ Should have failed with missing API key")
            
        except ValueError as e:
            print(f"✅ Correctly caught missing credentials error: {e}")
        finally:
            # Restore environment variable
            if original_key:
                os.environ['BOSCH_FARM_API_KEY'] = original_key
        
        # Test network error handling (with mock)
        print("\n🧪 Testing network error handling...")
        if PYDANTIC_AI_AVAILABLE:
            try:
                # Create provider with invalid base URL
                provider = BoschFarmProvider(
                    base_url="https://invalid-url-that-does-not-exist.com",
                    farm_api_key="test-key"
                )
                model = OpenAIChatModel('gpt-4o-mini', provider=provider)
                agent = Agent(model)
                
                # This should fail with network error
                result = await agent.run("test", timeout=5)
                print("❌ Should have failed with network error")
                
            except Exception as e:
                print(f"✅ Correctly caught network error: {type(e).__name__}")
        
    except Exception as e:
        print(f"❌ Unexpected error in error handling test: {e}")


async def performance_example():
    """Example demonstrating performance considerations."""
    
    print("\n📋 Performance Example")
    print("-" * 25)
    
    try:
        # Create provider with performance optimizations
        provider = BoschFarmProvider(
            farm_api_key=None,  # Use env var
            config_path=Path(__file__).parent.parent / "config" / "farm_config.yaml"
        )
        
        print(f"✅ Provider created with optimizations")
        print(f"   Base URL: {provider.base_url}")
        print(f"   Extra query: {provider.get_extra_query()}")
        
        if PYDANTIC_AI_AVAILABLE:
            model = OpenAIChatModel('gpt-4o-mini', provider=provider)
            
            # Multiple agents can share the same provider/model
            agents = [
                Agent(model, output_type=str) for _ in range(3)
            ]
            
            print(f"✅ Created {len(agents)} agents sharing the same model")
            
            # Concurrent requests (if API key is available)
            if provider.config.farm_api_key and provider.config.farm_api_key != "dummy":
                print("🤖 Testing concurrent requests...")
                tasks = [
                    agent.run(f"Count to {i+1}") 
                    for i, agent in enumerate(agents)
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        print(f"   Agent {i+1}: Error - {result}")
                    else:
                        print(f"   Agent {i+1}: Success - {len(result.output)} chars")
            else:
                print("💡 Set BOSCH_FARM_API_KEY to test concurrent requests")
        
    except Exception as e:
        print(f"❌ Performance example error: {e}")


def main():
    """Main function to run advanced examples."""
    print("🚀 Bosch Farm Provider - Advanced Usage Examples")
    print("=" * 55)
    
    # Run all advanced examples
    asyncio.run(custom_http_client_example())
    asyncio.run(structured_output_example()) 
    asyncio.run(error_handling_example())
    asyncio.run(performance_example())
    
    print("\n✅ Advanced examples completed!")
    print("\n💡 Advanced Tips:")
    print("   - Use custom HTTP clients for specific timeout/connection requirements")
    print("   - Leverage Pydantic models for structured LLM output")
    print("   - Implement proper error handling for production use")
    print("   - Share provider/model instances across agents for better performance")
    print("   - Monitor API usage and implement rate limiting if needed")


if __name__ == "__main__":
    main()