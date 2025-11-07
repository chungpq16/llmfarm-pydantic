# Bosch LLM Farm Client

A clean, production-ready Python client for the Bosch LLM Farm API. This client provides a reliable interface that handles the specific requirements of the Bosch Farm (like the required `api-version` parameter).

## ✅ What Works

- **Reliable API communication** with Bosch Farm
- **Clean, modern interface** inspired by PydanticAI
- **Both sync and async support**
- **Comprehensive error handling**
- **Type hints and documentation**
- **Convenience methods** for common use cases

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from bosch_llm_farm import BoschLLMFarm, LLMConfig

# Option 1: Use with default config (remember to update credentials!)
client = BoschLLMFarm()
response = client.complete("Hello, how are you?")
print(response)

# Option 2: Use with custom config
config = LLMConfig(
    api_key="your-actual-api-key",
    subscription_key="your-actual-subscription-key",
    model="gpt-4o-mini"
)
client = BoschLLMFarm(config)
response = client.complete("Hello, world!")
print(response)

# Option 3: Convenience function
from bosch_llm_farm import create_client
client = create_client(
    api_key="your-api-key",
    subscription_key="your-sub-key"
)
```

## 📖 API Reference

### Main Methods

#### `complete(user_text, system_prompt="You are a helpful assistant")`
Synchronous text completion.

```python
response = client.complete(
    "Explain quantum computing", 
    "You are a physics professor"
)
```

#### `complete_async(user_text, system_prompt="You are a helpful assistant")`
Asynchronous text completion.

```python
response = await client.complete_async("What is AI?")
```

#### `complete_with_details(user_text, system_prompt="You are a helpful assistant")`
Returns detailed response with usage info.

```python
result = client.complete_with_details("Hello!")
print(f"Content: {result.content}")
print(f"Tokens: {result.usage}")
print(f"Model: {result.model_used}")
```

### Convenience Methods

#### `chat(message)`
Simple chat with helpful assistant.

```python
response = client.chat("What's the weather like?")
```

#### `code_assistant(code_question)`
Coding help with programming-focused prompt.

```python
response = client.code_assistant("How do I reverse a string in Python?")
```

## 🔧 Configuration

The `LLMConfig` class supports these options:

```python
@dataclass
class LLMConfig:
    model: str = "gpt-4o-mini"
    api_key: str = "secrets"  # Replace!
    subscription_key: str = "my-farm-key"  # Replace!
    base_url: str = "https://aoai-farm.bosch-temp.com/api/openai/deployments/..."
    api_version: str = "2024-08-01-preview"
    timeout: float = 30.0
    log_level: str = "INFO"
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_production.py
```

This tests:
- ✅ Basic completion
- ✅ Custom system prompts  
- ✅ Detailed responses
- ✅ Convenience methods
- ✅ Async functionality
- ✅ Error handling

## ❌ What Doesn't Work (And Why)

**PydanticAI Integration**: The original PydanticAI methods don't work because PydanticAI doesn't support the `extra_query` parameter needed to add `?api-version=2024-08-01-preview` to requests. This is required by the Bosch Farm.

## 🔄 Migration from Old Version

If you're using `llm_farm_hybrid.py`, here's how to migrate:

### Old Code:
```python
from llm_farm_hybrid import LLMFarmPydanticAI
llm = LLMFarmPydanticAI()
response = llm.completion("Hello", "You are helpful")
```

### New Code:
```python
from bosch_llm_farm import BoschLLMFarm
llm = BoschLLMFarm()
response = llm.complete("Hello", "You are helpful")
```

The interface is almost identical, just cleaner!

## 🛠 Architecture

This client uses:
- **Direct OpenAI API calls** with `extra_query` parameter
- **Clean dataclasses** for configuration
- **Async/await** support throughout
- **Proper error handling** and logging
- **Type hints** for better development experience

## 📝 Examples

### Basic Chat
```python
client = BoschLLMFarm()
response = client.chat("Tell me about Python")
print(response)
```

### Custom Assistant
```python
response = client.complete(
    "Review this code: print('hello')",
    "You are a senior code reviewer. Be constructive."
)
```

### Async Batch Processing
```python
async def process_questions(questions):
    client = BoschLLMFarm()
    tasks = [client.complete_async(q) for q in questions]
    return await asyncio.gather(*tasks)
```

## 🔒 Security Notes

- **Never commit API keys** to version control
- **Use environment variables** for credentials in production
- **Validate inputs** before sending to the API
- **Monitor usage** to avoid unexpected costs

## 🐛 Troubleshooting

### Common Issues:

1. **404 Error**: Check your API credentials and network access
2. **Authentication Error**: Verify `api_key` and `subscription_key`
3. **Timeout**: Increase `timeout` in config or check network
4. **Import Error**: Run `pip install -r requirements.txt`

### Debug Mode:

```python
config = LLMConfig(log_level="DEBUG")
client = BoschLLMFarm(config)  # Will show detailed logs
```

---

## 🎉 Why This Solution is Better

✅ **Reliable** - Uses proven direct OpenAI API approach  
✅ **Clean** - Modern, typed interface  
✅ **Fast** - Minimal dependencies  
✅ **Flexible** - Both sync and async support  
✅ **Maintainable** - Clear code structure  
✅ **Production-ready** - Proper error handling  

This gives you the best of both worlds: the reliability of direct API calls with the clean interface design of modern Python libraries!
