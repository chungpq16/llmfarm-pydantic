# Simple Usage Guide

## Two Ways to Use Bosch Farm LLM

This package now provides **two interfaces** to choose from:

### 1. 🚀 Simple Direct Interface (Recommended for most users)

Perfect for straightforward LLM interactions without complex AI workflows.

```python
from llmfarm_pydantic import BoschFarmLLM

# Simple usage
llm = BoschFarmLLM()
response = llm.ask("Tell me about Bosch Group")
print(response)

# With custom system prompt
response = llm.chat(
    "How does Bosch contribute to sustainability?",
    "You are an expert on Bosch's environmental initiatives"
)
print(response)
```

#### Original llmfarminf Style (Backward Compatible)

```python
from llmfarm_pydantic import llmfarminf

# Exact same interface as your original code
obj = llmfarminf()
prompt = "Tell me about Bosch group"
response = obj._completion(prompt, "You are a helpful assistant")
print(response)
```

### 2. 🔧 Advanced Pydantic AI Integration

For complex AI agent workflows, structured outputs, and advanced features.

```python
from llmfarm_pydantic import create_bosch_farm_provider
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

# Create provider
provider = create_bosch_farm_provider()

# Use with Pydantic AI
model = OpenAIChatModel(provider.deployment_name, provider=provider)
agent = Agent(model)

result = await agent.run("Tell me about Bosch")
print(result.data)
```

## 📦 Installation

```bash
# For simple interface only
pip install openai pyyaml

# For Pydantic AI integration
pip install pydantic-ai openai pyyaml
```

## ⚙️ Configuration

Both interfaces use the same environment variables:

```bash
export BOSCH_FARM_API_KEY="your-genaiplatform-farm-subscription-key"
export BOSCH_FARM_BASE_URL="https://aoai-farm.bosch-temp.com/api/openai/deployments/your-deployment"
```

## 🆚 When to Use Which Interface

| Feature | Simple Interface | Pydantic AI Integration |
|---------|-----------------|------------------------|
| **Ease of use** | ✅ Very simple | ⚠️ More complex |
| **Dependencies** | ✅ Minimal | ❌ Requires pydantic-ai |
| **Basic chat** | ✅ Perfect | ✅ Works |
| **Structured outputs** | ❌ Manual parsing | ✅ Built-in |
| **AI agents** | ❌ Not supported | ✅ Full support |
| **Streaming** | ❌ Not yet | ✅ Supported |
| **Function calling** | ❌ Manual | ✅ Built-in |

## 🎯 Complete Examples

### Simple Interface Examples

```python
from llmfarm_pydantic import BoschFarmLLM

# Basic usage
llm = BoschFarmLLM()

# Ask questions
answer = llm.ask("What is Bosch's main business?")
print(f"Answer: {answer}")

# Chat with context
response = llm.chat(
    "How can I improve manufacturing efficiency?",
    "You are an expert in industrial automation and Bosch technologies"
)
print(f"Expert advice: {response}")

# Use the _completion method (llmfarminf style)
result = llm._completion(
    "Explain Industry 4.0",
    "You are a technical expert"
)
print(f"Technical explanation: {result}")
```

### Error Handling

```python
from llmfarm_pydantic import BoschFarmLLM

try:
    llm = BoschFarmLLM()
    response = llm.ask("Your question here")
    print(response)
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Custom Configuration

```python
from llmfarm_pydantic import BoschFarmLLM

# With explicit configuration
llm = BoschFarmLLM(
    model="your-custom-deployment-name",
    farm_api_key="your-key",
    base_url="https://your-custom-endpoint.com/api/openai/deployments/model",
    api_version="2024-08-01-preview"
)
```

## 🔄 Migration from llmfarminf

If you have existing code using the `llmfarminf` pattern, you can migrate easily:

**Before:**
```python
from your_module import llmfarminf

obj = llmfarminf()
response = obj._completion("question", "system prompt")
```

**After:**
```python
from llmfarm_pydantic import llmfarminf  # or BoschFarmLLM

obj = llmfarminf()  # Same interface!
response = obj._completion("question", "system prompt")
```

## 🛠️ Development

```bash
# Clone the repository
git clone <repository-url>
cd llmfarm-pydantic

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Run simple examples
python simple_example.py
```

## 🆘 Troubleshooting

**"BOSCH_FARM_API_KEY is required"**
```bash
export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'
```

**Connection or 404 errors**
- Verify your API key is correct
- Check that your deployment URL is accessible
- Ensure the deployment name matches your configuration

**Import errors**
```bash
# For simple interface
pip install openai pyyaml

# For Pydantic AI features
pip install pydantic-ai
```

## 📚 API Reference

### BoschFarmLLM Class

#### Methods

- `ask(question: str) -> str` - Ask a simple question
- `chat(prompt: str, system_prompt: str) -> str` - Chat with custom system prompt  
- `_completion(usertext: str, sysprompt: str) -> str` - Low-level completion (llmfarminf compatible)

#### Properties

- `model: str` - The deployment/model name
- `base_url: str` - The API endpoint URL
- `api_version: str` - The API version
- `client: OpenAI` - The underlying OpenAI client