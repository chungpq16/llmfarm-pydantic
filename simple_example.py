#!/usr/bin/env python3
"""
Simple example using the direct Bosch Farm LLM interface.
Based on the llmfarminf concept for easy usage.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bosch_farm_simple import BoschFarmLLM, llmfarminf


def example_basic_usage():
    """Basic usage example matching the original llmfarminf pattern."""
    
    print("📋 Example 1: Basic Usage (llmfarminf style)")
    print("-" * 50)
    
    # Create client (using the alias for backward compatibility)
    obj = llmfarminf()
    
    # Ask a question
    prompt = "Tell me about Bosch Group"
    response = obj._completion(prompt, "You are a helpful assistant")
    
    print(f"Question: {prompt}")
    print(f"Response: {response}")
    
    return True


def example_with_configuration():
    """Example with explicit configuration."""
    
    print("\n📋 Example 2: With Custom Configuration")
    print("-" * 50)
    
    # Create client with explicit parameters
    llm = BoschFarmLLM(
        model="askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18",
        farm_api_key=os.getenv("BOSCH_FARM_API_KEY"),
        api_version="2024-08-01-preview"
    )
    
    # Use convenience methods
    question = "What are the main business areas of Bosch?"
    answer = llm.ask(question)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    
    return True


def example_chat_interface():
    """Example using the chat interface with custom system prompt."""
    
    print("\n📋 Example 3: Chat Interface")
    print("-" * 50)
    
    llm = BoschFarmLLM()
    
    # Chat with custom system prompt
    response = llm.chat(
        "How does Bosch contribute to sustainability?",
        "You are an expert on Bosch's environmental and sustainability initiatives"
    )
    
    print(f"Chat response: {response}")
    
    return True


def main():
    """Run all examples."""
    
    print("🚀 Bosch Farm Simple LLM - Examples")
    print("=" * 60)
    
    # Check environment
    api_key = os.getenv("BOSCH_FARM_API_KEY")
    if not api_key:
        print("❌ BOSCH_FARM_API_KEY not set!")
        print("\nTo run these examples, set your API key:")
        print("export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'")
        print("\nOptionally, set custom base URL:")
        print("export BOSCH_FARM_BASE_URL='https://your-custom-deployment-url'")
        return False
    
    print(f"✅ API key configured: {api_key[:10]}...")
    
    base_url = os.getenv("BOSCH_FARM_BASE_URL")
    if base_url:
        print(f"✅ Custom base URL: {base_url}")
    else:
        print("ℹ️  Using default deployment URL")
    
    try:
        # Run examples
        example_basic_usage()
        example_with_configuration()
        example_chat_interface()
        
        print("\n🎉 All examples completed successfully!")
        print("\n💡 Key features:")
        print("  ✅ Simple direct interface (no Pydantic AI required)")
        print("  ✅ Environment variable configuration")
        print("  ✅ Custom headers for Bosch Farm authentication")
        print("  ✅ Multiple convenience methods (ask, chat, _completion)")
        print("  ✅ Backward compatible with llmfarminf naming")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print(f"Error type: {type(e).__name__}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)