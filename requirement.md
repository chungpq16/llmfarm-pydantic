- Integrate Pydantic AI with a custom LLM that is compatible with the OpenAI API.
- No proxy required.. You can skip proxy on below example


## Simple way to connect LLM Custom


curl -x 127.0.0.1:3128 https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18/chat/completions?api-version=2024-08-01-preview -H "Content-Type: application/json" -H "genaiplatform-farm-subscription-key: <your-api-key>" -d "{ ""messages"": [ {""role"": ""system"", ""content"": ""You are a helpful assistant.""},{""role"": ""user"",""content"": [{""type"": ""text"",""text"": ""Tell me a short joke please.""} ] }],""max_tokens"": 4096,""stream"": false}" 




from openai import OpenAI

class llmfarminf():
    def __init__(self, model = "gpt-4o-mini") -> None:
        self.client = OpenAI(
            api_key="dummy",
            base_url="https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18",
            default_headers = {"genaiplatform-farm-subscription-key": "my-farm-key"}
        )

    def _gen_message(self, sysprompt, userprompt):
        return [
            {"role" : "system", "content" : sysprompt},
            {"role" : "user", "content" : userprompt}
        ]

    def _completion(self, usertext, sysprompt):
        messages = self._gen_message(sysprompt, usertext)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            extra_query={"api-version": "2024-08-01-preview"}
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    obj = llmfarminf()
    prompt = "Tell me about Bosch group"
    print(obj._completion(prompt, "You are a helpful assistant"))


####   I want to test follow this approach:


```python
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# 1) Configure your custom OpenAI-compatible LLM endpoint
client = AsyncOpenAI(
    base_url="https://my-llm-gateway.example.com/v1",
    api_key="YOUR_KEY_OR_DUMMY",
    default_headers={
        "X-Special-Header": "my-special-value",      # required by your provider
        "X-Org-Id": "my-org",                        # more custom headers if needed
    },
)

# 2) Wrap it in a PydanticAI OpenAI model
model = OpenAIModel(
    model_name="gpt-4o-mini",                       # whatever your server exposes
    provider=OpenAIProvider(openai_client=client),
)

# 3) Build the agent
agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant.",
)

# 4) Use the agent
result = agent.run_sync("Test my custom LLM with special headers.")
print(result.output)

```

--> But we should add log to see what is happens for troubleshooting
--- Make everything simple, focus on functionality first....   Summary very very short short what you did, just focus on solutions, I will ask to full summary it when needed