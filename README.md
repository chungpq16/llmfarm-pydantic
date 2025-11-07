# Pydantic AI Integration for Bosch Corporate LLM Farm

A secure, production-ready integration between [Pydantic AI](https://ai.pydantic.dev/) and Bosch's corporate LLM Farm, providing OpenAI-compatible API access with enterprise-grade configuration management.

## 🚀 Features

- **🔐 Secure Configuration**: Environment variables and config files for sensitive data management
- **⚙️ Flexible Setup**: Support for both YAML and JSON configuration formats
- **🔌 Drop-in Replacement**: Works seamlessly with existing Pydantic AI code
- **🏢 Corporate Ready**: Custom headers and authentication for Bosch Farm
- **📊 Production Features**: Proper error handling, logging, and validation
- **🧪 Well Tested**: Comprehensive test suite with mocking and integration tests

## 📋 Requirements

- Python 3.9+
- Pydantic AI
- Valid Bosch Farm API subscription key
- Access to Bosch corporate LLM Farm deployment

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd llmfarm-pydantic
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
# or for development
pip install -e .[dev]
```

3. **Set up environment variables**:
```bash
export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'
# Optional: export BOSCH_FARM_BASE_URL='custom-deployment-url'
```

## 🚀 Quick Start

### Basic Usage

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from llmfarm_pydantic import create_bosch_farm_provider

# Create provider using environment variables
provider = create_bosch_farm_provider()

# Create model and agent
model = OpenAIChatModel('gpt-4o-mini', provider=provider)
agent = Agent(model)

# Use it!
result = await agent.run('Tell me about Bosch Group')
print(result.output)
```

### Advanced Configuration

```python
from llmfarm_pydantic import BoschFarmProvider
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

# Create provider with explicit configuration
provider = BoschFarmProvider(
    farm_api_key='your-key',
    base_url='https://your-deployment.bosch-farm.com',
    api_version='2024-08-01-preview',
    config_path='config/farm_config.yaml'
)

model = OpenAIChatModel('gpt-4o-mini', provider=provider)
agent = Agent(model)

result = await agent.run('Hello from Bosch Farm!')
```

### Using Configuration Files

Create a `config/farm_config.yaml`:

```yaml
bosch_farm:
  api_version: "2024-08-01-preview"
  default_model: "gpt-4o-mini"
  timeout: 30
  max_retries: 3
```

Then use it:

```python
from llmfarm_pydantic import BoschFarmProvider

provider = BoschFarmProvider(config_path='config/farm_config.yaml')
# farm_api_key will be read from BOSCH_FARM_API_KEY environment variable
```

## 📁 Project Structure

```
llmfarm-pydantic/
├── src/
│   ├── __init__.py                 # Main package exports
│   ├── providers/
│   │   ├── __init__.py
│   │   └── bosch_farm.py          # BoschFarmProvider implementation
│   └── config/
│       ├── __init__.py
│       └── settings.py            # Configuration management
├── examples/
│   ├── basic_usage.py             # Simple usage examples
│   ├── config_file_example.py     # Configuration file examples
│   └── advanced_usage.py          # Advanced features demo
├── tests/
│   ├── test_config.py             # Configuration tests
│   ├── test_provider.py           # Provider tests
│   └── test_integration.py        # Integration tests
├── config/
│   ├── farm_config.yaml           # Example YAML config
│   ├── farm_config.json           # Example JSON config
│   └── .env.example               # Environment variable template
├── requirements.txt               # Package dependencies
├── pyproject.toml                 # Package configuration
└── README.md                      # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `BOSCH_FARM_API_KEY` | ✅ | Your genaiplatform-farm-subscription-key | - |
| `BOSCH_FARM_BASE_URL` | ❌ | Custom deployment URL | Default Bosch Farm URL |
| `BOSCH_FARM_API_VERSION` | ❌ | API version for requests | `2024-08-01-preview` |
| `BOSCH_FARM_DEFAULT_MODEL` | ❌ | Default model name | `gpt-4o-mini` |
| `BOSCH_FARM_TIMEOUT` | ❌ | Request timeout in seconds | `30` |
| `BOSCH_FARM_MAX_RETRIES` | ❌ | Maximum retry attempts | `3` |

### Configuration File Format

**YAML Example** (`config/farm_config.yaml`):
```yaml
bosch_farm:
  api_version: "2024-08-01-preview"
  default_model: "gpt-4o-mini"
  timeout: 30
  max_retries: 3
  # Note: API keys should be set via environment variables
```

**JSON Example** (`config/farm_config.json`):
```json
{
  "bosch_farm": {
    "api_version": "2024-08-01-preview",
    "default_model": "gpt-4o-mini",
    "timeout": 30,
    "max_retries": 3
  }
}
```

### Configuration Priority

1. **Explicit parameters** (highest priority)
2. **Environment variables**
3. **Configuration file values** (lowest priority)

## 🔒 Security Best Practices

### ✅ Do:
- Store API keys in environment variables
- Use configuration files for non-sensitive settings
- Keep `.env` files out of version control
- Validate configuration on startup
- Use HTTPS URLs only

### ❌ Don't:
- Hardcode API keys in source code
- Commit sensitive configuration to Git
- Use HTTP URLs for production
- Share API keys in logs or error messages

## 🎯 Examples

### Structured Output with Pydantic Models

```python
from pydantic import BaseModel
from pydantic_ai import Agent
from llmfarm_pydantic import create_bosch_farm_provider

class CompanyInfo(BaseModel):
    name: str
    founded_year: int
    headquarters: str
    industry: str

provider = create_bosch_farm_provider()
model = OpenAIChatModel('gpt-4o-mini', provider=provider)
agent = Agent(model, output_type=CompanyInfo)

result = await agent.run('Tell me about Bosch company')
print(f"Company: {result.output.name}")
print(f"Founded: {result.output.founded_year}")
```

### Custom HTTP Client

```python
import httpx
from llmfarm_pydantic import BoschFarmProvider

custom_client = httpx.AsyncClient(
    timeout=60,
    limits=httpx.Limits(max_connections=20)
)

provider = BoschFarmProvider(
    farm_api_key='your-key',
    http_client=custom_client
)
```

### Error Handling

```python
from llmfarm_pydantic import BoschFarmProvider, BoschFarmConfig

try:
    provider = BoschFarmProvider()
except ValueError as e:
    if "BOSCH_FARM_API_KEY" in str(e):
        print("Please set your API key:")
        print("export BOSCH_FARM_API_KEY='your-key'")
    else:
        print(f"Configuration error: {e}")
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_provider.py -v

# Run integration tests (requires API key)
BOSCH_FARM_API_KEY='your-key' pytest tests/test_integration.py -v
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd llmfarm-pydantic

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e .[dev]
```

### Running Examples

```bash
# Set your API key
export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'

# Run basic example
python examples/basic_usage.py

# Run configuration example
python examples/config_file_example.py

# Run advanced example
python examples/advanced_usage.py
```

## 🔧 Technical Details

### Provider Architecture

The `BoschFarmProvider` follows Pydantic AI's provider pattern:

- **Inherits from**: `Provider[AsyncOpenAI]`
- **Client Type**: `AsyncOpenAI` (from OpenAI Python SDK)
- **Authentication**: Custom header (`genaiplatform-farm-subscription-key`)
- **API Compatibility**: OpenAI-compatible endpoints

### API Integration

- **Base URL**: Bosch Farm deployment URL
- **Authentication**: Via `genaiplatform-farm-subscription-key` header
- **API Version**: Query parameter (`api-version=2024-08-01-preview`)
- **Model Support**: All Bosch Farm available models

### Key Components

1. **BoschFarmProvider**: Main provider class
2. **BoschFarmConfig**: Configuration management
3. **create_bosch_farm_provider()**: Convenience function
4. **Configuration loaders**: Support for env vars and files

## 📚 API Reference

### BoschFarmProvider

```python
class BoschFarmProvider(Provider[AsyncOpenAI]):
    def __init__(
        self,
        farm_api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
        config_path: Optional[str | Path] = None,
        openai_client: Optional[AsyncOpenAI] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None
```

### BoschFarmConfig

```python
@dataclass
class BoschFarmConfig:
    farm_api_key: Optional[str] = None
    base_url: Optional[str] = None
    api_version: str = "2024-08-01-preview"
    default_model: str = "gpt-4o-mini"
    timeout: int = 30
    max_retries: int = 3
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"BOSCH_FARM_API_KEY is required"**
- Set the environment variable: `export BOSCH_FARM_API_KEY='your-key'`

**"Import pydantic_ai could not be resolved"**
- Install pydantic-ai: `pip install pydantic-ai`

**404 "Resource not found" errors**
- ✅ **Fixed in v1.1**: Provider now automatically constructs correct URLs
- The provider automatically appends `/chat/completions` to your base URL
- Your base URL should be: `https://aoai-farm.bosch-temp.com/api/openai/deployments/your-deployment-name`
- Final URL will be: `https://aoai-farm.bosch-temp.com/api/openai/deployments/your-deployment-name/chat/completions`

**Connection timeouts**
- Increase timeout in config: `timeout: 60` 
- Check network connectivity to Bosch Farm

**Invalid API responses**
- Verify your API key is correct
- Check if your deployment URL is accessible
- Ensure API version matches deployment

### Getting Help

1. Check the [examples/](./examples/) directory
2. Review the [tests/](./tests/) for usage patterns
3. Open an issue on GitHub
4. Contact the Bosch LLM Farm support team

---

**Built with ❤️ for the Bosch developer community**