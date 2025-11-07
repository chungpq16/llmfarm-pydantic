# Installation Guide

## Prerequisites

- Python 3.9 or higher
- Access to Bosch Corporate LLM Farm
- API key for the LLM Farm service

## Installation Options

### Option 1: Development Installation (Recommended for testing)

1. Clone or download the project
2. Navigate to the project directory:
   ```bash
   cd llmfarm-pydantic
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

### Option 2: Direct Installation from Source

1. Navigate to the project directory:
   ```bash
   cd llmfarm-pydantic
   ```

2. Install the package:
   ```bash
   pip install .
   ```

### Option 3: Install with Development Dependencies

For development and testing:
```bash
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

Set these environment variables:

```bash
export BOSCH_FARM_API_KEY="your-api-key-here"
export BOSCH_FARM_BASE_URL="https://aoai-farm.bosch-temp.com"
export BOSCH_FARM_DEPLOYMENT_NAME="askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18"
export BOSCH_FARM_API_VERSION="2024-08-01-preview"
```

### Configuration File

Alternatively, create a config file (see `config/farm_config.yaml` for an example).

## Quick Test

After installation, test the setup:

```python
from llmfarm_pydantic import create_bosch_farm_provider
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

# Create provider
provider = create_bosch_farm_provider()

# Create model and agent
model = OpenAIChatModel('gpt-4o-mini', provider=provider)
agent = Agent(model)

# Test a simple interaction
result = agent.run_sync("Hello! Can you respond?")
print(result.data)
```

## Running Examples

After installation, you can run the examples:

```bash
python examples/basic_usage.py
python examples/config_file_example.py
python examples/advanced_usage.py
```

## Running Tests

To run the test suite:

```bash
pytest tests/
```

For coverage report:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you've installed the package correctly and all dependencies are available.

### API Connection Issues
1. Verify your API key is correct
2. Check that the base URL is accessible from your network
3. Ensure the deployment name matches your Bosch Farm setup

### Configuration Problems
1. Check that environment variables are set correctly
2. Verify config file syntax if using file-based configuration
3. Ensure all required configuration parameters are provided