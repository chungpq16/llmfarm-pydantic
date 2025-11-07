"""
Test script for the production-ready Bosch LLM Farm client.
"""
import asyncio
from bosch_llm_farm import BoschLLMFarm, LLMConfig, create_client


def test_basic_functionality():
    """Test all the main functionality of the client"""
    print("🧪 Testing Production Bosch LLM Farm Client")
    print("=" * 50)
    
    # Test 1: Basic client creation
    print("\n1️⃣ Testing client creation...")
    try:
        client = BoschLLMFarm()
        print("✅ Client created successfully")
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return
    
    # Test 2: Simple completion
    print("\n2️⃣ Testing simple completion...")
    try:
        response = client.complete("Hello, how are you?")
        print(f"✅ Simple completion: {response[:100]}...")
    except Exception as e:
        print(f"❌ Simple completion failed: {e}")
        return
    
    # Test 3: Custom system prompt
    print("\n3️⃣ Testing custom system prompt...")
    try:
        response = client.complete(
            "Explain quantum computing",
            "You are a physics professor explaining concepts to undergraduates."
        )
        print(f"✅ Custom prompt: {response[:100]}...")
    except Exception as e:
        print(f"❌ Custom prompt failed: {e}")
    
    # Test 4: Detailed response
    print("\n4️⃣ Testing detailed response...")
    try:
        detailed = client.complete_with_details("What is machine learning?")
        print(f"✅ Content: {detailed.content[:50]}...")
        print(f"📊 Model: {detailed.model_used}")
        print(f"📊 Usage: {detailed.usage}")
    except Exception as e:
        print(f"❌ Detailed response failed: {e}")
    
    # Test 5: Convenience methods
    print("\n5️⃣ Testing convenience methods...")
    try:
        chat_resp = client.chat("What's 2+2?")
        print(f"💬 Chat method: {chat_resp}")
        
        code_resp = client.code_assistant("How to sort a list in Python?")
        print(f"💻 Code assistant: {code_resp[:50]}...")
    except Exception as e:
        print(f"❌ Convenience methods failed: {e}")
    
    # Test 6: Async functionality
    print("\n6️⃣ Testing async functionality...")
    try:
        async def test_async():
            response = await client.complete_async("What is async programming?")
            return response
        
        async_response = asyncio.run(test_async())
        print(f"⚡ Async response: {async_response[:50]}...")
    except Exception as e:
        print(f"❌ Async functionality failed: {e}")


def test_custom_config():
    """Test client with custom configuration"""
    print("\n🔧 Testing custom configuration...")
    
    try:
        # Create custom config (you'd use real credentials here)
        config = LLMConfig(
            model="gpt-4o-mini",
            api_key="your-real-api-key",  # Replace with actual
            subscription_key="your-real-sub-key",  # Replace with actual
            log_level="DEBUG"
        )
        
        client = BoschLLMFarm(config)
        print("✅ Custom config client created")
        
        # Test it
        response = client.complete("Hello from custom config!")
        print(f"✅ Custom config response: {response[:50]}...")
        
    except Exception as e:
        print(f"❌ Custom config test failed: {e}")
        if "your-real" in str(e):
            print("💡 Note: Replace placeholder credentials with actual values")


def test_error_handling():
    """Test error handling"""
    print("\n🚨 Testing error handling...")
    
    try:
        client = BoschLLMFarm()
        
        # Test empty input
        try:
            client.complete("")
            print("❌ Should have failed with empty input")
        except ValueError:
            print("✅ Correctly rejected empty input")
        except Exception as e:
            print(f"⚠️ Unexpected error type: {e}")
        
        # Test very long input (this might work, just testing)
        try:
            long_text = "Hello! " * 1000
            response = client.complete(long_text)
            print("✅ Handled long input successfully")
        except Exception as e:
            print(f"⚠️ Long input failed (might be expected): {type(e).__name__}")
            
    except Exception as e:
        print(f"❌ Error handling test setup failed: {e}")


if __name__ == "__main__":
    print("🎯 Comprehensive Test Suite for Bosch LLM Farm Client")
    print("IMPORTANT: Ensure you have valid credentials configured!")
    print()
    
    try:
        # Run all tests
        test_basic_functionality()
        test_custom_config()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 Test suite completed!")
        print("\n💡 If you see credential errors, remember to:")
        print("   1. Replace 'secrets' with your actual API key")
        print("   2. Replace 'my-farm-key' with your actual subscription key")
        print("   3. Ensure you're on the correct network/VPN")
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        print(f"Error type: {type(e).__name__}")