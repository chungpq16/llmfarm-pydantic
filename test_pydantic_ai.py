"""
Test script specifically for the completion_with_pydantic_ai method
"""
import asyncio
from llm_farm_hybrid import LLMFarmPydanticAI

def test_pydantic_ai_completion():
    """Test the PydanticAI completion method specifically"""
    print("=== Testing PydanticAI Completion Method ===")
    print("IMPORTANT: Make sure to replace 'my-farm-key' and 'secrets' with actual values!")
    print()
    
    try:
        # Create instance
        print("Creating LLM Farm instance...")
        llm_farm = LLMFarmPydanticAI()
        print("✅ LLM Farm instance created successfully")
        
        # Test with default system prompt
        print("\n🔄 Testing PydanticAI method with default system prompt...")
        prompt = "Hello, how are you?"
        
        try:
            response = llm_farm.completion_with_pydantic_ai(prompt)
            print(f"✅ PydanticAI Response: {response}")
        except Exception as e:
            print(f"❌ PydanticAI method failed: {e}")
            print(f"Error type: {type(e).__name__}")
            
        # Test with custom system prompt
        print("\n🔄 Testing PydanticAI method with custom system prompt...")
        custom_prompt = "You are a helpful coding assistant."
        
        try:
            response = llm_farm.completion_with_pydantic_ai(prompt, custom_prompt)
            print(f"✅ PydanticAI Response with custom prompt: {response}")
        except Exception as e:
            print(f"❌ PydanticAI method with custom prompt failed: {e}")
            print(f"Error type: {type(e).__name__}")
        
        # Compare with working direct method for reference
        print("\n📊 Comparing with direct method (for reference)...")
        try:
            direct_response = llm_farm.completion(prompt)
            print(f"✅ Direct method response: {direct_response}")
        except Exception as e:
            print(f"❌ Direct method also failed: {e}")
            
    except Exception as e:
        print(f"❌ Failed to create LLM Farm instance: {e}")
        print(f"Error type: {type(e).__name__}")
        
        print("\n=== TROUBLESHOOTING TIPS ===")
        print("1. Check your API credentials")
        print("2. Verify you're on the right network/VPN")
        print("3. Ensure the farm URL is accessible")

if __name__ == "__main__":
    test_pydantic_ai_completion()