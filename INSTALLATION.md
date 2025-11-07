# Installation & Quick Start Guide

## Installation Options

### Option 1: Development Installation (Recommended)
```bash
# Clone/navigate to the project
cd llmfarm-pydantic

# Install in development mode
pip install -e .

# Install pydantic-ai for full functionality
pip install pydantic-ai
```

### Option 2: Direct Installation
```bash
pip install pydantic-ai
# Then use the working example directly
```

## Quick Test

After installation, test that everything works:

```bash
# Test the implementation
python examples/working_basic_example.py

# Should show:
# 🚀 Bosch Farm Provider - Working Basic Example
# ✅ Configuration created successfully
# ✅ Authentication headers ready
# 🎉 All functionality working correctly!
```

## Setting Up Real API Access

1. **Get your subscription key** from Bosch IT
2. **Set environment variables**:
   ```bash
   export BOSCH_FARM_API_KEY='your-genaiplatform-farm-subscription-key'
   ```
3. **Test connection** (after installing pydantic-ai):
   ```bash
   python examples/test_real_connection.py
   ```

## Configuration Options

### Environment Variables (Recommended)
```bash
export BOSCH_FARM_API_KEY='your-key'
export BOSCH_FARM_BASE_URL='custom-url'  # Optional
export BOSCH_FARM_API_VERSION='2024-08-01-preview'  # Optional
```

### Configuration Files
Create `config/farm_config.yaml`:
```yaml
farm_api_key: your-key-here
api_version: "2024-08-01-preview"
timeout: 30
max_retries: 3
```

Or `config/farm_config.json`:
```json
{
  "farm_api_key": "your-key-here",
  "api_version": "2024-08-01-preview",
  "timeout": 30,
  "max_retries": 3
}
```

## Usage Examples

### Basic Usage
```python
from llmfarm_pydantic import create_bosch_farm_provider
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

# Create provider
provider = create_bosch_farm_provider()

# Create model and agent
model = OpenAIChatModel('gpt-4o-mini', provider=provider)
agent = Agent(model)

# Use it!
result = await agent.run('Tell me about Bosch Group')
print(result.output)
```

### With Custom Configuration
```python
from llmfarm_pydantic import create_bosch_farm_provider, BoschFarmConfig

# Custom config
config = BoschFarmConfig(
    farm_api_key='your-key',
    api_version='2024-08-01-preview',
    timeout=60
)

# Create provider with custom config
provider = create_bosch_farm_provider(config)
```

## Troubleshooting

### Import Errors
If you see import errors:
1. Make sure you've installed with `pip install -e .`
2. Or use the `examples/working_basic_example.py` which handles imports automatically

### Connection Issues
1. Check your API key is correct
2. Verify the base URL matches your deployment
3. Check firewall/proxy settings if applicable

### Need Help?
- Check the examples in `examples/` directory
- Run `python examples/working_basic_example.py` to test functionality
- Review configuration options in `config/` directory