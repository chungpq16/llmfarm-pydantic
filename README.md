# LLM Farm + Pydantic AI Integration

Simple integration of Pydantic AI with Bosch LLM Farm endpoint.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Update API key in `app.py`:
```python
API_KEY = "your-farm-key-here"
```

Run:
```bash
python app.py
```

## Features

- ✅ Async OpenAI client for LLM Farm
- ✅ Custom headers (genaiplatform-farm-subscription-key)
- ✅ Pydantic AI Agent wrapper
- ✅ Logging for troubleshooting
- ✅ Both async and sync interfaces
